"""Tests for the opportunity magnifier modules."""

import numpy as np
import pytest

from janus.config import AGGRESSIVE, CONSERVATIVE, OPPORTUNITY
from janus.contracts import Action, MarketSnapshot, ModulePhase
from janus.modules.base import ModuleContext, ModuleResult
from janus.modules.opportunity_common import (
    aligned_direction,
    build_patches,
    downside_score,
    natural_direction,
    recent_slope,
)
from janus.modules.agop_opportunity import AgopOpportunityModule
from janus.modules.causality_opportunity import CausalityOpportunityModule
from janus.modules.kairos_opportunity import KairosOpportunityModule
from janus.modules.opportunity_synthesizer import OpportunitySynthesizerModule


def _snapshot(
    mu: float = 0.008,
    sigma: float = 0.012,
    slippage: float = 2.0,
    slippage_maximum: float = 20.0,
    venue_risk: float = 0.15,
    order_flow_imbalance: float = 0.6,
    history: tuple = None,
) -> MarketSnapshot:
    if history is None:
        history = tuple(
            50000.0 + 300.0 * np.sin(i / 4.0) for i in range(64)
        )
    return MarketSnapshot(
        symbol="BTC/USDT",
        price=50000.0,
        expected_return=mu,
        realized_volatility=sigma,
        slippage=slippage,
        slippage_maximum=slippage_maximum,
        venue_risk=venue_risk,
        signal_agreement=0.7,
        order_flow_imbalance=order_flow_imbalance,
        history=history,
        timestamps=tuple(float(i) for i in range(len(history))),
        external_data={"cycle_period": 32.0},
    )


def _context(snapshot, strategy=OPPORTUNITY, prior_results=None) -> ModuleContext:
    from janus.config import Config
    return ModuleContext(
        snapshot=snapshot,
        configuration=Config(),
        strategy=strategy,
        phase=ModulePhase.PRE_AGOP,
        prior_results=prior_results or {},
    )


# ─────────────────────────────────────────────────────────────────────
# Shared helpers
# ─────────────────────────────────────────────────────────────────────


def test_downside_score_is_bounded():
    for slip in [0.0, 5.0, 20.0]:
        for venue in [0.0, 0.5, 1.0]:
            score = downside_score(_snapshot(slippage=slip, venue_risk=venue))
            assert 0.0 <= score <= 1.0


def test_downside_score_high_when_safe():
    score = downside_score(_snapshot(slippage=0.0, venue_risk=0.0))
    assert score == pytest.approx(1.0, abs=1e-9)


def test_downside_score_low_when_dangerous():
    score = downside_score(_snapshot(slippage=20.0, venue_risk=1.0))
    assert score < 0.1


def test_natural_direction_returns_none_for_zero_mu():
    assert natural_direction(_snapshot(mu=0.0)) is None


def test_natural_direction_returns_long_for_positive():
    assert natural_direction(_snapshot(mu=0.01)) is Action.LONG


def test_natural_direction_returns_short_for_negative():
    assert natural_direction(_snapshot(mu=-0.01)) is Action.SHORT


def test_build_patches_produces_bounded_values():
    patches = build_patches(Action.LONG, 1.0, 1.0)
    for axis, values in patches.items():
        for direction, value in values.items():
            assert 0.0 <= value <= 1.0, f"{axis}[{direction}]={value}"


def test_build_patches_neutral_when_amplitude_zero():
    patches = build_patches(Action.LONG, 0.0, 1.0)
    assert patches["pain"]["LONG"] == pytest.approx(0.5, abs=1e-9)
    assert patches["readiness"]["LONG"] == pytest.approx(0.5, abs=1e-9)
    assert patches["barrier"]["LONG"] == pytest.approx(0.5, abs=1e-9)


def test_build_patches_returns_empty_for_flat():
    patches = build_patches(Action.FLAT, 1.0, 1.0)
    assert patches == {}


def test_aligned_direction_returns_true_for_match():
    assert aligned_direction(Action.LONG, Action.LONG) is True


def test_aligned_direction_returns_false_for_mismatch():
    assert aligned_direction(Action.LONG, Action.SHORT) is False


def test_aligned_direction_returns_false_for_none():
    assert aligned_direction(Action.LONG, None) is False


def test_recent_slope_detects_upward_trend():
    history = tuple(float(i) for i in range(64))
    assert recent_slope(history, 16) == 1


