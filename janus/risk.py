"""
risk.py — Kelly sizing, the toxic-flow gate, and the composed risk bound.

The module multiplier is the product of all enabled POST_AGOP modules'
risk multipliers, each in [0,1]. The upper bound never exceeds the base
cap (invariant I7).
"""

from __future__ import annotations

import numpy as np

from janus.config import StrategyProfile
from janus.contracts import (
    Action,
    AgopResult,
    MarketSnapshot,
    RiskBound,
)


def kelly_fraction(win_probability: float, payoff_ratio: float) -> float:
    """f* = p - (1-p)/b, clamped to [0,1]."""
    if payoff_ratio <= 0:
        return 0.0
    fraction = win_probability - (1.0 - win_probability) / payoff_ratio
    return float(np.clip(fraction, 0.0, 1.0))


def toxic_flow(
    snapshot: MarketSnapshot,
    action: Action,
    threshold: float,
) -> bool:
    if action is Action.FLAT:
        return False
    sign = 1.0 if action is Action.LONG else -1.0
    return (snapshot.order_flow_imbalance * sign) < -threshold


def bound(
    snapshot: MarketSnapshot,
    agop_result: AgopResult,
    module_multiplier: float,
    profile: StrategyProfile,
    action: Action,
) -> RiskBound:
    if not agop_result.contract_verified:
        return RiskBound(
            upper_position_size=0.0,
            kelly_fraction=0.0,
            module_multiplier=0.0,
            toxic=False,
            reason="agop contract violated; forced flat",
        )

    lower_bound = agop_result.lower_confidence_bound.get(action.value, -1.0)
    if lower_bound < profile.lower_confidence_bound_floor:
        return RiskBound(
            upper_position_size=0.0,
            kelly_fraction=0.0,
            module_multiplier=0.0,
            toxic=False,
            reason=(
                f"lower confidence bound {lower_bound:.4f} below floor "
                f"{profile.lower_confidence_bound_floor}"
            ),
        )

    win_probability = float(
        np.clip(
            0.5
            + 0.5
            * np.tanh(
                snapshot.expected_return
                / max(snapshot.realized_volatility, 1e-12)
            ),
            0.01,
            0.99,
        )
    )
    payoff_ratio = max(
        abs(snapshot.expected_return)
        / max(snapshot.realized_volatility, 1e-12),
        0.1,
    )
    kelly = kelly_fraction(win_probability, payoff_ratio)

    upper_bound = (
        profile.position_cap
        * profile.kelly_coefficient
        * kelly
        * module_multiplier
    )

    is_toxic = toxic_flow(snapshot, action, profile.toxicity_threshold)
    if is_toxic:
        upper_bound = 0.0

    reason = (
        f"kelly={kelly:.4f} coefficient={profile.kelly_coefficient} "
        f"module_multiplier={module_multiplier:.4f} "
        f"cap={profile.position_cap}"
    )
    return RiskBound(
        upper_position_size=float(
            max(0.0, min(upper_bound, profile.position_cap))
        ),
        kelly_fraction=kelly,
        module_multiplier=module_multiplier,
        toxic=is_toxic,
        reason=reason,
    )