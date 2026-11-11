"""
modules/causality.py — Causalitybot as a POST_AGOP module.

Uses the actual starwalkerz/Causalitybot API:
    causalitybot.CausalSetMomentumBot(symbol, delta, ...)
        .ingest_orderbook(order_book, timestamp) -> Optional[MarketEvent]
        .generate_signal(event) -> Optional[dict]
            keys: direction, target, strength, curvature, mid, bottlenecks

The module is stateless: it creates a fresh bot per tick, feeds the snapshot
history as synthetic order books, and takes the last signal. The horizon
proxy is `signal["strength"]` (attractor strength, already in [0,1]); the
bottleneck proxy is max(score) from `signal["bottlenecks"]` normalized by
dividing by 10.0 and capping at 1.0.
"""

from __future__ import annotations

import importlib
import sys
from typing import Optional

import numpy as np

from janus.contracts import ModulePhase
from janus.modules.base import Module, ModuleContext, ModuleResult


def _import_causalitybot(local_path: str):
    if local_path and local_path not in sys.path:
        sys.path.insert(0, local_path)
    try:
        return importlib.import_module("causalitybot")
    except ImportError:
        return None


def _synthesize_order_book(
    price: float, volatility: float, slippage: float
) -> dict:
    spread = max(slippage / 10_000.0 * price, 0.01 * price)
    depth = max(volatility * price, 1.0)
    return {
        "bids": [[price - spread / 2.0, depth]],
        "asks": [[price + spread / 2.0, depth]],
    }


def _normalize_bottleneck(signal: dict) -> float:
    bottlenecks = signal.get("bottlenecks", [])
    if not bottlenecks:
        return 0.0
    scores = [score for _, score in bottlenecks]
    maximum_score = max(scores) if scores else 0.0
    return float(min(maximum_score / 10.0, 1.0))


class CausalityModule(Module):
    name = "causality"
    phase = ModulePhase.POST_AGOP

    def __init__(self, configuration) -> None:
        self._local_path = getattr(
            configuration, "causality_local_path", ""
        )
        self._http_url = getattr(configuration, "causality_http_url", "")

    def run(self, context: ModuleContext) -> ModuleResult:
        snapshot = context.snapshot
        if len(snapshot.history) < 30 or len(snapshot.history) != len(
            snapshot.timestamps
        ):
            return ModuleResult(
                name=self.name,
                phase=self.phase,
                notes="causalitybot unavailable; insufficient history",
            )

        module = _import_causalitybot(self._local_path)
        if module is None or not hasattr(module, "CausalSetMomentumBot"):
            return ModuleResult(
                name=self.name,
                phase=self.phase,
                notes="causalitybot unavailable; neutral",
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
                notes=f"causalitybot construction failed: {type(exception).__name__}",
            )

        last_event = None
        last_signal: Optional[dict] = None
        for index, (price, timestamp) in enumerate(
            zip(snapshot.history, snapshot.timestamps)
        ):
            order_book = _synthesize_order_book(
                price,
                snapshot.realized_volatility,
                snapshot.slippage,
            )
            try:
                event = bot.ingest_orderbook(order_book, timestamp)
            except Exception:
                event = None
            if event is None:
                continue
            last_event = event
            try:
                signal = bot.generate_signal(event)
            except Exception:
                signal = None
            if signal is not None:
                last_signal = signal

        if last_signal is None:
            return ModuleResult(
                name=self.name,
                phase=self.phase,
                notes="causalitybot: no horizon detected; neutral",
            )

        horizon = float(np.clip(last_signal.get("strength", 0.0), 0.0, 1.0))
        bottleneck = _normalize_bottleneck(last_signal)
        h0 = context.strategy.causality_h0
        kappa = context.strategy.causality_kappa
        multiplier = float(0.5 * (1.0 + np.tanh(kappa * (horizon - h0))))

        return ModuleResult(
            name=self.name,
            phase=self.phase,
            risk_multiplier=multiplier,
            context={
                "causality": {
                    "available": True,
                    "horizon": horizon,
                    "bottleneck": bottleneck,
                    "direction": int(last_signal.get("direction", 0)),
                    "target": float(last_signal.get("target", 0.0)),
                    "curvature": float(last_signal.get("curvature", 0.0)),
                }
            },
            notes=(
                f"causality: horizon={horizon:.3f} "
                f"bottleneck={bottleneck:.3f} "
                f"multiplier={multiplier:.4f}"
            ),
        )