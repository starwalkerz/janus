"""
quantum_runner.py — Qiskit/IQM execution for the econophysics module.

Three backends in order of preference:

  1. IQM Resonance via iqm.qiskit_iqm.IQMProvider. Requires an API token,
     a server URL, and an event-triggered tick. When the event gate is
     False (see quantum_trigger.py), IQM is skipped even if a token is
     present.

  2. Qiskit Aer statevector simulator. Used when Qiskit is installed and
     the IQM path is either unavailable or gated off.

  3. NumPy exact evolution via scipy.sparse.linalg.expm_multiply. Used
     when neither Qiskit nor IQM is available.

Every entry returns a dict with a `backend` key identifying which path
was taken and an `event_triggered` key recording whether the event gate
permitted the IQM path on this tick.
"""

from __future__ import annotations

import math
from typing import Optional

import numpy as np


def _try_import_qiskit():
    try:
        from qiskit import QuantumCircuit, transpile
        from qiskit.circuit.library import PauliEvolutionGate
        from qiskit.synthesis import LieTrotter, SuzukiTrotter
        from qiskit.quantum_info import SparsePauliOp, Statevector
        return {
            "QuantumCircuit": QuantumCircuit,
            "transpile": transpile,
            "PauliEvolutionGate": PauliEvolutionGate,
            "LieTrotter": LieTrotter,
            "SuzukiTrotter": SuzukiTrotter,
            "SparsePauliOp": SparsePauliOp,
            "Statevector": Statevector,
        }
    except ImportError:
        return None


def _try_import_aer():
    try:
        from qiskit_aer import AerSimulator
        return AerSimulator
    except ImportError:
        return None


def _try_import_iqm():
    try:
        from iqm.qiskit_iqm import IQMProvider
        return IQMProvider
    except ImportError:
        return None


# ─────────────────────────────────────────────────────────────────────
# Tunneling circuit
# ─────────────────────────────────────────────────────────────────────


def run_tunneling(
    hamiltonian_matrix: np.ndarray,
    initial_index: int,
    n_qubits: int,
    evolution_time: float,
    trotter_steps: int = 3,
    shots: int = 2000,
    iqm_token: Optional[str] = None,
    iqm_server: str = "https://resonance.iqm.tech",
    iqm_backend: Optional[str] = None,
    event_triggered: bool = True,
) -> dict:
    """Evolve `initial_index` under `hamiltonian_matrix`.

    The IQM path is attempted only when `event_triggered` is True and
    `iqm_token` is set. When `event_triggered` is False, IQM is skipped
    entirely and the circuit runs on Aer or classical-exact.
    """
    dim = 1 << n_qubits
    if hamiltonian_matrix.shape != (dim, dim):
        raise ValueError(
            f"hamiltonian shape {hamiltonian_matrix.shape} does not match "
            f"2^{n_qubits} = {dim}"
        )

    qiskit_modules = _try_import_qiskit()

    # Path 1: IQM Resonance — only when event_triggered and iqm_token is set
    if event_triggered and iqm_token and qiskit_modules is not None:
        iqm_module = _try_import_iqm()
        if iqm_module is not None:
            try:
                return _run_tunneling_iqm(
                    qiskit_modules, iqm_module, hamiltonian_matrix,
                    initial_index, n_qubits, evolution_time, trotter_steps,
                    shots, iqm_token, iqm_server, iqm_backend,
                )
            except Exception:
                pass

    # Path 2: Qiskit Aer
    if qiskit_modules is not None:
        aer_module = _try_import_aer()
        if aer_module is not None:
            try:
                result = _run_tunneling_aer(
                    qiskit_modules, aer_module, hamiltonian_matrix,
                    initial_index, n_qubits, evolution_time, trotter_steps,
                    shots,
                )
                result["event_triggered"] = event_triggered
                return result
            except Exception:
                pass

    # Path 3: Classical exact
    result = _run_tunneling_classical(
        hamiltonian_matrix, initial_index, n_qubits, evolution_time,
    )
    result["event_triggered"] = event_triggered
    return result