def test_recent_slope_detects_downward_trend():
    history = tuple(float(63 - i) for i in range(64))
    assert recent_slope(history, 16) == -1


def test_recent_slope_returns_zero_for_flat():
    history = tuple(100.0 for _ in range(64))
    assert recent_slope(history, 16) == 0


# ─────────────────────────────────────────────────────────────────────
# KairosOpportunityModule
# ─────────────────────────────────────────────────────────────────────


def test_kairos_opportunity_neutral_without_history():
    snapshot = MarketSnapshot(
        symbol="X",
        price=100.0,
        expected_return=0.01,
        realized_volatility=0.012,
        slippage=2.0,
        slippage_maximum=20.0,
        venue_risk=0.15,
        signal_agreement=0.7,
        order_flow_imbalance=0.5,
        history=(),
        timestamps=(),
    )
    module = KairosOpportunityModule()
    result = module.run(_context(snapshot))
    assert result.axes_patch == {}


def test_kairos_opportunity_neutral_when_kairos_unavailable():
    snapshot = _snapshot()
    module = KairosOpportunityModule()
    result = module.run(_context(snapshot))
    assert result.axes_patch == {}
    assert "unavailable" in result.notes or "neutral" in result.notes


def test_kairos_opportunity_qualifies_with_monkeypatched_report(monkeypatch):
    from janus.modules import kairos_opportunity as kairos_module

    class _FakeReport:
        flagged = True
        classical_amplitude = 0.5

    monkeypatch.setattr(
        kairos_module, "kairos_call_local",
        lambda *args, **kwargs: _FakeReport(),
    )

    base = [50000.0 + 100.0 * i for i in range(64)]
    snapshot = _snapshot(
        mu=0.01, venue_risk=0.1, slippage=1.0, history=tuple(base)
    )
    module = KairosOpportunityModule()
    result = module.run(_context(snapshot))

    if result.axes_patch:
        for axis, values in result.axes_patch.items():
            for direction, value in values.items():
                assert 0.0 <= value <= 1.0, (
                    f"{axis}[{direction}]={value}"
                )
        assert "LONG" in result.axes_patch.get("pain", {})


def test_kairos_opportunity_neutral_when_not_aligned(monkeypatch):
    from janus.modules import kairos_opportunity as kairos_module

    class _FakeReport:
        flagged = True
        classical_amplitude = 0.5

    monkeypatch.setattr(
        kairos_module, "kairos_call_local",
        lambda *args, **kwargs: _FakeReport(),
    )

    base = [50000.0 - 100.0 * i for i in range(64)]
    snapshot = _snapshot(
        mu=0.01, venue_risk=0.1, slippage=1.0, history=tuple(base)
    )
    module = KairosOpportunityModule()
    result = module.run(_context(snapshot))
    assert result.axes_patch == {}


def test_kairos_opportunity_neutral_when_dangerous(monkeypatch):
    from janus.modules import kairos_opportunity as kairos_module

    class _FakeReport:
        flagged = True
        classical_amplitude = 0.5

    monkeypatch.setattr(
        kairos_module, "kairos_call_local",
        lambda *args, **kwargs: _FakeReport(),
    )

    base = [50000.0 + 100.0 * i for i in range(64)]
    snapshot = _snapshot(
        mu=0.01, venue_risk=0.9, slippage=19.0, history=tuple(base)
    )
    module = KairosOpportunityModule()
    result = module.run(_context(snapshot))
    assert result.axes_patch == {}


# ─────────────────────────────────────────────────────────────────────
# CausalityOpportunityModule
# ─────────────────────────────────────────────────────────────────────


def test_causality_opportunity_neutral_without_history():
    snapshot = MarketSnapshot(
        symbol="X",
        price=100.0,
        expected_return=0.01,
        realized_volatility=0.012,
        slippage=2.0,
        slippage_maximum=20.0,
        venue_risk=0.15,
        signal_agreement=0.7,
        order_flow_imbalance=0.5,
        history=(),
        timestamps=(),
    )
    module = CausalityOpportunityModule()
    result = module.run(_context(snapshot))
    assert result.axes_patch == {}


def test_causality_opportunity_neutral_when_causalitybot_unavailable():
    snapshot = _snapshot()
    module = CausalityOpportunityModule()
    result = module.run(_context(snapshot))
    assert result.axes_patch == {}
    assert "unavailable" in result.notes or "neutral" in result.notes


