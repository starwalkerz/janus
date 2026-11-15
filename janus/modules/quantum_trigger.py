"""
Event gating for the quantum econophysics modules.

The IQM hardware path costs credits. Burning credits on every tick that
produces no actionable signal is wasteful. This module provides a shared
event trigger that gates the IQM path on KAIROS and Causalitybot
observations:

    trigger = kairos_flagged OR causality_horizon_above_threshold

When the trigger is False, the quantum_runner uses the classical-exact or
Qiskit Aer path (both free) and never contacts IQM Resonance. When the
trigger is True and iqm_token is set, the runner uses IQM.

The trigger can reuse signal results from prior phase modules
(prior_results) to avoid invoking KAIROS or Causalitybot a second time.
When prior_results is None or does not contain a usable signal, the
trigger falls back to a direct, classical-only invocation of the
underlying KAIROS or Causalitybot detector.

Determinism (I6) is preserved: the trigger is a deterministic function
of the snapshot, the configuration, and the prior_results, all of which
are themselves deterministic per tick.

Alphabetic-order notes
----------------------
PRE_AGOP modules execute alphabetically: agop_opportunity (a),
causality_opportunity (c), econophysics_tunneling (e),
kairos_opportunity (k), regime (r), sentiment (s).

econophysics_tunneling therefore runs before kairos_opportunity but
after causality_opportunity. It sees causality_opportunity in
prior_results but must call KAIROS directly.

POST_AGOP modules execute alphabetically: causality (c),
econophysics_herding (e), kairos (k). econophysics_herding runs after
causality but before kairos. It sees the entire PRE_AGOP accumulated
results (including kairos_opportunity and causality_opportunity when
those are enabled), and it sees the causality dampening module when
that is enabled. It must call KAIROS directly only when
kairos_opportunity is disabled (i.e., under the conservative or
aggressive strategy).

See the README section on quantum econophysics for the operational
rationale.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from janus.modules.causality import (
    _import_causalitybot,
    _normalize_bottleneck,
    _synthesize_order_book,
)
from janus.modules.kairos import (
    _call_http as kairos_call_http,
    _call_local as kairos_call_local,
)


DEFAULT_KAIROS_AMPLITUDE_THRESHOLD = 0.05
DEFAULT_CAUSALITY_HORIZON_THRESHOLD = 0.20


def should_trigger_quantum_hardware(
    snapshot: Any,
    configuration: Any,
    prior_results: dict | None = None,
    gate_on_kairos: bool = True,
    gate_on_causality: bool = True,
    kairos_amplitude_threshold: float = DEFAULT_KAIROS_AMPLITUDE_THRESHOLD,
    causality_horizon_threshold: float = DEFAULT_CAUSALITY_HORIZON_THRESHOLD,
) -> tuple[bool, dict]:
    """Determine whether the current tick should route to IQM hardware.

    Returns (triggered, diagnostics). The diagnostics dict records which
    signal sources were checked, what they reported, and whether each
    one fired. The dict is placed in the module's context for the audit
    log.
    """
    if gate_on_kairos:
        kairos_data = _check_kairos_cached(
            snapshot,
            configuration,
            prior_results,
            kairos_amplitude_threshold,
        )
    else:
        kairos_data = {
            "checked": False,
            "available": False,
            "flagged": False,
            "amplitude": 0.0,
            "triggered": False,
        }

    if gate_on_causality:
        causality_data = _check_causality_cached(
            snapshot,
            configuration,
            prior_results,
            causality_horizon_threshold,
        )
    else:
        causality_data = {
            "checked": False,
            "available": False,
            "horizon": 0.0,
            "bottleneck": 0.0,
            "triggered": False,
        }

    triggered = (
        kairos_data.get("triggered", False)
        or causality_data.get("triggered", False)
    )
    return triggered, {"kairos": kairos_data, "causality": causality_data}


# ─────────────────────────────────────────────────────────────────────
# KAIROS check
# ─────────────────────────────────────────────────────────────────────


def _check_kairos_cached(
    snapshot: Any,
    configuration: Any,
    prior_results: dict | None,
    threshold: float,
) -> dict:
    """Check KAIROS, preferring prior_results over a direct call."""
    if prior_results:
        for name in ("kairos_opportunity", "kairos"):
            result = prior_results.get(name)
            if result is None or not getattr(result, "context", None):
                continue
            inner = result.context.get(name, {})
            if not inner:
                continue
            if name == "kairos":
                flagged = bool(inner.get("flagged", False))
                amplitude = float(inner.get("amplitude", 0.0))
            else:
                flagged = bool(
                    inner.get("flagged", inner.get("qualified", False))
                )
                amplitude = float(inner.get("amplitude", 0.0))
            return {
                "checked": True,
                "available": True,
                "flagged": flagged,
                "amplitude": amplitude,
                "triggered": flagged and amplitude > threshold,
                "source": f"prior_results.{name}",
            }

    return _check_kairos(snapshot, configuration, threshold)


def _check_kairos(
    snapshot: Any,
    configuration: Any,
    threshold: float,
) -> dict:
    result = {
        "checked": True,
        "available": False,
        "flagged": False,
        "amplitude": 0.0,
        "triggered": False,
        "source": "direct_call",
    }

    if len(snapshot.history) < 8 or len(snapshot.history) != len(
        snapshot.timestamps
    ):
        return result

    cycle_length = snapshot.external_data.get("cycle_period")
    if cycle_length is None:
        cycle_length = len(snapshot.history) * 0.25
    if cycle_length <= 0:
        return result

    amplitude_scale = max(snapshot.realized_volatility, 1e-6)
    local_path = getattr(configuration, "kairos_local_path", "")
    http_url = getattr(configuration, "kairos_http_url", "")

    report = kairos_call_local(
        snapshot.history,
        snapshot.timestamps,
        float(cycle_length),
        amplitude_scale,
        local_path,
        False,
    )
    if report is None:
        data = kairos_call_http(
            snapshot.history,
            snapshot.timestamps,
            float(cycle_length),
            amplitude_scale,
            http_url,
            False,
        )
        if data is not None:
            result["available"] = True
            result["flagged"] = bool(data.get("flagged", False))
            result["amplitude"] = float(
                data.get("amplitude", {}).get("classical", 0.0)
            )
    else:
        result["available"] = True
        result["flagged"] = bool(report.flagged)
        result["amplitude"] = float(report.classical_amplitude)

    result["triggered"] = (
        result["flagged"] and result["amplitude"] > threshold
    )
    return result


# ─────────────────────────────────────────────────────────────────────
# Causalitybot check
# ─────────────────────────────────────────────────────────────────────


def _check_causality_cached(
    snapshot: Any,
    configuration: Any,
    prior_results: dict | None,
    threshold: float,
) -> dict:
    """Check Causalitybot, preferring prior_results over a direct call."""
    if prior_results:
        for name in ("causality", "causality_opportunity"):
            result = prior_results.get(name)
            if result is None or not getattr(result, "context", None):
                continue
            inner = result.context.get(name, {})
            if not inner:
                continue
            horizon = float(inner.get("horizon", 0.0))
            bottleneck = float(inner.get("bottleneck", 0.0))
            return {
                "checked": True,
                "available": True,
                "horizon": horizon,
                "bottleneck": bottleneck,
                "triggered": horizon > threshold,
                "source": f"prior_results.{name}",
            }

    return _check_causality(snapshot, configuration, threshold)


def _check_causality(
    snapshot: Any,
    configuration: Any,
    threshold: float,
) -> dict:
    result = {
        "checked": True,
        "available": False,
        "horizon": 0.0,
        "bottleneck": 0.0,
        "triggered": False,
        "source": "direct_call",
    }

    if len(snapshot.history) < 30 or len(snapshot.history) != len(
        snapshot.timestamps
    ):
        return result

    local_path = getattr(configuration, "causality_local_path", "")
    module = _import_causalitybot(local_path)
    if module is None or not hasattr(module, "CausalSetMomentumBot"):
        return result

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
    except Exception:
        return result

    last_signal = None
    for price, timestamp in zip(snapshot.history, snapshot.timestamps):
        order_book = _synthesize_order_book(
            price, snapshot.realized_volatility, snapshot.slippage
        )
        try:
            event = bot.ingest_orderbook(order_book, timestamp)
            if event is not None:
                signal = bot.generate_signal(event)
                if signal is not None:
                    last_signal = signal
        except Exception:
            continue

    if last_signal is None:
        return result

    result["available"] = True
    result["horizon"] = float(
        np.clip(last_signal.get("strength", 0.0), 0.0, 1.0)
    )
    result["bottleneck"] = _normalize_bottleneck(last_signal)
    result["triggered"] = result["horizon"] > threshold
    return result