"""Tests for the AGOP bridge and feature construction."""

from janus.agop_bridge import _build_graph
from janus.contracts import MarketSnapshot
from janus.features import build_axes


def test_graph_mutual_exclusion():
    graph = _build_graph(["LONG", "FLAT", "SHORT"])
    assert graph["LONG"]["SHORT"]["sign"] == -1
    assert graph["SHORT"]["LONG"]["sign"] == -1
    assert graph["FLAT"]["LONG"]["sign"] == 1


def test_axes_are_bounded():
    snapshot = MarketSnapshot(
        symbol="X",
        price=100.0,
        expected_return=0.01,
        realized_volatility=0.02,
        slippage=2.0,
        slippage_maximum=10.0,
        venue_risk=0.3,
        signal_agreement=0.7,
        order_flow_imbalance=0.1,
    )
    axes = build_axes(snapshot)
    for axis_name, axis_values in axes.items():
        for action_name, value in axis_values.items():
            assert 0.0 <= value <= 1.0, (
                f"{axis_name}[{action_name}]={value} out of bounds"
            )