def _build_tunneling_circuit(
    qiskit_modules: dict,
    hamiltonian_matrix: np.ndarray,
    initial_index: int,
    n_qubits: int,
    evolution_time: float,
    trotter_steps: int,
):
    sp = qiskit_modules["SparsePauliOp"].from_operator(hamiltonian_matrix)
    if np.max(np.abs(sp.coeffs.imag)) > 1e-9:
        raise ValueError("hamiltonian must be real-symmetric")
    sp = qiskit_modules["SparsePauliOp"](
        sp.paulis, sp.coeffs.real.astype(float)
    )

    evolution_gate = qiskit_modules["PauliEvolutionGate"](
        sp,
        time=evolution_time,
        synthesis=qiskit_modules["LieTrotter"](reps=trotter_steps),
    )

    circuit = qiskit_modules["QuantumCircuit"](n_qubits)
    for qubit in range(n_qubits):
        if not (initial_index >> qubit) & 1:
            circuit.x(qubit)
    circuit.append(evolution_gate, range(n_qubits))
    circuit.measure_all()
    return circuit


def _run_tunneling_iqm(
    qiskit_modules, iqm_module, hamiltonian_matrix, initial_index,
    n_qubits, evolution_time, trotter_steps, shots,
    iqm_token, iqm_server, iqm_backend,
) -> dict:
    provider = iqm_module(iqm_server, token=iqm_token)
    backend = (
        provider.get_backend(iqm_backend)
        if iqm_backend
        else provider.get_backend()
    )

    circuit = _build_tunneling_circuit(
        qiskit_modules, hamiltonian_matrix, initial_index,
        n_qubits, evolution_time, trotter_steps,
    )
    transpiled = qiskit_modules["transpile"](circuit, backend)
    job = backend.run(transpiled, shots=shots)
    counts = job.result().get_counts()

    probabilities = np.zeros(1 << n_qubits, dtype=float)
    total = sum(counts.values())
    for bitstring, count in counts.items():
        index = int(bitstring.replace(" ", ""), 2)
        probabilities[index] = count / total

    return {
        "backend": f"iqm:{getattr(backend, 'name', 'iqm')}",
        "probabilities": probabilities,
        "shots": shots,
        "event_triggered": True,
    }


def _run_tunneling_aer(
    qiskit_modules, aer_module, hamiltonian_matrix, initial_index,
    n_qubits, evolution_time, trotter_steps, shots,
) -> dict:
    simulator = aer_module()
    circuit = _build_tunneling_circuit(
        qiskit_modules, hamiltonian_matrix, initial_index,
        n_qubits, evolution_time, trotter_steps,
    )
    transpiled = qiskit_modules["transpile"](circuit, simulator)
    job = simulator.run(transpiled, shots=shots)
    counts = job.result().get_counts()

    probabilities = np.zeros(1 << n_qubits, dtype=float)
    total = sum(counts.values())
    for bitstring, count in counts.items():
        index = int(bitstring.replace(" ", ""), 2)
        probabilities[index] = count / total

    return {
        "backend": "qiskit-aer",
        "probabilities": probabilities,
        "shots": shots,
    }


def _run_tunneling_classical(
    hamiltonian_matrix, initial_index, n_qubits, evolution_time,
) -> dict:
    from scipy.sparse.linalg import expm_multiply
    from scipy.sparse import csr_matrix

    initial = np.zeros(1 << n_qubits, dtype=complex)
    initial[initial_index] = 1.0

    evolved = expm_multiply(
        -1j * evolution_time * csr_matrix(hamiltonian_matrix),
        initial,
    )
    probabilities = np.abs(evolved) ** 2
    probabilities = probabilities / (probabilities.sum() + 1e-300)

    return {
        "backend": "classical-exact",
        "probabilities": probabilities,
        "shots": 0,
    }


