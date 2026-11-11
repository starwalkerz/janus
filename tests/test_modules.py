"""Module lifecycle, composition, and veto semantics."""

import pytest

from janus.config import Config, ModuleConfiguration
from janus.contracts import ModulePhase, MarketSnapshot
from janus.modules.base import Module, ModuleContext, ModuleResult
from janus.modules.registry import ModuleRegistry, validate_result


def _snapshot():
    return MarketSnapshot(
        symbol="BTC/USDT",
        price=100.0,
        expected_return=0.004,
        realized_volatility=0.012,
        slippage=2.0,
        slippage_maximum=20.0,
        venue_risk=0.2,
        signal_agreement=0.6,
        order_flow_imbalance=0.05,
        history=tuple(50_000.0 + index for index in range(64)),
        timestamps=tuple(float(index) for index in range(64)),
    )


class _VetoModule(Module):
    name = "veto_test"
    phase = ModulePhase.POST_AGOP

    def run(self, context):
        return ModuleResult(
            name=self.name, phase=self.phase, veto=True, notes="veto"
        )


class _HalfModule(Module):
    name = "half_test"
    phase = ModulePhase.POST_AGOP

    def run(self, context):
        return ModuleResult(
            name=self.name,
            phase=self.phase,
            risk_multiplier=0.5,
            notes="half",
        )


class _QuarterModule(Module):
    name = "quarter_test"
    phase = ModulePhase.POST_AGOP

    def run(self, context):
        return ModuleResult(
            name=self.name,
            phase=self.phase,
            risk_multiplier=0.25,
            notes="quarter",
        )


class _AxesPatchModule(Module):
    name = "axes_test"
    phase = ModulePhase.PRE_AGOP

    def run(self, context):
        return ModuleResult(
            name=self.name,
            phase=self.phase,
            axes_patch={"pain": {"LONG": 0.9, "SHORT": 0.1}},
            notes="patched",
        )


class _BrokenAxesModule(Module):
    name = "broken_axes"
    phase = ModulePhase.POST_AGOP

    def run(self, context):
        return ModuleResult(
            name=self.name,
            phase=self.phase,
            axes_patch={"pain": {"LONG": 0.9}},
            notes="illegal",
        )


def test_register_requires_name_and_phase():
    registry = ModuleRegistry()

    class _Bad(Module):
        pass

    with pytest.raises(TypeError):
        registry.register(_Bad())


def test_duplicate_registration_rejected():
    registry = ModuleRegistry()
    registry.register(_HalfModule())
    with pytest.raises(ValueError):
        registry.register(_HalfModule())


def test_phase_ordering_is_alphabetical():
    registry = ModuleRegistry()
    registry.register(_VetoModule())
    registry.register(_HalfModule())
    registry.register(_QuarterModule())
    names = [
        module.name
        for module in registry.all_by_phase(ModulePhase.POST_AGOP)
    ]
    assert names == sorted(names)


def test_validate_axes_patch_outside_pre_agop_raises():
    with pytest.raises(ValueError):
        validate_result(
            ModuleResult(
                name="x",
                phase=ModulePhase.POST_AGOP,
                axes_patch={"pain": {"LONG": 0.5}},
            )
        )


def test_validate_risk_multiplier_outside_unit_interval_raises():
    with pytest.raises(ValueError):
        validate_result(
            ModuleResult(
                name="x",
                phase=ModulePhase.POST_AGOP,
                risk_multiplier=1.5,
            )
        )
    with pytest.raises(ValueError):
        validate_result(
            ModuleResult(
                name="x",
                phase=ModulePhase.POST_AGOP,
                risk_multiplier=-0.1,
            )
        )


def test_validate_unknown_axis_raises():
    with pytest.raises(ValueError):
        validate_result(
            ModuleResult(
                name="x",
                phase=ModulePhase.PRE_AGOP,
                axes_patch={"nonexistent": {"LONG": 0.5}},
            )
        )


def test_validate_axis_value_outside_unit_interval_raises():
    with pytest.raises(ValueError):
        validate_result(
            ModuleResult(
                name="x",
                phase=ModulePhase.PRE_AGOP,
                axes_patch={"pain": {"LONG": 1.2}},
            )
        )


def test_broken_module_triggers_fail_closed_in_conservative_orchestrator():
    from janus.orchestrator import Orchestrator

    registry = ModuleRegistry()
    registry.register(_BrokenAxesModule())
    configuration = Config()
    configuration.agop_local_path = "/tmp/nonexistent"
    configuration.module_configurations = {
        "broken_axes": ModuleConfiguration(
            enabled=True, on_error="fail_closed"
        )
    }

    orchestrator = Orchestrator(configuration, registry=registry)
    record = orchestrator.tick(_snapshot())
    assert record["intent"]["action"] == "FLAT"
    assert record["intent"]["vetoed"] is True


def test_disabled_module_is_skipped():
    from janus.orchestrator import Orchestrator

    registry = ModuleRegistry()
    registry.register(_VetoModule())
    configuration = Config()
    configuration.agop_local_path = "/tmp/nonexistent"
    configuration.module_configurations = {
        "veto_test": ModuleConfiguration(enabled=False)
    }

    orchestrator = Orchestrator(configuration, registry=registry)
    record = orchestrator.tick(_snapshot())
    assert record["intent"]["vetoed"] is True
    assert "PRE_AGOP" not in record["intent"]["rationale"]


def test_two_risk_multipliers_compose_multiplicatively():
    from janus.risk import bound
    from janus.contracts import Action, AgopMode, AgopResult
    from janus.config import CONSERVATIVE

    agop_result = AgopResult(
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
    snapshot = _snapshot()
    first_bound = bound(
        snapshot, agop_result, 0.5, CONSERVATIVE, Action.LONG
    )
    second_bound = bound(
        snapshot, agop_result, 0.25, CONSERVATIVE, Action.LONG
    )
    assert (
        second_bound.upper_position_size
        <= first_bound.upper_position_size
    )
    assert first_bound.module_multiplier == 0.5
    assert second_bound.module_multiplier == 0.25


def test_kairos_module_returns_neutral_when_unavailable():
    from janus.modules.kairos import KairosModule

    module = KairosModule(Config())
    context = ModuleContext(
        snapshot=_snapshot(),
        configuration=Config(),
        strategy=__import__(
            "janus.config", fromlist=["CONSERVATIVE"]
        ).CONSERVATIVE,
        phase=ModulePhase.POST_AGOP,
    )
    result = module.run(context)
    assert result.risk_multiplier == 1.0
    assert "unavailable" in result.notes or "neutral" in result.notes


def test_causality_module_returns_neutral_when_unavailable():
    from janus.modules.causality import CausalityModule

    module = CausalityModule(Config())
    context = ModuleContext(
        snapshot=_snapshot(),
        configuration=Config(),
        strategy=__import__(
            "janus.config", fromlist=["CONSERVATIVE"]
        ).CONSERVATIVE,
        phase=ModulePhase.POST_AGOP,
    )
    result = module.run(context)
    assert result.risk_multiplier == 1.0
    assert "unavailable" in result.notes or "neutral" in result.notes