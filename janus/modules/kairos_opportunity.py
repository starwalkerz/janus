"""
modules/kairos_opportunity.py — magnify KAIROS anomalies as opportunity signals.

Formal definition
-----------------
The KAIROS anomaly filter (janus.modules.kairos) returns a KairosReport
with `flagged`, `amplitude`, `window`, and `backend`. When flagged, the
signal is interpreted as a reason to trade rather than a reason to
dampen. The direction of the anomaly is determined from the recent
slope of the price history (KAIROS does not expose direction).

The natural direction is d_μ = sign(mu). The opportunity score is

    Ω_K = KAIROS.amplitude    (when flagged, else 0)

The downside score Δ is computed identically to the other opportunity
modules: Δ = (1 - slippage/slip_max) · (1 - venue_risk).

Qualification: Ω_K > 0.05 AND Δ > 0.50 AND aligned with d_μ.

Patches: build_patches(d_μ, Ω_K, Δ).

Contrast with janus.modules.kairos
----------------------------------
The standard `kairos` module (POST_AGOP) consumes the signal as a reason
to dampen. This module (PRE_AGOP) consumes the same signal as a reason
to trade. Enable one or the other, not both.
"""

from __future__ import annotations

import numpy as np

from janus.contracts import Action, ModulePhase
from janus.modules.base import Module, ModuleContext, ModuleResult
from janus.modules.kairos import (
    _call_http as kairos_call_http,
    _call_local as kairos_call_local,
)
from janus.modules.opportunity_common import (
    aligned_direction,
    build_patches,
    downside_score,
    natural_direction,
    recent_slope,
)


DEFAULT_AMPLITUDE_THRESHOLD = 0.05
DEFAULT_DOWNSIDE_THRESHOLD = 0.50
DEFAULT_CYCLE_LENGTH_RATIO = 0.25


class KairosOpportunityModule(Module):
    name = "kairos_opportunity"
    phase = ModulePhase.PRE_AGOP

    def __init__(self, configuration=None) -> None:
        pass

    def run(self, context: ModuleContext) -> ModuleResult:
        snapshot = context.snapshot
        configuration = context.configuration

        if len(snapshot.history) < 8 or len(snapshot.history) != len(
            snapshot.timestamps
        ):
            return ModuleResult(
                name=self.name,
                phase=self.phase,
                notes="kairos_opportunity: insufficient history; neutral",
            )

        cycle_length = snapshot.external_data.get("cycle_period")
        if cycle_length is None:
            cycle_length = len(snapshot.history) * DEFAULT_CYCLE_LENGTH_RATIO
        if cycle_length <= 0:
            return ModuleResult(
                name=self.name,
                phase=self.phase,
                notes="kairos_opportunity: invalid cycle period; neutral",
            )

        amplitude = max(snapshot.realized_volatility, 1e-6)

        report = kairos_call_local(
            snapshot.history,
            snapshot.timestamps,
            float(cycle_length),
            amplitude,
            getattr(configuration, "kairos_local_path", ""),
            getattr(configuration, "kairos_quantum", False),
        )
        if report is None:
            data = kairos_call_http(
                snapshot.history,
                snapshot.timestamps,
                float(cycle_length),
                amplitude,
                getattr(configuration, "kairos_http_url", ""),
                getattr(configuration, "kairos_quantum", False),
            )
            if data is None:
                return ModuleResult(
                    name=self.name,
                    phase=self.phase,
                    notes="kairos_opportunity: kairos unavailable; neutral",
                )
            flagged = bool(data.get("flagged", False))
            anomaly_amplitude = float(
                data.get("amplitude", {}).get("classical", 0.0)
            )
        else:
            flagged = bool(report.flagged)
            anomaly_amplitude = float(report.classical_amplitude)

        if not flagged:
            return ModuleResult(
                name=self.name,
                phase=self.phase,
                context={
                    "kairos_opportunity": {
                        "amplitude": anomaly_amplitude,
                        "flagged": False,
                        "qualified": False,
                    }
                },
                notes=(
                    f"kairos_opportunity: no anomaly flagged "
                    f"(amplitude={anomaly_amplitude:.3f}); neutral"
                ),
            )

        window_size = max(4, len(snapshot.history) // 4)
        slope_sign = recent_slope(snapshot.history, window_size)
        if slope_sign == 0:
            return ModuleResult(
                name=self.name,
                phase=self.phase,
                context={
                    "kairos_opportunity": {
                        "amplitude": anomaly_amplitude,
                        "flagged": True,
                        "direction": None,
                        "qualified": False,
                    }
                },
                notes="kairos_opportunity: anomaly flagged but direction unclear",
            )

        anomaly_direction = (
            Action.LONG if slope_sign > 0 else Action.SHORT
        )
        natural = natural_direction(snapshot)

        if not aligned_direction(anomaly_direction, natural):
            return ModuleResult(
                name=self.name,
                phase=self.phase,
                context={
                    "kairos_opportunity": {
                        "amplitude": anomaly_amplitude,
                        "flagged": True,
                        "anomaly_direction": anomaly_direction.value,
                        "natural_direction": natural.value if natural else None,
                        "qualified": False,
                    }
                },
                notes=(
                    f"kairos_opportunity: anomaly={anomaly_direction.value} "
                    f"not aligned with natural direction; neutral"
                ),
            )

        downside = downside_score(snapshot)
        opportunity = float(np.clip(anomaly_amplitude, 0.0, 1.0))
        qualifies = (
            opportunity > DEFAULT_AMPLITUDE_THRESHOLD
            and downside > DEFAULT_DOWNSIDE_THRESHOLD
        )

        if not qualifies:
            return ModuleResult(
                name=self.name,
                phase=self.phase,
                context={
                    "kairos_opportunity": {
                        "amplitude": opportunity,
                        "direction": natural.value if natural else None,
                        "downside": downside,
                        "qualified": False,
                    }
                },
                notes=(
                    f"kairos_opportunity: amplitude={opportunity:.3f} "
                    f"downside={downside:.3f} below threshold; neutral"
                ),
            )

        patches = build_patches(natural, opportunity, downside)

        return ModuleResult(
            name=self.name,
            phase=self.phase,
            axes_patch=patches,
            context={
                "kairos_opportunity": {
                    "amplitude": opportunity,
                    "direction": natural.value,
                    "downside": downside,
                    "qualified": True,
                }
            },
            notes=(
                f"kairos_opportunity: QUALIFIED amplitude={opportunity:.3f} "
                f"direction={natural.value} downside={downside:.3f}"
            ),
        )