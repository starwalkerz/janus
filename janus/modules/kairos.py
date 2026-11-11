"""
modules/kairos.py — KAIROS anomaly detection as a POST_AGOP module.

Uses the actual starwalkerz/kairos API:
    core.GmGCycle(name, period, phase0, mu_L, sigma_L, mu_T, sigma_T, amplitude)
    detect.detect(series, t, cycles, *, kappa, threshold, quantum, ...)
        -> AnomalyReport

The module contributes a risk multiplier in [0,1] derived from the classical
anomaly amplitude. A flagged anomaly dampens the bound under the conservative
profile; the aggressive profile leaves it untouched.
"""

from __future__ import annotations

import importlib
import sys
from typing import Optional

import numpy as np

from janus.contracts import ModulePhase
from janus.modules.base import Module, ModuleContext, ModuleResult


def _import_kairos(local_path: str):
    if local_path and local_path not in sys.path:
        sys.path.insert(0, local_path)
    try:
        core = importlib.import_module("core")
        detect_module = importlib.import_module("detect")
        return core, detect_module
    except ImportError:
        return None, None


def _call_local(
    history: tuple[float, ...],
    timestamps: tuple[float, ...],
    period: float,
    amplitude: float,
    local_path: str,
    quantum: bool,
):
    if len(history) < 8 or len(history) != len(timestamps):
        return None
    core, detect_module = _import_kairos(local_path)
    if core is None or detect_module is None:
        return None
    try:
        cycle = core.GmGCycle(
            name="session",
            period=period,
            phase0=0.0,
            mu_L=-0.5 * period,
            sigma_L=0.25 * period,
            mu_T=+0.5 * period,
            sigma_T=0.25 * period,
            amplitude=amplitude,
        )
        report = detect_module.detect(
            np.asarray(history, dtype=float),
            np.asarray(timestamps, dtype=float),
            [cycle],
            threshold=0.05,
            quantum=quantum,
        )
        return report
    except Exception:
        return None


def _call_http(
    history: tuple[float, ...],
    timestamps: tuple[float, ...],
    period: float,
    amplitude: float,
    http_url: str,
    quantum: bool,
):
    if not http_url or len(history) < 8:
        return None
    try:
        import httpx
        payload = {
            "series": list(history),
            "t": list(timestamps),
            "cycles": [
                {
                    "name": "session",
                    "period": period,
                    "phase0": 0.0,
                    "mu_L": -0.5 * period,
                    "sigma_L": 0.25 * period,
                    "mu_T": +0.5 * period,
                    "sigma_T": 0.25 * period,
                    "amplitude": amplitude,
                }
            ],
            "threshold": 0.05,
            "quantum": quantum,
        }
        with httpx.Client(timeout=10.0) as client:
            response = client.post(
                f"{http_url.rstrip('/')}/api/detect", json=payload
            )
            response.raise_for_status()
            data = response.json()
        return data
    except Exception:
        return None


class KairosModule(Module):
    name = "kairos"
    phase = ModulePhase.POST_AGOP

    def __init__(self, configuration) -> None:
        self._local_path = getattr(configuration, "kairos_local_path", "")
        self._http_url = getattr(configuration, "kairos_http_url", "")
        self._quantum = getattr(configuration, "kairos_quantum", False)

    def run(self, context: ModuleContext) -> ModuleResult:
        snapshot = context.snapshot
        period = len(snapshot.history) / 4.0 if snapshot.history else 24.0
        amplitude = max(snapshot.realized_volatility, 1e-6)

        report = _call_local(
            snapshot.history,
            snapshot.timestamps,
            period,
            amplitude,
            self._local_path,
            self._quantum,
        )
        if report is None:
            data = _call_http(
                snapshot.history,
                snapshot.timestamps,
                period,
                amplitude,
                self._http_url,
                self._quantum,
            )
            if data is None:
                return ModuleResult(
                    name=self.name,
                    phase=self.phase,
                    notes="kairos unavailable; neutral",
                )
            flagged = bool(data.get("flagged", False))
            classical_amplitude = float(
                data.get("amplitude", {}).get("classical", 0.0)
            )
            backend = str(data.get("amplitude", {}).get("backend", "http"))
            window = data.get("window", {"lo": 0.0, "hi": 0.0})
        else:
            flagged = bool(report.flagged)
            classical_amplitude = float(report.classical_amplitude)
            backend = report.quantum_backend
            window = {"lo": report.window[0], "hi": report.window[1]}

        if not flagged:
            multiplier = 1.0
        else:
            dampening = context.strategy.kairos_dampening
            multiplier = float(max(0.0, 1.0 - dampening * classical_amplitude))

        return ModuleResult(
            name=self.name,
            phase=self.phase,
            risk_multiplier=multiplier,
            context={
                "kairos": {
                    "available": True,
                    "flagged": flagged,
                    "amplitude": classical_amplitude,
                    "window": window,
                    "backend": backend,
                }
            },
            notes=(
                f"kairos: flagged={flagged} "
                f"amplitude={classical_amplitude:.4f} "
                f"multiplier={multiplier:.4f}"
            ),
        )