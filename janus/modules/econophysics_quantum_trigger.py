"""
modules/econophysics.py — quantum econophysics modules for JANUS.

Two modules in one file, sharing one quantum runner, one correlation
extractor, and one event trigger:

    EconophysicsTunnelingModule  (PRE_AGOP)
        Encodes support/resistance walls as a potential barrier on a
        discretized Baaquie Hamiltonian, evolves the current price
        state through the barrier with a Trotterized circuit, and
        returns the tunneling probability. Patches AGOP's `barrier`
        axis from the result.

    EconophysicsHerdingModule    (POST_AGOP)
        Encodes cross-asset correlation as an Ising cost Hamiltonian
        and runs QAOA to estimate the magnetization order parameter M.
        Returns a risk multiplier 1 - alpha * |M|.

Event gating
------------
The IQM hardware path costs credits. Burning credits on every tick that
produces no actionable signal is wasteful. Both modules compute an event
trigger (see quantum_trigger.should_trigger_quantum_hardware) before
calling the quantum runner:

    trigger = kairos_flagged OR causality_horizon_above_threshold

When the trigger is False, the runner uses Qiskit Aer or classical-exact
(both free) and never contacts IQM Resonance. When the trigger is True
and iqm_token is set, the runner uses IQM. Every baseline tick is
completely free of credit burn.

The trigger result is recorded in each module's context under
`event_triggered` and `trigger_info`, so the audit log shows exactly
why each tick did or did not route to hardware.

Two modules, not one
--------------------
JANUS's invariant I7 forbids a PRE_AGOP module from contributing a risk
multiplier and I9 forbids a POST_AGOP module from patching axes. The two
effects are separable and the two phases are the natural home for each.
"""

from __future__ import annotations

import numpy as np

from janus.contracts import ModulePhase
from janus.modules.base import Module, ModuleContext, ModuleResult
from janus.modules.quantum_runner import (
    run_qaoa_herding,
    run_tunneling,
)
from janus.modules.quantum_trigger import (
    should_trigger_quantum_hardware,
)


# ─────────────────────────────────────────────────────────────────────
# Configuration accessors
# ─────────────────────────────────────────────────────────────────────


def _quantum_settings(context: ModuleContext) -> dict:
    configuration = context.configuration
    return {
        "iqm_token": getattr(configuration, "quantum_iqm_token", "") or None,
        "iqm_server": getattr(
            configuration, "quantum_iqm_server",
            "https://resonance.iqm.tech",
        ),
        "iqm_backend": getattr(
            configuration, "quantum_iqm_backend", None
        ) or None,
        "tunneling_qubits": int(
            getattr(configuration, "quantum_tunneling_qubits", 4)
        ),
        "tunneling_time": float(
            getattr(configuration, "quantum_tunneling_time", 3.0)
        ),
        "tunneling_trotter_steps": int(
            getattr(configuration, "quantum_tunneling_trotter_steps", 3)
        ),
        "herding_qubits": int(
            getattr(configuration, "quantum_herding_qubits", 4)
        ),
        "herding_layers": int(
            getattr(configuration, "quantum_herding_layers", 1)
        ),
        "herding_shots": int(
            getattr(configuration, "quantum_herding_shots", 4000)
        ),
    }


def _event_gate(context: ModuleContext) -> tuple[bool, dict]:
    """Compute the event trigger for the current tick."""
    configuration = context.configuration

    gate_enabled = bool(
        getattr(configuration, "quantum_gate_enabled", True)
    )
    if not gate_enabled:
        return True, {"gating_disabled": True}

    return should_trigger_quantum_hardware(
        snapshot=context.snapshot,
        configuration=configuration,
        prior_results=context.prior_results,
        gate_on_kairos=bool(
            getattr(configuration, "quantum_gate_on_kairos", True)
        ),
        gate_on_causality=bool(
            getattr(configuration, "quantum_gate_on_causality", True)
        ),
        kairos_amplitude_threshold=float(
            getattr(configuration, "quantum_gate_kairos_threshold", 0.05)
        ),
        causality_horizon_threshold=float(
            getattr(configuration, "quantum_gate_causality_threshold", 0.20)
        ),
    )