# ─────────────────────────────────────────────────────────────────────
# QAOA herding circuit
# ─────────────────────────────────────────────────────────────────────


def run_qaoa_herding(
    couplings: dict[tuple[int, int], float],
    fields: dict[int, float],
    n_qubits: int,
    layers: int = 1,
    shots: int = 4000,
    iqm_token: Optional[str] = None,
    iqm_server: str = "https://resonance.iqm.tech",
    iqm_backend: Optional[str] = None,
    optimizer_iterations: int = 60,
    event_triggered: bool = True,
) -> dict:
    """Run QAOA on the Ising cost Hamiltonian.

    The IQM path is attempted only when `event_triggered` is True and
    `iqm_token` is set.
    """
    qiskit_modules = _try_import_qiskit()

    if event_triggered and iqm_token and qiskit_modules is not None:
        iqm_module = _try_import_iqm()
        if iqm_module is not None:
            try:
                result = _run_qaoa(
                    couplings, fields, n_qubits, layers, shots,
                    optimizer_iterations, qiskit_modules, "iqm",
                    iqm_module, iqm_token, iqm_server, iqm_backend,
                )
                result["event_triggered"] = True
                return result
            except Exception:
                pass

    if qiskit_modules is not None:
        try:
            result = _run_qaoa(
                couplings, fields, n_qubits, layers, shots,
                optimizer_iterations, qiskit_modules, "aer",
                None, None, None, None,
            )
            result["event_triggered"] = event_triggered
            return result
        except Exception:
            pass

    result = _run_qaoa_classical(
        couplings, fields, n_qubits, layers, optimizer_iterations,
    )
    result["event_triggered"] = event_triggered
    return result


def _cost_expectation_from_probabilities(
    probabilities, couplings, fields, n_qubits,
) -> float:
    expectation = 0.0
    for index, probability in enumerate(probabilities):
        if probability == 0.0:
            continue
        z_values = np.array(
            [1.0 - 2.0 * ((index >> qubit) & 1)
             for qubit in range(n_qubits)]
        )
        cost = 0.0
        for (i, j), J_ij in couplings.items():
            cost -= J_ij * z_values[i] * z_values[j]
        for i, h_i in fields.items():
            cost -= h_i * z_values[i]
        expectation += probability * cost
    return float(expectation)


def _magnetization_from_probabilities(probabilities, n_qubits) -> float:
    magnetization_sum = 0.0
    for index, probability in enumerate(probabilities):
        if probability == 0.0:
            continue
        for qubit in range(n_qubits):
            z = 1.0 - 2.0 * ((index >> qubit) & 1)
            magnetization_sum += probability * z
    return float(magnetization_sum / n_qubits)


