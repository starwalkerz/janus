"""Tests for the trade-intent verifier."""

import pytest

from janus.contracts import (
    Action,
    AgopMode,
    AgopResult,
    ContractViolation,
    RiskBound,
    StrategyName,
    TradeIntent,
    verify_trade_intent,
)


def _sample_agop(
    verified: bool = True,
    ranking: tuple[str, ...] = ("LONG", "FLAT"),
) -> AgopResult:
    return AgopResult(
        mode=AgopMode.DBC,
        ranking=list(ranking),
        survivor_set=list(ranking),
        lower_confidence_bound={value: 1.0 for value in ranking},
        composite_score={value: 1.0 for value in ranking},
        topology_class={value: "T_A" for value in ranking},
        convergence_depth=1,
        capacity=2,
        number_of_weisfeiler_lehman_classes=2,
        contract_verified=verified,
    )


def _sample_risk(
    upper_bound: float = 0.05,
    toxic: bool = False,
) -> RiskBound:
    return RiskBound(upper_bound, 0.5, 1.0, toxic, "ok")


@verify_trade_intent
def _step(intent, agop_result, risk_bound):
    return intent, agop_result, risk_bound, StrategyName.CONSERVATIVE


def test_invariant_i1_closed_action_set():
    bad_intent = TradeIntent(
        Action.SHORT, 0.02, "x", AgopMode.DBC, StrategyName.CONSERVATIVE
    )
    result = _step(bad_intent, _sample_agop(), _sample_risk())
    assert result.action is Action.FLAT
    assert result.position_size == 0.0


def test_invariant_i2_bounded_size():
    bad_intent = TradeIntent(
        Action.LONG, 0.50, "x", AgopMode.DBC, StrategyName.CONSERVATIVE
    )
    result = _step(
        bad_intent, _sample_agop(), _sample_risk(upper_bound=0.50)
    )
    assert result.position_size == 0.0


def test_invariant_i3_contract_supremacy():
    bad_intent = TradeIntent(
        Action.LONG, 0.02, "x", AgopMode.DBC, StrategyName.CONSERVATIVE
    )
    result = _step(
        bad_intent,
        _sample_agop(verified=False, ranking=()),
        _sample_risk(),
    )
    assert result.action is Action.FLAT
    assert result.contract_forced_flat is True


def test_invariant_i4_toxicity_supremacy():
    bad_intent = TradeIntent(
        Action.LONG, 0.02, "x", AgopMode.DBC, StrategyName.CONSERVATIVE
    )
    result = _step(
        bad_intent, _sample_agop(), _sample_risk(toxic=True)
    )
    assert result.action is Action.FLAT


def test_invariant_i5_downward_only():
    bad_intent = TradeIntent(
        Action.LONG, 0.08, "x", AgopMode.DBC, StrategyName.CONSERVATIVE
    )
    result = _step(
        bad_intent, _sample_agop(), _sample_risk(upper_bound=0.05)
    )
    assert result.position_size == 0.0


def test_strict_mode_raises():
    bad_intent = TradeIntent(
        Action.SHORT, 0.02, "x", AgopMode.DBC, StrategyName.CONSERVATIVE
    )
    with pytest.raises(ContractViolation):
        _step(
            bad_intent,
            _sample_agop(),
            _sample_risk(),
            strict=True,
        )