# ─────────────────────────────────────────────────────────────────────
# Support / resistance detection from the snapshot history
# ─────────────────────────────────────────────────────────────────────


def _detect_barrier(
    history: tuple[float, ...],
    current_price: float,
    tolerance_fraction: float = 0.01,
):
    if len(history) < 10 or current_price <= 0:
        return None

    grid = max(current_price * tolerance_fraction, 1e-9)
    profile: dict[float, float] = {}
    for price in history:
        level = round(price / grid) * grid
        profile[level] = profile.get(level, 0.0) + 1.0

    candidates = [
        (level, volume) for level, volume in profile.items()
        if level > current_price
    ]
    if not candidates:
        return None

    barrier, _ = max(candidates, key=lambda pair: pair[1])
    return float(barrier)


def _detect_support(
    history: tuple[float, ...],
    current_price: float,
    tolerance_fraction: float = 0.01,
):
    if len(history) < 10 or current_price <= 0:
        return None

    grid = max(current_price * tolerance_fraction, 1e-9)
    profile: dict[float, float] = {}
    for price in history:
        level = round(price / grid) * grid
        profile[level] = profile.get(level, 0.0) + 1.0

    candidates = [
        (level, volume) for level, volume in profile.items()
        if level < current_price
    ]
    if not candidates:
        return None

    support, _ = max(candidates, key=lambda pair: pair[1])
    return float(support)


# ─────────────────────────────────────────────────────────────────────
# Baaquie Hamiltonian construction
# ─────────────────────────────────────────────────────────────────────


def _build_baaquie_hamiltonian(
    n_qubits: int,
    log_price_min: float,
    log_price_max: float,
    barrier_position: float,
    barrier_strength: float,
    barrier_width: float,
    kinetic_hopping: float = 1.0,
    drift: float = 0.0,
) -> tuple[np.ndarray, np.ndarray]:
    dimension = 1 << n_qubits
    positions = np.linspace(log_price_min, log_price_max, dimension)

    hamiltonian = np.zeros((dimension, dimension), dtype=float)

    for index in range(dimension - 1):
        hamiltonian[index, index + 1] = -kinetic_hopping
        hamiltonian[index + 1, index] = -kinetic_hopping
        if drift != 0.0:
            hamiltonian[index, index + 1] -= drift
            hamiltonian[index + 1, index] += drift

    potential = barrier_strength * np.exp(
        -((positions - barrier_position) ** 2) / (2.0 * barrier_width ** 2)
    )
    for index in range(dimension):
        hamiltonian[index, index] += potential[index]

    return hamiltonian, positions


# ─────────────────────────────────────────────────────────────────────
# Cross-asset correlation extractor
# ─────────────────────────────────────────────────────────────────────


