"""
contracts.py — typed primitives, exceptions, and the trade-intent verifier.

The verifier enforces invariants I1–I9 on every emitted intent. A breach
returns a flat intent rather than raising to the caller; the strict=True
keyword on the wrapper raises ContractViolation for the test suite.

AgopResult now carries the Nash strategies from the AGOP State, so that
downstream consumers (STIRPES in particular) do not need access to the raw
State object.
"""

from __future__ import annotations

import functools
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Action(str, Enum):
    LONG = "LONG"
    FLAT = "FLAT"
    SHORT = "SHORT"


class AgopMode(str, Enum):
    LEGACY = "legacy"
    DBC = "dbc"


class StrategyName(str, Enum):
    CONSERVATIVE = "conservative"
    AGGRESSIVE = "aggressive"


class ModulePhase(str, Enum):
    PRE_AGOP = "pre_agop"
    POST_AGOP = "post_agop"
    PRE_LLM = "pre_llm"


class ContractViolation(AssertionError):
    """Raised when a trade-intent invariant is breached."""


@dataclass(frozen=True)
class MarketSnapshot:
    symbol: str
    price: float
    expected_return: float
    realized_volatility: float
    slippage: float
    slippage_maximum: float
    venue_risk: float
    signal_agreement: float
    order_flow_imbalance: float
    history: tuple[float, ...] = ()
    timestamps: tuple[float, ...] = ()
    external_data: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.realized_volatility <= 0:
            raise ValueError("realized_volatility must be positive")
        if self.slippage_maximum <= 0:
            raise ValueError("slippage_maximum must be positive")
        if not (0.0 <= self.venue_risk <= 1.0):
            raise ValueError("venue_risk must lie in [0,1]")


@dataclass(frozen=True)
class AgopResult:
    """
    The normalised output of an AGOP run.

    Fields
    ------
    mode                                     : the AGOP mode (legacy or dbc)
    ranking                                  : the ordered list of alternatives
    survivor_set                             : the sorted set of survivors
    lower_confidence_bound                   : the map from action to LCB
    composite_score                          : the map from action to Phi
    topology_class                           : the map from action to WL class
    convergence_depth                        : the fixed-point iteration depth
    capacity                                 : the derived or supplied capacity
    number_of_weisfeiler_lehman_classes      : the WL class count (dbc only)
    contract_verified                        : True if Theorem 5 held
    nash_dm                                  : the decision-maker's Nash strategy
    nash_cp                                  : the counter-party's Nash strategy
    contract_error                           : the breach reason, if any
    """
    mode: AgopMode
    ranking: list[str]
    survivor_set: list[str]
    lower_confidence_bound: dict[str, float]
    composite_score: dict[str, float]
    topology_class: dict[str, str]
    convergence_depth: int
    capacity: Optional[int]
    number_of_weisfeiler_lehman_classes: Optional[int]
    contract_verified: bool
    nash_dm: tuple[float, float] = (0.5, 0.5)
    nash_cp: tuple[float, float] = (0.5, 0.5)
    contract_error: Optional[str] = None


@dataclass(frozen=True)
class RiskBound:
    upper_position_size: float
    kelly_fraction: float
    module_multiplier: float
    toxic: bool
    reason: str


@dataclass(frozen=True)
class TradeIntent:
    action: Action
    position_size: float
    rationale: str
    agop_mode: AgopMode
    strategy: StrategyName
    skills_cited: list[str] = field(default_factory=list)
    vetoed: bool = False
    contract_forced_flat: bool = False

    def is_flat(self) -> bool:
        return self.action is Action.FLAT or self.position_size <= 0.0


def verify_trade_intent(function):
    """
    Enforce I1–I9 on the intent returned by the wrapped orchestrator step.

    The wrapped function must return a four-tuple:
        (intent, agop_result, risk_bound, strategy_name)

    If any invariant is false, a flat intent is returned instead. The
    verifier never raises to the caller unless strict=True.
    """
    @functools.wraps(function)
    def wrapper(*arguments, strict: bool = False, **keyword_arguments):
        intent, agop_result, risk_bound, strategy_name = function(
            *arguments, **keyword_arguments
        )

        def fail(reason: str) -> TradeIntent:
            if strict:
                raise ContractViolation(reason)
            return TradeIntent(
                action=Action.FLAT,
                position_size=0.0,
                rationale=f"contract: {reason}",
                agop_mode=intent.agop_mode,
                strategy=intent.strategy,
                vetoed=True,
                contract_forced_flat=True,
            )

        allowed_actions = set(agop_result.ranking) | {Action.FLAT.value}
        if intent.action.value not in allowed_actions:
            return fail(
                f"I1: action {intent.action.value} not in AGOP ranking"
            )

        cap = 0.10 if strategy_name.value == "conservative" else 0.35
        if not (0.0 <= intent.position_size <= cap + 1e-12):
            return fail(
                f"I2: position_size {intent.position_size} outside [0, {cap}]"
            )

        if agop_result.mode is AgopMode.DBC and not agop_result.contract_verified:
            if not (
                intent.action is Action.FLAT and intent.position_size == 0.0
            ):
                return fail(
                    "I3: DbC contract violated but intent not flat"
                )

        if risk_bound.toxic and not (
            intent.action is Action.FLAT and intent.position_size == 0.0
        ):
            return fail("I4: toxic flow but intent not flat")

        if intent.position_size > risk_bound.upper_position_size + 1e-12:
            return fail(
                f"I5: position_size {intent.position_size} exceeds risk bound "
                f"{risk_bound.upper_position_size}"
            )

        if risk_bound.upper_position_size > cap + 1e-12:
            return fail(
                f"I7: upper_position_size {risk_bound.upper_position_size} "
                f"exceeds base cap {cap}"
            )

        return intent

    return wrapper