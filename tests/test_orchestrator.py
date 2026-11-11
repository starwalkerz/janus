"""Tests for the orchestrator pipeline."""

from janus.config import Config
from janus.contracts import MarketSnapshot
from janus.orchestrator import Orchestrator


def _sample_snapshot() -> MarketSnapshot:
    return MarketSnapshot(
        symbol="X",
        price=100.0,
        expected_return=0.004,
        realized_volatility=0.012,
        slippage=2.0,
        slippage_maximum=20.0,
        venue_risk=0.2,
        signal_agreement=0.6,
        order_flow_imbalance=0.05,
        history=tuple(0.01 for _ in range(32)),
        timestamps=tuple(float(index) for index in range(32)),
    )


def test_tick_is_flat_when_agop_unavailable(temporary_directory):
    configuration = Config()
    configuration.agop_local_path = str(temporary_directory)
    orchestrator = Orchestrator(configuration)
    record = orchestrator.tick(_sample_snapshot())
    assert record["intent"]["action"] == "FLAT"
    assert record["intent"]["position_size"] == 0.0


def test_tick_is_deterministic(temporary_directory):
    configuration = Config()
    configuration.agop_local_path = str(temporary_directory)
    first_record = Orchestrator(configuration).tick(_sample_snapshot())
    second_record = Orchestrator(configuration).tick(_sample_snapshot())
    assert first_record["intent"] == second_record["intent"]