def _run_qaoa(
    couplings, fields, n_qubits, layers, shots,
    optimizer_iterations, qiskit_modules, mode,
    iqm_module, iqm_token, iqm_server, iqm_backend,
) -> dict:
    from scipy.optimize import minimize

    if mode == "iqm":
        provider = iqm_module(iqm_server, token=iqm_token)
        backend = (
            provider.get_backend(iqm_backend)
            if iqm_backend
            else provider.get_backend()
        )
    else:
        aer_module = _try_import_aer()
        if aer_module is None:
            raise RuntimeError("Aer not available")
        backend = aer_module()

    def build_circuit(parameters):
        circuit = qiskit_modules["QuantumCircuit"](n_qubits)
        circuit.h(range(n_qubits))
        for layer in range(layers):
            gamma = parameters[2 * layer]
            beta = parameters[2 * layer + 1]
            for (i, j), J_ij in couplings.items():
                circuit.rzz(2.0 * gamma * J_ij, i, j)
            for i, h_i in fields.items():
                circuit.rz(2.0 * gamma * h_i, i)
            for qubit in range(n_qubits):
                circuit.rx(2.0 * beta, qubit)
        circuit.measure_all()
        return circuit

    def cost_function(parameters):
        circuit = build_circuit(parameters)
        transpiled = qiskit_modules["transpile"](circuit, backend)
        job = backend.run(transpiled, shots=shots)
        counts = job.result().get_counts()
        probabilities = np.zeros(1 << n_qubits, dtype=float)
        total = sum(counts.values())
        for bitstring, count in counts.items():
            index = int(bitstring.replace(" ", ""), 2)
            probabilities[index] = count / total
        return _cost_expectation_from_probabilities(
            probabilities, couplings, fields, n_qubits,
        )

    initial_parameters = np.random.default_rng(42).uniform(
        -0.5, 0.5, size=2 * layers,
    )
    result = minimize(
        cost_function, initial_parameters, method="COBYLA",
        options={"maxiter": optimizer_iterations, "tol": 1e-3},
    )

    final_circuit = build_circuit(result.x)
    transpiled = qiskit_modules["transpile"](final_circuit, backend)
    job = backend.run(transpiled, shots=shots)
    counts = job.result().get_counts()
    probabilities = np.zeros(1 << n_qubits, dtype=float)
    total = sum(counts.values())
    for bitstring, count in counts.items():
        index = int(bitstring.replace(" ", ""), 2)
        probabilities[index] = count / total

    backend_name = (
        f"iqm:{getattr(backend, 'name', 'iqm')}" if mode == "iqm"
        else "qiskit-aer"
    )
    return {
        "backend": backend_name,
        "parameters": result.x.tolist(),
        "cost": float(result.fun),
        "magnetization": _magnetization_from_probabilities(
            probabilities, n_qubits,
        ),
        "probabilities": probabilities,
        "shots": shots,
        "converged": bool(result.success),
    }


def _run_qaoa_classical(
    couplings, fields, n_qubits, layers, optimizer_iterations,
) -> dict:
    from scipy.optimize import minimize
    from scipy.linalg import expm

    dim = 1 << n_qubits
    identity = np.eye(2, dtype=complex)
    pauli_x = np.array([[0, 1], [1, 0]], dtype=complex)
    pauli_z = np.array([[1, 0], [0, -1]], dtype=complex)

    def kron_operator(operator, position):
        result = np.array([[1.0]], dtype=complex)
        for qubit in range(n_qubits):
            result = np.kron(
                result, operator if qubit == position else identity,
            )
        return result

    z_operators = [kron_operator(pauli_z, q) for q in range(n_qubits)]
    x_operators = [kron_operator(pauli_x, q) for q in range(n_qubits)]

    h_cost = np.zeros((dim, dim), dtype=complex)
    for (i, j), J_ij in couplings.items():
        h_cost -= J_ij * (z_operators[i] @ z_operators[j])
    for i, h_i in fields.items():
        h_cost -= h_i * z_operators[i]

    h_mixer = sum(x_operators)

    def state(parameters):
        psi = np.ones(dim, dtype=complex) / np.sqrt(dim)
        for layer in range(layers):
            gamma = parameters[2 * layer]
            beta = parameters[2 * layer + 1]
            psi = expm(-1j * gamma * h_cost) @ psi
            psi = expm(-1j * beta * h_mixer) @ psi
        return psi

    def cost_function(parameters):
        psi = state(parameters)
        return float(np.real(psi.conj() @ h_cost @ psi))

    initial_parameters = np.random.default_rng(42).uniform(
        -0.5, 0.5, size=2 * layers,
    )
    result = minimize(
        cost_function, initial_parameters, method="COBYLA",
        options={"maxiter": optimizer_iterations, "tol": 1e-4},
    )

    final_state = state(result.x)
    probabilities = np.abs(final_state) ** 2

    return {
        "backend": "classical-exact",
        "parameters": result.x.tolist(),
        "cost": float(result.fun),
        "magnetization": _magnetization_from_probabilities(
            probabilities, n_qubits,
        ),
        "probabilities": probabilities,
        "shots": 0,
        "converged": bool(result.success),
    }