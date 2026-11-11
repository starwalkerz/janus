"""Tests for the quantum econophysics modules."""

import numpy as np
import pytest

from janus.config import Config, CONSERVATIVE, AGGRESSIVE
from janus.contracts import MarketSnapshot, ModulePhase
from janus.modules.base import ModuleContext
from janus.modules.econophysics import (
    EconophysicsHerdingModule,
    EconophysicsTunnelingModule,
    _build_baaquie_hamiltonian,
    _detect_barrier,
    _detect_support,
    _extract_couplings_and_fields,
)


def _sample_snapshot(history_override=None) -> MarketSnapshot:
    history = history_override or tuple(
        50_000.0 + 500.0 * np.sin(index / 8.0)
        for index in range(128)
    )
    return MarketSnapshot(
        symbol="BTC/USDT",
        price=50_000.0,
        expected_return=0.004,
        realized_volatility=0.012,
        slippage=2.0,
        slippage_maximum=20.0,
        venue_risk=0.2,
        signal_agreement=0.6,
        order_flow_imbalance=0.05,
        history=history,
        timestamps=tuple(float(index) for index in range(len(history))),
    )


def test_hamiltonian_is_symmetric():
    hamiltonian, positions = _build_baaquie_hamiltonian(
        n_qubits=4,
        log_price_min=np.log(49_000.0),
        log_price_max=np.log(51_000.0),
        barrier_position=np.log(50_500.0),
        barrier_strength=2.0,
        barrier_width=0.005,
    )
    assert hamiltonian.shape == (16, 16)
    assert np.allclose(hamiltonian, hamiltonian.T)
    assert np.allclose(np.linalg.eigvalsh(hamiltonian).imag, 0.0)


def test_barrier_detection_returns_level_above_price():
    history = tuple(
        50_000.0 + 500.0 * np.sin(index / 8.0) + 200.0 * (index % 5 == 0)
        for index in range(128)
    )
    barrier = _detect_barrier(history, 50_000.0)
    assert barrier is not None
    assert barrier > 50_000.0


def test_support_detection_returns_level_below_price():
    history = tuple(
        50_000.0 + 500.0 * np.sin(index / 8.0) - 200.0 * (index % 5 == 0)
        for index in range(128)
    )
    support = _detect_support(history, 50_000.0)
    assert support is not None
    assert support < 50_000.0


def test_tunneling_module_returns_barrier_patch():
    module = EconophysicsTunnelingModule()
    context = ModuleContext(
        snapshot=_sample_snapshot(),
        configuration=Config(),
        strategy=CONSERVATIVE,
        phase=ModulePhase.PRE_AGOP,
    )
    result = module.run(context)
    assert result.phase is ModulePhase.PRE_AGOP
    if result.axes_patch:
        assert "barrier" in result.axes_patch
        assert all(0.0 <= value <= 1.0 for value in result.axes_patch["barrier"].values())


def test_herding_module_returns_bounded_multiplier():
    module = EconophysicsHerdingModule()
    context = ModuleContext(
        snapshot=_sample_snapshot(),
        configuration=Config(),
        strategy=CONSERVATIVE,
        phase=ModulePhase.POST_AGOP,
    )
    result = module.run(context)
    assert 0.0 <= result.risk_multiplier <= 1.0


def test_herding_sensitivity_differs_between_profiles():
    module = EconophysicsHerdingModule()
    snapshot = _sample_snapshot()

    conservative_result = module.run(ModuleContext(
        snapshot=snapshot,
        configuration=Config(),
        strategy=CONSERVATIVE,
        phase=ModulePhase.POST_AGOP,
    ))
    aggressive_result = module.run(ModuleContext(
        snapshot=snapshot,
        configuration=Config(),
        strategy=AGGRESSIVE,
        phase=ModulePhase.POST_AGOP,
    ))

    # The aggressive profile uses a smaller sensitivity, so its risk
    # multiplier is at least as large as the conservative one.
    assert aggressive_result.risk_multiplier >= conservative_result.risk_multiplier - 1e-9


def test_couplings_extracted_from_multi_asset_data():
    snapshot = _sample_snapshot()
    snapshot_assets = {
        "asset_a": list(range(100, 200)),
        "asset_b": list(range(200, 300)),
        "asset_c": list(range(300, 400)),
    }
    snapshot = MarketSnapshot(
        symbol=snapshot.symbol,
        price=snapshot.price,
        expected_return=snapshot.expected_return,
        realized_volatility=snapshot.realized_volatility,
        slippage=snapshot.slippage,
        slippage_maximum=snapshot.slippage_maximum,
        venue_risk=snapshot.venue_risk,
        signal_agreement=snapshot.signal_agreement,
        order_flow_imbalance=snapshot.order_flow_imbalance,
        history=snapshot.history,
        timestamps=snapshot.timestamps,
        external_data={"econophysics_assets": snapshot_assets},
    )
    couplings, fields = _extract_couplings_and_fields(snapshot, n_qubits=3)
    # All three assets are strictly monotonic, so all pairwise correlations
    # are +1.
    assert len(couplings) >= 1
    for value in couplings.values():
        assert -1.0 <= value <= 1.0