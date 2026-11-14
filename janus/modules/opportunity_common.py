"""
Shared helpers for the opportunity magnifier modules.

See the README section "Opportunity modules" for the formal definitions
of Δ, d_μ, and the amplification patches.
"""

from __future__ import annotations

from typing import Optional

import numpy as np

from janus.contracts import Action, MarketSnapshot


PAIN_GAIN = 0.30
READINESS_GAIN = 0.30
BARRIER_GAIN = 0.30


def downside_score(snapshot: MarketSnapshot) -> float:
    """Δ = (1 - slippage/slippage_max) · (1 - venue_risk), in [0, 1]."""
    slippage_factor = float(
        np.clip(1.0 - snapshot.slippage / snapshot.slippage_maximum, 0.0, 1.0)
    )
    venue_factor = float(np.clip(1.0 - snapshot.venue_risk, 0.0, 1.0))
    return slippage_factor * venue_factor


def natural_direction(snapshot: MarketSnapshot) -> Optional[Action]:
    """d_μ = sign(mu). None if mu is too close to zero."""
    if abs(snapshot.expected_return) < 1e-9:
        return None
    return Action.LONG if snapshot.expected_return > 0 else Action.SHORT


def build_patches(
    direction: Action,
    opportunity: float,
    downside: float,
    pain_gain: float = PAIN_GAIN,
    readiness_gain: float = READINESS_GAIN,
    barrier_gain: float = BARRIER_GAIN,
) -> dict[str, dict[str, float]]:
    """Build the axis patches for a qualifying opportunity signal."""
    if direction is Action.FLAT:
        return {}

    amplitude = opportunity * downside
    action_name = direction.value

    pain_value = float(np.clip(0.5 + pain_gain * amplitude, 0.0, 1.0))
    readiness_value = float(np.clip(0.5 + readiness_gain * amplitude, 0.0, 1.0))
    barrier_value = float(np.clip(0.5 - barrier_gain * amplitude, 0.0, 1.0))

    return {
        "pain": {action_name: pain_value},
        "readiness": {action_name: readiness_value},
        "barrier": {action_name: barrier_value},
    }


def aligned_direction(
    signal_direction: Action,
    natural_direction_value: Optional[Action],
) -> bool:
    """True if the signal's direction matches the natural direction."""
    if natural_direction_value is None:
        return False
    return signal_direction is natural_direction_value


def recent_slope(history: tuple[float, ...], window_size: int) -> int:
    """Sign of the second-half-minus-first-half mean over the last window.

    Returns 1 for positive slope, -1 for negative, 0 for flat.
    Used to determine the direction of an anomaly detected by KAIROS
    or Causalitybot, neither of which exposes direction in its public
    report.
    """
    if len(history) < 4 or window_size < 4:
        return 0
    recent = history[-window_size:]
    midpoint = len(recent) // 2
    if midpoint == 0:
        return 0
    first_mean = float(np.mean(recent[:midpoint]))
    second_mean = float(np.mean(recent[midpoint:]))
    threshold = 1e-9 * max(abs(first_mean), abs(second_mean), 1.0)
    if second_mean - first_mean > threshold:
        return 1
    if first_mean - second_mean > threshold:
        return -1
    return 0