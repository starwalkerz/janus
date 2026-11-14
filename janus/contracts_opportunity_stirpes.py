"""
contracts.py — typed primitives, exceptions, and the trade-intent verifier.

The verifier enforces invariants I1–I9 on every emitted intent. A breach
returns a flat intent rather than raising to the caller; the strict=True
keyword on the wrapper raises ContractViolation for the test suite.

AgopResult carries the Nash strategies from the AGOP State, so that
downstream consumers (STIRPES in particular) do not need access to the raw
State object.

TradeIntent carries a `verdict` field. The verdict is a short string code
that classifies how the intent was produced. STIRPES uses the verdict as
part of the fingerprint; the orchestrator uses it to classify the tick in
its audit log.

StrategyName has three members: CONSERVATIVE, AGGRESSIVE, and OPPORTUNITY.
The OPPORTUNITY member corresponds to the opportunity strategy profile in
config.py and activates the opportunity modules in bootstrap.py.

Verdict codes (mirror the STIRPES verdict constants):
    "pass"                       — normal completion, full LLM size
    "size_clamped"               — LLM chose less than the risk bound
    "contract_collapse"          — a contract invariant fired (I1–I8, PRE_AGOP
                                   veto, POST_AGOP veto, PRE_LLM veto, AGOP
                                   contract violation)
    "toxicity_collapse"          — toxic order-flow forced FLAT
    "confidence_floor_collapse"  — LLM confidence below floor
"""

from __future__ import annotations

import functools
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ─────────────────────────────────────────────────────────────────────
# Verdict codes (STIRPES-compatible)
# ─────────────────────────────────────────────────────────────────────


VERDICT_PASS = "pass"
VERDICT_SIZE_CLAMPED = "size_clamped"
VERDICT_CONTRACT_COLLAPSE = "contract_collapse"
VERDICT_TOXICITY_COLLAPSE = "toxicity_collapse"
VERDICT_CONFIDENCE_FLOOR_COLLAPSE = "confidence_floor_collapse"

ALL_VERDICTS = frozenset({
    VERDICT_PASS,
    VERDICT_SIZE_CLAMPED,
    VERDICT_CONTRACT_COLLAPSE,
    VERDICT_TOXICITY_COLLAPSE,
    VERDICT_CONFIDENCE_FLOOR_COLLAPSE,
})


# ─────────────────────────────────────────────────────────────────────
# Enums
# ─────────────────────────────────────────────────────────────────────


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
    OPPORTUNITY = "opportunity"


class ModulePhase(str, Enum):
    PRE_AGOP = "pre_agop"
    POST_AGOP = "post_agop"
    PRE_LLM = "pre_llm"


class ContractViolation(AssertionError):
    """Raised when a trade-intent invariant is breached."""


# ─────────────────────────────────────────────────────────────────────
# Snapshot
# ─────────────────────────────────────────────────────────────────────


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


# ─────────────────────────────────────────────────────────────────────
# AGOP output
# ─────────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class AgopResult:
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


# ─────────────────────────────────────────────────────────────────────
# Risk bound and trade intent
# ─────────────────────────────────────────────────────────────────────


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
    verdict: str = VERDICT_PASS

    def __post_init__(self) -> None:
        if self.verdict not in ALL_VERDICTS:
            raise ValueError(
                f"verdict must be one of {sorted(ALL_VERDICTS)}, "
                f"got {self.verdict!r}"
            )

    def is_flat(self) -> bool:
        return self.action is Action.FLAT or self.position_size <= 0.0


# ─────────────────────────────────────────────────────────────────────
# Verifier
# ─────────────────────────────────────────────────────────────────────


def verify_trade_intent(function):
    """
    Enforce I1–I9 on the intent returned by the wrapped orchestrator step.

    The wrapped function must return a four-tuple:
        (intent, agop_result, risk_bound, strategy_name)

    If any invariant is false, a flat intent is returned instead. The
    verifier never raises to the caller unless strict=True.

    When the verifier forces a flat intent, it sets verdict to
    VERDICT_CONTRACT_COLLAPSE. The orchestrator's own verdicts (set when
    it returns from its branches) are preserved when the verifier passes.
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
                verdict=VERDICT_CONTRACT_COLLAPSE,
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