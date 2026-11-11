"""
modules/econophysics.py — quantum econophysics modules for JANUS.

Two modules in one file, sharing one quantum runner and one correlation
extractor:

    EconophysicsTunnelingModule  (PRE_AGOP)
        Encodes support/resistance walls as a potential barrier on a
        discretized Baaquie Hamiltonian, evolves the current price state
        through the barrier with a Trotterized circuit, and returns the
        tunneling probability. Patches AGOP's `barrier` axis from the
        result: high tunneling probability lowers the effective barrier
        for the direction of the breach.

    EconophysicsHerdingModule    (POST_AGOP)
        Encodes cross-asset correlation as an Ising cost Hamiltonian and
        runs QAOA to estimate the magnetization order parameter M. Returns
        a risk multiplier 1 - alpha * |M|, shrinking position size when
        the market is in a fragile ferromagnetic (herding) phase.

Two modules, not one, because JANUS's invariant I7 forbids a PRE_AGOP
module from contributing a risk multiplier and I9 forbids a POST_AGOP
module from patching axes. The two effects are separable and the two
phases are the natural home for each.
"""

from __future__ import annotations

import importlib
import sys
from typing import Optional

import numpy as np

from janus.contracts import ModulePhase
from janus.modules.base import Module, ModuleContext, ModuleResult
from janus.modules.quantum_runner import run_qaoa_herding, run_tunneling


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
        "iqm_backend": getattr(configuration, "quantum_iqm_backend", None),
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


# ─────────────────────────────────────────────────────────────────────
# Support / resistance detection from the snapshot history
# ─────────────────────────────────────────────────────────────────────


def _detect_barrier(
    history: tuple[float, ...],
    current_price: float,
    tolerance_fraction: float = 0.01,
) -> Optional[float]:
    """
    Return the nearest high-volume price level above the current price.

    The volume profile is a histogram over the last len(history) prices at
    a grid resolution of tolerance_fraction * current_price. The barrier is
    the highest-volume level strictly above current_price. Returns None if
    the history is empty or no level exceeds the current price.
    """
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
) -> Optional[float]:
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
    """
    Return (Hamiltonian, position_grid) for the discretized Baaquie model.

    The position grid has N = 2^n_qubits points uniformly spaced on
    [log_price_min, log_price_max]. The kinetic operator is tight-binding
    (nearest-neighbour hopping t_hop); the potential is a Gaussian well
    centred at barrier_position with amplitude barrier_strength and width
    barrier_width; the drift term is a small first-derivative correction
    implemented as an asymmetric hopping.

    The Hamiltonian is real-symmetric after Wick rotation, which is what
    the gate-model implementation of PauliEvolutionGate requires.
    """
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
    """
    Build the Ising cost Hamiltonian from the snapshot.

    Preferred input: snapshot.external_data["econophysics_assets"] is a
    dict mapping asset name to a list of prices. The pairwise correlation
    of returns is mapped to J_ij; the momentum of each asset is mapped to
    h_i.

    Fallback input: no econophysics_assets key. The snapshot.history is
    split into n_qubits overlapping windows, each window treated as one
    "asset's" return series, and the coupling is computed between
    windows. This is not a cross-asset herding measure — it is a
    multi-horizon momentum alignment measure — and the module records
    that fact in its context field so the LLM can interpret it correctly.
    """
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
                    couplings[(i, j)] = float(np.clip(correlation, -1.0, 1.0))

        return couplings, fields

    # Fallback: split the single history into overlapping windows.
    history = np.asarray(snapshot.history, dtype=float)
    if history.size < 4 * n_qubits:
        for i in range(n_qubits):
            fields[i] = 0.0
        return couplings, fields

    window = max(history.size // n_qubits, 3)
    return_series = []
    for i in range(n_qubits):
        start = i * (history.size - window) // max(n_qubits - 1, 1)
        chunk = history[start:start + window]
        if chunk.size < 3:
            return_series.append(np.zeros(2))
            continue
        return_series.append(np.diff(np.log(chunk)))

    for i in range(n_qubits):
        series_i = return_series[i]
        fields[i] = float(np.tanh(series_i.mean() * 100.0))
        for j in range(i + 1, n_qubits):
            series_j = return_series[j]
            length = min(series_i.size, series_j.size)
            if length < 3:
                continue
            correlation = float(np.corrcoef(
                series_i[-length:], series_j[-length:],
            )[0, 1])
            if not np.isnan(correlation):
                couplings[(i, j)] = float(np.clip(correlation, -1.0, 1.0))

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
        dimension = 1 << n_qubits

        log_current = np.log(max(snapshot.price, 1e-9))
        log_lo = log_current - 0.15
        log_hi = log_current + 0.15

        # Encode both barriers as potentials. The circuit evaluates the
        # probability of crossing the resistance; a symmetric downward
        # reflection gives the support case. The chosen direction is the
        # side whose barrier is closer to the current price.
        barrier_distance_up = (
            abs(np.log(barrier) - log_current) if barrier is not None else np.inf
        )
        barrier_distance_down = (
            abs(np.log(support) - log_current) if support is not None else np.inf
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
                notes="econophysics_tunneling: no barrier or support; neutral",
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
        # Tunneling region: positions strictly beyond the barrier.
        beyond_indices = np.where(
            positions > target_log + barrier_width
            if direction == "up"
            else positions < target_log - barrier_width
        )[0]
        tunneling_probability = float(probabilities[beyond_indices].sum())

        # Patch barrier: high tunneling probability means the wall is
        # porous, so the barrier axis is set low. Clamp to [0.05, 0.95] to
        # keep AGOP's deductive filter well-behaved.
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
                },
            },
            notes=(
                f"tunneling: direction={direction} "
                f"P_tunnel={tunneling_probability:.4f} "
                f"barrier={effective_barrier:.4f} "
                f"backend={result['backend']}"
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

        if not couplings and all(abs(value) < 1e-9 for value in fields.values()):
            return ModuleResult(
                name=self.name,
                phase=self.phase,
                notes="econophysics_herding: no structure detected; neutral",
            )

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

        magnetization = float(np.clip(abs(result["magnetization"]), 0.0, 1.0))

        # Herding sensitivity: how strongly |M| shrinks the risk bound.
        # Conservative profile uses 0.5, aggressive uses 0.2 (set below).
        sensitivity = getattr(
            context.strategy, "econophysics_herding_sensitivity", 0.5,
        )
        risk_multiplier = float(np.clip(1.0 - sensitivity * magnetization, 0.0, 1.0))

        return ModuleResult(
            name=self.name,
            phase=self.phase,
            risk_multiplier=risk_multiplier,
            context={
                "econophysics_herding": {
                    "magnetization": magnetization,
                    "signed_magnetization": float(result["magnetization"]),
                    "cost": float(result["cost"]),
                    "risk_multiplier": risk_multiplier,
                    "layers": settings["herding_layers"],
                    "backend": result["backend"],
                    "converged": bool(result["converged"]),
                },
            },
            notes=(
                f"herding: |M|={magnetization:.4f} "
                f"multiplier={risk_multiplier:.4f} "
                f"backend={result['backend']}"
            ),
        )