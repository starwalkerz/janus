"""
modules/sentiment.py — sentiment nudge as a PRE_AGOP module.
"""

from __future__ import annotations

import numpy as np

from janus.contracts import ModulePhase
from janus.modules.base import Module, ModuleContext, ModuleResult


class SentimentModule(Module):
    name = "sentiment"
    phase = ModulePhase.PRE_AGOP

    def __init__(self, configuration=None) -> None:
        pass

    def run(self, context: ModuleContext) -> ModuleResult:
        raw = context.snapshot.external_data.get("sentiment")
        if raw is None:
            return ModuleResult(
                name=self.name,
                phase=self.phase,
                notes="sentiment: absent; neutral",
            )

        sentiment = float(np.clip(float(raw), -1.0, 1.0))
        pain_patch = {
            "LONG": float(0.5 + 0.4 * sentiment),
            "SHORT": float(0.5 - 0.4 * sentiment),
        }
        readiness_patch = {
            "LONG": float(0.5 + 0.3 * sentiment),
            "SHORT": float(0.5 - 0.3 * sentiment),
        }

        return ModuleResult(
            name=self.name,
            phase=self.phase,
            axes_patch={
                "pain": pain_patch,
                "readiness": readiness_patch,
            },
            context={"sentiment": sentiment},
            notes=f"sentiment: {sentiment:+.3f}",
        )