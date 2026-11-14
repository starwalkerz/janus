"""
modules/agop_opportunity.py — amplify raw market opportunity.

Formal definition
-----------------
Ω_A = |mu|/sigma · (1 - venue_risk) · (1 - slippage/slip_max)

Qualifies when Ω_A > 0.40 AND Δ > 0.50.
Patches: build_patches(d_μ, clip(Ω_A / 2, 0, 1), Δ).
"""

from __future__ import annotations

import numpy as np

from janus.contracts import ModulePhase
from janus.modules.base import Module, ModuleContext, ModuleResult
from janus.modules.opportunity_common import (
    build_patches,
    downside_score,
    natural_direction,
)


DEFAULT_OPPORTUNITY_THRESHOLD = 0.40
DEFAULT_DOWNSIDE_THRESHOLD = 0.50


class AgopOpportunityModule(Module):
    name = "agop_opportunity"
    phase = ModulePhase.PRE_AGOP

    def __init__(self, configuration=None) -> None:
        pass

    def run(self, context: ModuleContext) -> ModuleResult:
        snapshot = context.snapshot

        natural = natural_direction(snapshot)
        if natural is None:
            return ModuleResult(
                name=self.name,
                phase=self.phase,
                notes="agop_opportunity: no expected return direction; neutral",
            )

        sigma = max(snapshot.realized_volatility, 1e-9)
        edge_ratio = abs(snapshot.expected_return) / sigma
        slippage_factor = float(
            np.clip(1.0 - snapshot.slippage / snapshot.slippage_maximum, 0.0, 1.0)
        )
        venue_factor = float(np.clip(1.0 - snapshot.venue_risk, 0.0, 1.0))

        opportunity = float(edge_ratio * slippage_factor * venue_factor)
        downside = downside_score(snapshot)

        qualifies = (
            opportunity > DEFAULT_OPPORTUNITY_THRESHOLD
            and downside > DEFAULT_DOWNSIDE_THRESHOLD
        )

        if not qualifies:
            return ModuleResult(
                name=self.name,
                phase=self.phase,
                context={
                    "agop_opportunity": {
                        "opportunity": opportunity,
                        "direction": natural.value,
                        "downside": downside,
                        "qualified": False,
                    }
                },
                notes=(
                    f"agop_opportunity: opportunity={opportunity:.3f} "
                    f"downside={downside:.3f} below threshold; neutral"
                ),
            )

        scaled_opportunity = float(np.clip(opportunity / 2.0, 0.0, 1.0))
        patches = build_patches(natural, scaled_opportunity, downside)

        return ModuleResult(
            name=self.name,
            phase=self.phase,
            axes_patch=patches,
            context={
                "agop_opportunity": {
                    "opportunity": opportunity,
                    "direction": natural.value,
                    "downside": downside,
                    "qualified": True,
                }
            },
            notes=(
                f"agop_opportunity: QUALIFIED opportunity={opportunity:.3f} "
                f"direction={natural.value} downside={downside:.3f}"
            ),
        )