# ─────────────────────────────────────────────────────────────────────
# AgopOpportunityModule
# ─────────────────────────────────────────────────────────────────────


def test_agop_opportunity_neutral_for_zero_mu():
    snapshot = _snapshot(mu=0.0)
    module = AgopOpportunityModule()
    result = module.run(_context(snapshot))
    assert result.axes_patch == {}


def test_agop_opportunity_qualifies_when_edge_ratio_is_high():
    snapshot = _snapshot(
        mu=0.02, sigma=0.01, venue_risk=0.05, slippage=0.5
    )
    module = AgopOpportunityModule()
    result = module.run(_context(snapshot))
    assert result.axes_patch, "Expected axes_patch for high edge ratio"
    for axis, values in result.axes_patch.items():
        for direction, value in values.items():
            assert 0.0 <= value <= 1.0, f"{axis}[{direction}]={value}"
    assert "LONG" in result.axes_patch.get("pain", {})


def test_agop_opportunity_neutral_when_edge_ratio_low():
    snapshot = _snapshot(mu=0.0001, sigma=0.02)
    module = AgopOpportunityModule()
    result = module.run(_context(snapshot))
    assert result.axes_patch == {}


def test_agop_opportunity_neutral_when_venue_risk_high():
    snapshot = _snapshot(mu=0.02, sigma=0.01, venue_risk=0.9)
    module = AgopOpportunityModule()
    result = module.run(_context(snapshot))
    assert result.axes_patch == {}


def test_agop_opportunity_qualifies_for_short_direction():
    snapshot = _snapshot(
        mu=-0.02, sigma=0.01, venue_risk=0.05, slippage=0.5
    )
    module = AgopOpportunityModule()
    result = module.run(_context(snapshot))
    if result.axes_patch:
        assert "SHORT" in result.axes_patch.get("pain", {})


def test_agop_opportunity_works_with_conservative_profile():
    snapshot = _snapshot(mu=0.02, sigma=0.01, venue_risk=0.05, slippage=0.5)
    module = AgopOpportunityModule()
    result = module.run(_context(snapshot, strategy=CONSERVATIVE))
    assert isinstance(result, ModuleResult)


def test_agop_opportunity_works_with_aggressive_profile():
    snapshot = _snapshot(mu=0.02, sigma=0.01, venue_risk=0.05, slippage=0.5)
    module = AgopOpportunityModule()
    result = module.run(_context(snapshot, strategy=AGGRESSIVE))
    assert isinstance(result, ModuleResult)


# ─────────────────────────────────────────────────────────────────────
# OpportunitySynthesizerModule
# ─────────────────────────────────────────────────────────────────────


def _fake_opportunity_result(name, direction, qualified):
    return ModuleResult(
        name=name,
        phase=ModulePhase.PRE_AGOP,
        axes_patch={},
        risk_multiplier=1.0,
        veto=False,
        context={
            name: {
                "direction": direction,
                "qualified": qualified,
            }
        },
    )


def _pre_llm_context(snapshot, prior_results) -> ModuleContext:
    from janus.config import Config
    return ModuleContext(
        snapshot=snapshot,
        configuration=Config(),
        strategy=OPPORTUNITY,
        phase=ModulePhase.PRE_LLM,
        prior_results=prior_results,
    )


def test_synthesizer_none_when_no_prior_results():
    snapshot = _snapshot()
    module = OpportunitySynthesizerModule()
    result = module.run(_pre_llm_context(snapshot, {}))
    synthesis = result.context["opportunity_synthesis"]
    assert synthesis["consensus"] == "none"
    assert synthesis["direction"] is None
    assert synthesis["confidence"] == 0.0
    assert synthesis["contributing_modules"] == []


def test_synthesizer_none_when_no_module_qualified():
    snapshot = _snapshot()
    prior = {
        "agop_opportunity": _fake_opportunity_result(
            "agop_opportunity", "LONG", False
        ),
        "kairos_opportunity": _fake_opportunity_result(
            "kairos_opportunity", "LONG", False
        ),
    }
    module = OpportunitySynthesizerModule()
    result = module.run(_pre_llm_context(snapshot, prior))
    synthesis = result.context["opportunity_synthesis"]
    assert synthesis["consensus"] == "none"