def _extract_couplings_and_fields(
    snapshot,
    n_qubits: int,
) -> tuple[dict[tuple[int, int], float], dict[int, float]]:
    external = getattr(snapshot, "external_data", {}) or {}
    assets = external.get("econophysics_assets")

    couplings: dict[tuple[int, int], float] = {}
    fields: dict[int, float] = {}

    if assets and len(assets) >= 2:
        names = sorted(assets.keys())[:n_qubits]
        return_series: dict[str, np.ndarray] = {}
        for name in names:
            prices = np.asarray(assets[name], dtype=float)
            if prices.size < 3:
                continue
            return_series[name] = np.diff(np.log(prices))

        names = list(return_series.keys())
        n_assets = len(names)
        for i in range(n_assets):
            series_i = return_series[names[i]]
            fields[i] = float(np.tanh(series_i.mean() * 100.0))
            for j in range(i + 1, n_assets):
                series_j = return_series[names[j]]
                length = min(series_i.size, series_j.size)
                if length < 3:
                    continue
                correlation = float(np.corrcoef(
                    series_i[-length:], series_j[-length:],
                )[0, 1])
                if not np.isnan(correlation):
                    couplings[(i, j)] = float(
                        np.clip(correlation, -1.0, 1.0)
                    )

        return couplings, fields

    history = np.asarray(snapshot.history, dtype=float)
    if history.size < 4 * n_qubits:
        for i in range(n_qubits):
            fields[i] = 0.0
        return couplings, fields

    window = max(history.size // n_qubits, 3)
    return_series_list = []
    for i in range(n_qubits):
        start = i * (history.size - window) // max(n_qubits - 1, 1)
        chunk = history[start:start + window]
        if chunk.size < 3:
            return_series_list.append(np.zeros(2))
            continue
        return_series_list.append(np.diff(np.log(chunk)))

    for i in range(n_qubits):
        series_i = return_series_list[i]
        fields[i] = float(np.tanh(series_i.mean() * 100.0))
        for j in range(i + 1, n_qubits):
            series_j = return_series_list[j]
            length = min(series_i.size, series_j.size)
            if length < 3:
                continue
            correlation = float(np.corrcoef(
                series_i[-length:], series_j[-length:],
            )[0, 1])
            if not np.isnan(correlation):
                couplings[(i, j)] = float(
                    np.clip(correlation, -1.0, 1.0)
                )

    return couplings, fields


# ─────────────────────────────────────────────────────────────────────
# Tunneling module (PRE_AGOP)
# ─────────────────────────────────────────────────────────────────────


class EconophysicsTunnelingModule(Module):
    name = "econophysics_tunneling"
    phase = ModulePhase.PRE_AGOP

    def __init__(self, configuration=None) -> None:
        pass

    def run(self, context: ModuleContext) -> ModuleResult:
        snapshot = context.snapshot
        settings = _quantum_settings(context)

        barrier = _detect_barrier(snapshot.history, snapshot.price)
        support = _detect_support(snapshot.history, snapshot.price)

        if barrier is None and support is None:
            return ModuleResult(
                name=self.name,
                phase=self.phase,
                notes="econophysics_tunneling: no barrier detected; neutral",
            )

        n_qubits = settings["tunneling_qubits"]

        log_current = np.log(max(snapshot.price, 1e-9))
        log_lo = log_current - 0.15
        log_hi = log_current + 0.15

        barrier_distance_up = (
            abs(np.log(barrier) - log_current)
            if barrier is not None
            else np.inf
        )
        barrier_distance_down = (
            abs(np.log(support) - log_current)
            if support is not None
            else np.inf
        )

        if barrier_distance_up <= barrier_distance_down and barrier is not None:
            target_log = np.log(barrier)
            direction = "up"
        elif support is not None:
            target_log = np.log(support)
            direction = "down"
        else:
            return ModuleResult(
                name=self.name,
                phase=self.phase,
                notes=(
                    "econophysics_tunneling: no barrier or support; "
                    "neutral"
                ),
            )

        barrier_strength = 2.0
        barrier_width = 0.02
        hamiltonian, positions = _build_baaquie_hamiltonian(
            n_qubits=n_qubits,
            log_price_min=log_lo,
            log_price_max=log_hi,
            barrier_position=target_log,
            barrier_strength=barrier_strength,
            barrier_width=barrier_width,
        )

        initial_index = int(np.argmin(np.abs(positions - log_current)))

        # Event gate: skip IQM when no signal is present.
        event_triggered, trigger_info = _event_gate(context)

        try:
            result = run_tunneling(
                hamiltonian_matrix=hamiltonian,
                initial_index=initial_index,
                n_qubits=n_qubits,
                evolution_time=settings["tunneling_time"],
                trotter_steps=settings["tunneling_trotter_steps"],
                shots=2000,
                iqm_token=settings["iqm_token"],
                iqm_server=settings["iqm_server"],
                iqm_backend=settings["iqm_backend"],
                event_triggered=event_triggered,
            )
        except Exception as exception:
            return ModuleResult(
                name=self.name,
                phase=self.phase,
                notes=(
                    f"econophysics_tunneling: quantum runner failed: "
                    f"{type(exception).__name__}"
                ),
            )

        probabilities = result["probabilities"]
        beyond_indices = np.where(
            positions > target_log + barrier_width
            if direction == "up"
            else positions < target_log - barrier_width
        )[0]
        tunneling_probability = float(probabilities[beyond_indices].sum())

        effective_barrier = float(np.clip(
            1.0 - tunneling_probability, 0.05, 0.95,
        ))

        return ModuleResult(
            name=self.name,
            phase=self.phase,
            axes_patch={
                "barrier": {
                    "LONG": effective_barrier if direction == "up" else 0.5,
                    "SHORT": effective_barrier if direction == "down" else 0.5,
                },
            },
            context={
                "econophysics_tunneling": {
                    "direction": direction,
                    "barrier_price": float(np.exp(target_log)),
                    "tunneling_probability": tunneling_probability,
                    "effective_barrier": effective_barrier,
                    "backend": result["backend"],
                    "event_triggered": event_triggered,
                    "trigger_info": trigger_info,
                },
            },
            notes=(
                f"tunneling: direction={direction} "
                f"P_tunnel={tunneling_probability:.4f} "
                f"barrier={effective_barrier:.4f} "
                f"backend={result['backend']} "
                f"gated={not event_triggered}"
            ),
        )


# ─────────────────────────────────────────────────────────────────────
# Herding module (POST_AGOP)
# ─────────────────────────────────────────────────────────────────────


class EconophysicsHerdingModule(Module):
    name = "econophysics_herding"
    phase = ModulePhase.POST_AGOP

    def __init__(self, configuration=None) -> None:
        pass

    def run(self, context: ModuleContext) -> ModuleResult:
        snapshot = context.snapshot
        settings = _quantum_settings(context)

        couplings, fields = _extract_couplings_and_fields(
            snapshot, settings["herding_qubits"],
        )

        if (
            not couplings
            and all(abs(value) < 1e-9 for value in fields.values())
        ):
            return ModuleResult(
                name=self.name,
                phase=self.phase,
                notes=(
                    "econophysics_herding: no structure detected; neutral"
                ),
            )

        # Event gate: skip IQM when no signal is present.
        event_triggered, trigger_info = _event_gate(context)

        try:
            result = run_qaoa_herding(
                couplings=couplings,
                fields=fields,
                n_qubits=settings["herding_qubits"],
                layers=settings["herding_layers"],
                shots=settings["herding_shots"],
                iqm_token=settings["iqm_token"],
                iqm_server=settings["iqm_server"],
                iqm_backend=settings["iqm_backend"],
                event_triggered=event_triggered,
            )
        except Exception as exception:
            return ModuleResult(
                name=self.name,
                phase=self.phase,
                notes=(
                    f"econophysics_herding: quantum runner failed: "
                    f"{type(exception).__name__}"
                ),
            )

        magnetization = float(
            np.clip(abs(result["magnetization"]), 0.0, 1.0)
        )

        sensitivity = getattr(
            context.strategy, "econophysics_herding_sensitivity", 0.5,
        )
        risk_multiplier = float(
            np.clip(1.0 - sensitivity * magnetization, 0.0, 1.0)
        )

        return ModuleResult(
            name=self.name,
            phase=self.phase,
            risk_multiplier=risk_multiplier,
            context={
                "econophysics_herding": {
                    "magnetization": magnetization,
                    "signed_magnetization": float(
                        result["magnetization"]
                    ),
                    "cost": float(result["cost"]),
                    "risk_multiplier": risk_multiplier,
                    "layers": settings["herding_layers"],
                    "backend": result["backend"],
                    "converged": bool(result["converged"]),
                    "event_triggered": event_triggered,
                    "trigger_info": trigger_info,
                },
            },
            notes=(
                f"herding: |M|={magnetization:.4f} "
                f"multiplier={risk_multiplier:.4f} "
                f"backend={result['backend']} "
                f"gated={not event_triggered}"
            ),
        )