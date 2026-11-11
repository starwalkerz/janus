"""Tests for the risk bound computation."""

from janus.config import CONSERVATIVE
from janus.contracts import (
    Action,
    AgopMode,
    AgopResult,
    MarketSnapshot,
)
from janus.risk import bound, kelly_fraction, toxic_flow


def _sample_agop() -> AgopResult:
    return AgopResult(
        mode=AgopMode.DBC,
        ranking=["LONG", "FLAT"],
        survivor_set=["LONG", "FLAT"],
        lower_confidence_bound={"LONG": 1.0, "FLAT": 1.0},
        composite_score={"LONG": 1.0, "FLAT": 1.0},
        topology_class={"LONG": "T_A", "FLAT": "T_B"},
        convergence_depth=1,
        capacity=2,
        number_of_weisfeiler_lehman_classes=2,
        contract_verified=True,
    )


def _sample_snapshot(order_flow_imbalance: float = 0.0) -> MarketSnapshot:
    return MarketSnapshot(
        symbol="X",
        price=100.0,
        expected_return=0.004,
        realized_volatility=0.012,
        slippage=2.0,
        slippage_maximum=20.0,
        venue_risk=0.2,
        signal_agreement=0.6,
        order_flow_imbalance=order_flow_imbalance,
    )


def test_kelly_formula():
    assert abs(kelly_fraction(0.6, 1.0) - 0.2) < 1e-12
    assert kelly_fraction(0.4, 1.0) == 0.0


def test_toxic_direction():
    assert toxic_flow(
        _sample_snapshot(order_flow_imbalance=0.5),
        Action.SHORT,
        0.15,
    )
    assert not toxic_flow(
        _sample_snapshot(order_flow_imbalance=0.5),
        Action.LONG,
        0.15,
    )


def test_bound_is_capped():
    result = bound(
        _sample_snapshot(),
        _sample_agop(),
        1.0,
        CONSERVATIVE,
        Action.LONG,
    )
    assert result.upper_position_size <= CONSERVATIVE.position_cap