"""
features.py — market snapshot to AGOP axes.

Each axis is a documented map from observable quantities to [0,1]. The maps
are deterministic and involve no learned parameters.
"""

from __future__ import annotations

import numpy as np

from janus.contracts import Action, MarketSnapshot

EDGE_KAPPA = 2.0
SIGNAL_KAPPA = 2.0


def _logistic(value: float) -> float:
    return float(1.0 / (1.0 + np.exp(-value)))


def build_axes(
    snapshot: MarketSnapshot,
) -> dict[str, dict[str, float]]:
    edge = snapshot.expected_return / max(
        snapshot.realized_volatility, 1e-12
    )
    pain = _logistic(EDGE_KAPPA * abs(edge))
    integration = float(
        np.clip(
            1.0 - snapshot.slippage / snapshot.slippage_maximum, 0.0, 1.0
        )
    )
    regulatory = float(np.clip(snapshot.venue_risk, 0.0, 1.0))
    readiness_long = 0.5 * (
        1.0 + np.tanh(SIGNAL_KAPPA * snapshot.signal_agreement)
    )
    readiness_short = 1.0 - readiness_long
    barrier = float(
        np.clip(
            snapshot.realized_volatility
            / max(snapshot.realized_volatility * 3.0, 1e-12),
            0.0,
            1.0,
        )
    )

    direction = np.sign(edge) if abs(edge) > 1e-9 else 0.0
    pain_long = pain if direction >= 0 else pain * 0.5
    pain_short = pain if direction <= 0 else pain * 0.5

    return {
        "pain": {
            Action.LONG.value: pain_long,
            Action.FLAT.value: 0.5,
            Action.SHORT.value: pain_short,
        },
        "integration": {
            Action.LONG.value: integration,
            Action.FLAT.value: 1.0,
            Action.SHORT.value: integration,
        },
        "regulatory": {
            Action.LONG.value: regulatory,
            Action.FLAT.value: 0.0,
            Action.SHORT.value: regulatory,
        },
        "readiness": {
            Action.LONG.value: float(readiness_long),
            Action.FLAT.value: 0.5,
            Action.SHORT.value: float(readiness_short),
        },
        "barrier": {
            Action.LONG.value: barrier,
            Action.FLAT.value: 0.0,
            Action.SHORT.value: barrier,
        },
    }