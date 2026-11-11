"""
modules/regime.py — volatility-regime classifier as a PRE_AGOP module.
"""

from __future__ import annotations

import numpy as np

from janus.contracts import ModulePhase
from janus.modules.base import Module, ModuleContext, ModuleResult

CALM_THRESHOLD = 0.008
CHOPPY_THRESHOLD = 0.020


def _classify_regime(
    history: tuple[float, ...], realized_volatility: float
) -> str:
    if history and len(history) >= 8:
        array = np.asarray(history, dtype=float)
        realised = float(np.std(np.diff(array)))
    else:
        realised = realized_volatility
    if realised < CALM_THRESHOLD:
        return "calm"
    if realised > CHOPPY_THRESHOLD:
        return "choppy"
    return "normal"


class RegimeModule(Module):
    name = "regime"
    phase = ModulePhase.PRE_AGOP

    def __init__(self, configuration=None) -> None:
        pass

    def run(self, context: ModuleContext) -> ModuleResult:
        snapshot = context.snapshot
        regime = _classify_regime(
            snapshot.history, snapshot.realized_volatility
        )

        if regime == "calm":
            barrier_patch = {action: 0.10 for action in ("LONG", "SHORT")}
            readiness_patch = {"LONG": 0.70, "SHORT": 0.70}
        elif regime == "choppy":
            barrier_patch = {action: 0.90 for action in ("LONG", "SHORT")}
            readiness_patch = {"LONG": 0.30, "SHORT": 0.30}
        else:
            barrier_patch = {action: 0.50 for action in ("LONG", "SHORT")}
            readiness_patch = {"LONG": 0.60, "SHORT": 0.60}

        return ModuleResult(
            name=self.name,
            phase=self.phase,
            axes_patch={
                "barrier": barrier_patch,
                "readiness": readiness_patch,
            },
            context={"regime": regime},
            notes=f"regime: {regime}",
        )