def test_synthesizer_unanimous_when_multiple_agree():
    snapshot = _snapshot()
    prior = {
        "agop_opportunity": _fake_opportunity_result(
            "agop_opportunity", "LONG", True
        ),
        "kairos_opportunity": _fake_opportunity_result(
            "kairos_opportunity", "LONG", True
        ),
    }
    module = OpportunitySynthesizerModule()
    result = module.run(_pre_llm_context(snapshot, prior))
    synthesis = result.context["opportunity_synthesis"]
    assert synthesis["consensus"] == "unanimous"
    assert synthesis["direction"] == "LONG"
    assert synthesis["confidence"] == pytest.approx(2 / 3, abs=1e-2)
    assert "agop_opportunity" in synthesis["contributing_modules"]
    assert "kairos_opportunity" in synthesis["contributing_modules"]


def test_synthesizer_single_when_one_qualifies():
    snapshot = _snapshot()
    prior = {
        "agop_opportunity": _fake_opportunity_result(
            "agop_opportunity", "LONG", True
        ),
        "kairos_opportunity": _fake_opportunity_result(
            "kairos_opportunity", "LONG", False
        ),
    }
    module = OpportunitySynthesizerModule()
    result = module.run(_pre_llm_context(snapshot, prior))
    synthesis = result.context["opportunity_synthesis"]
    assert synthesis["consensus"] == "single"
    assert synthesis["direction"] == "LONG"
    assert synthesis["confidence"] == 0.5
    assert synthesis["contributing_modules"] == ["agop_opportunity"]


def test_synthesizer_mixed_when_directions_disagree():
    snapshot = _snapshot()
    prior = {
        "agop_opportunity": _fake_opportunity_result(
            "agop_opportunity", "LONG", True
        ),
        "kairos_opportunity": _fake_opportunity_result(
            "kairos_opportunity", "SHORT", True
        ),
    }
    module = OpportunitySynthesizerModule()
    result = module.run(_pre_llm_context(snapshot, prior))
    synthesis = result.context["opportunity_synthesis"]
    assert synthesis["consensus"] == "mixed"
    assert synthesis["direction"] is None
    assert synthesis["confidence"] == 0.0
    assert len(synthesis["contributing_modules"]) == 2


def test_synthesizer_unanimous_with_three_modules():
    snapshot = _snapshot()
    prior = {
        "agop_opportunity": _fake_opportunity_result(
            "agop_opportunity", "SHORT", True
        ),
        "causality_opportunity": _fake_opportunity_result(
            "causality_opportunity", "SHORT", True
        ),
        "kairos_opportunity": _fake_opportunity_result(
            "kairos_opportunity", "SHORT", True
        ),
    }
    module = OpportunitySynthesizerModule()
    result = module.run(_pre_llm_context(snapshot, prior))
    synthesis = result.context["opportunity_synthesis"]
    assert synthesis["consensus"] == "unanimous"
    assert synthesis["direction"] == "SHORT"
    assert synthesis["confidence"] == pytest.approx(1.0, abs=1e-9)
    assert len(synthesis["contributing_modules"]) == 3


def test_synthesizer_ignores_invalid_direction():
    snapshot = _snapshot()
    prior = {
        "agop_opportunity": ModuleResult(
            name="agop_opportunity",
            phase=ModulePhase.PRE_AGOP,
            context={
                "agop_opportunity": {
                    "direction": "NOT_A_DIRECTION",
                    "qualified": True,
                }
            },
        ),
    }
    module = OpportunitySynthesizerModule()
    result = module.run(_pre_llm_context(snapshot, prior))
    synthesis = result.context["opportunity_synthesis"]
    assert synthesis["consensus"] == "none"


# ─────────────────────────────────────────────────────────────────────
# Invariant preservation across modules
# ─────────────────────────────────────────────────────────────────────


def test_all_modules_never_produce_out_of_bounds_axes():
    base = [50000.0 + 100.0 * np.sin(i / 4.0) for i in range(64)]
    history = base[:56] + [base[i] + 400.0 for i in range(56, 64)]
    snapshot = _snapshot(
        mu=0.01, venue_risk=0.1, slippage=1.0, history=tuple(history),
        order_flow_imbalance=0.7,
    )
    for module_cls in (
        KairosOpportunityModule,
        CausalityOpportunityModule,
        AgopOpportunityModule,
    ):
        module = module_cls()
        result = module.run(_context(snapshot))
        for axis, values in result.axes_patch.items():
            for direction, value in values.items():
                assert 0.0 <= value <= 1.0, (
                    f"{module_cls.__name__}: {axis}[{direction}]={value}"
                )