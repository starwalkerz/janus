"""
modules/causality_opportunity.py — magnify Causalitybot horizons.

Formal definition
-----------------
Causalitybot (janus.modules.causality) returns a dict from the actual
starwalkerz/Causalitybot library with keys `direction`, `target`,
`strength`, `curvature`, `mid`, and `bottlenecks`. The opportunity
module reuses the same bot invocation and derives:

    H    = signal["strength"]            (attractor strength, in [0, 1])
    β    = max(score from bottlenecks)/10 (clipped to [0, 1])
    d_C  = sign(signal["direction"])     (order-flow direction)

The opportunity score is

    Ω_C = H · β

The natural direction d_μ = sign(mu). The signal is aligned if
d_C = d_μ. The downside score Δ is identical to the KAIROS module.

Qualification: Ω_C > 0.20 AND Δ > 0.50 AND aligned.

Patches: build_patches(d_μ, Ω_C, Δ).

Contrast with janus.modules.causality
-------------------------------------
The standard `causality` module (POST_AGOP) consumes the same signal as
a reason to dampen. This module (PRE_AGOP) consumes it as a reason to
trade. Enable one or the other, not both.
"""

from __future__ import annotations

import numpy as np

from janus.contracts import Action, MarketSnapshot, ModulePhase
from janus.modules.base import Module, ModuleContext, ModuleResult
from janus.modules.causality import (
    _import_causalitybot,
    _normalize_bottleneck,
    _synthesize_order_book,
)
from janus.modules.opportunity_common import (
    aligned_direction,
    build_patches,
    downside_score,
    natural_direction,
)


DEFAULT_HORIZON_THRESHOLD = 0.20
DEFAULT_DOWNSIDE_THRESHOLD = 0.50


class CausalityOpportunityModule(Module):
    name = "causality_opportunity"
    phase = ModulePhase.PRE_AGOP

    def __init__(self, configuration=None) -> None:
        pass

    def run(self, context: ModuleContext) -> ModuleResult:
        snapshot = context.snapshot
        configuration = context.configuration

        if len(snapshot.history) < 30 or len(snapshot.history) != len(
            snapshot.timestamps
        ):
            return ModuleResult(
                name=self.name,
                phase=self.phase,
                notes="causality_opportunity: insufficient history; neutral",
            )

        local_path = getattr(configuration, "causality_local_path", "")
        module = _import_causalitybot(local_path)
        if module is None or not hasattr(module, "CausalSetMomentumBot"):
            return ModuleResult(
                name=self.name,
                phase=self.phase,
                notes="causality_opportunity: causalitybot unavailable; neutral",
            )

        try:
            bot = module.CausalSetMomentumBot(
                symbol=snapshot.symbol,
                delta=0.5,
                curvature_window=50,
                horizon_sigma=3.0,
                bottleneck_threshold=5.0,
                risk_per_trade=0.01,
                max_position=1.0,
                tick_size=0.1,
            )
        except Exception as exception:
            return ModuleResult(
                name=self.name,
                phase=self.phase,
                notes=(
                    f"causality_opportunity: bot construction failed "
                    f"({type(exception).__name__})"
                ),
            )

        last_signal = None
        for price, timestamp in zip(snapshot.history, snapshot.timestamps):
            order_book = _synthesize_order_book(
                price, snapshot.realized_volatility, snapshot.slippage
            )
            try:
                event = bot.ingest_orderbook(order_book, timestamp)
            except Exception:
                continue
            if event is None:
                continue
            try:
                signal = bot.generate_signal(event)
            except Exception:
                continue
            if signal is not None:
                last_signal = signal

        if last_signal is None:
            return ModuleResult(
                name=self.name,
                phase=self.phase,
                notes="causality_opportunity: no horizon detected; neutral",
            )

        horizon = float(np.clip(last_signal.get("strength", 0.0), 0.0, 1.0))
        bottleneck = _normalize_bottleneck(last_signal)
        direction_sign = int(np.sign(last_signal.get("direction", 0)))

        if direction_sign > 0:
            horizon_direction = Action.LONG
        elif direction_sign < 0:
            horizon_direction = Action.SHORT
        else:
            return ModuleResult(
                name=self.name,
                phase=self.phase,
                context={
                    "causality_opportunity": {
                        "horizon": horizon,
                        "bottleneck": bottleneck,
                        "direction": None,
                        "qualified": False,
                    }
                },
                notes="causality_opportunity: no dominant direction; neutral",
            )

        natural = natural_direction(snapshot)

        if not aligned_direction(horizon_direction, natural):
            return ModuleResult(
                name=self.name,
                phase=self.phase,
                context={
                    "causality_opportunity": {
                        "horizon": horizon,
                        "bottleneck": bottleneck,
                        "horizon_direction": horizon_direction.value,
                        "natural_direction": natural.value if natural else None,
                        "qualified": False,
                    }
                },
                notes=(
                    f"causality_opportunity: horizon={horizon:.3f} "
                    f"bottleneck={bottleneck:.3f} not aligned; neutral"
                ),
            )

        downside = downside_score(snapshot)
        opportunity = float(np.clip(horizon * bottleneck, 0.0, 1.0))
        qualifies = (
            opportunity > DEFAULT_HORIZON_THRESHOLD
            and downside > DEFAULT_DOWNSIDE_THRESHOLD
        )

        if not qualifies:
            return ModuleResult(
                name=self.name,
                phase=self.phase,
                context={
                    "causality_opportunity": {
                        "horizon": horizon,
                        "bottleneck": bottleneck,
                        "direction": natural.value if natural else None,
                        "downside": downside,
                        "qualified": False,
                    }
                },
                notes=(
                    f"causality_opportunity: horizon={horizon:.3f} "
                    f"bottleneck={bottleneck:.3f} downside={downside:.3f} "
                    f"below threshold; neutral"
                ),
            )

        patches = build_patches(natural, opportunity, downside)

        return ModuleResult(
            name=self.name,
            phase=self.phase,
            axes_patch=patches,
            context={
                "causality_opportunity": {
                    "horizon": horizon,
                    "bottleneck": bottleneck,
                    "direction": natural.value,
                    "downside": downside,
                    "qualified": True,
                }
            },
            notes=(
                f"causality_opportunity: QUALIFIED horizon={horizon:.3f} "
                f"bottleneck={bottleneck:.3f} direction={natural.value} "
                f"downside={downside:.3f}"
            ),
        )