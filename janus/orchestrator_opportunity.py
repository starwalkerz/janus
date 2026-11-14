"""
orchestrator.py — the tick.

Pipeline:
  snapshot → [PRE_AGOP modules] → axes → AGOP → [POST_AGOP modules]
           → risk bound → [PRE_LLM modules] → LLM → verified intent

Deterministic given (snapshot, configuration, random seed). Modules
execute alphabetically within each phase (I9). Any veto short-circuits
to FLAT at the phase where it occurs.

The orchestrator stores the tick's outputs on public attributes for
downstream consumers (STIRPES): last_snapshot, last_agop_result,
last_intent, last_module_contexts.

The _run_phase method passes accumulated prior-phase results to each
module's context, so PRE_LLM modules (such as the opportunity
synthesizer) can see PRE_AGOP and POST_AGOP results.
"""

from __future__ import annotations

import json
from dataclasses import asdict

from janus.agop_bridge import AgopUnavailable, run_agop
from janus.config import Config
from janus.contracts import (
    Action,
    AgopMode,
    AgopResult,
    MarketSnapshot,
    ModulePhase,
    RiskBound,
    StrategyName,
    TradeIntent,
    verify_trade_intent,
)
from janus.execution import PaperBroker
from janus.features import build_axes
from janus.llm import LLMClient
from janus.modules.base import ModuleContext, ModuleResult
from janus.modules.registry import ModuleRegistry, validate_result
from janus.risk import bound
from janus.skills import compose_system_prompt, load_skills
from janus.strategies import get_profile, resolve_mode


class Orchestrator:
    def __init__(
        self,
        configuration: Config,
        registry: ModuleRegistry | None = None,
        broker: PaperBroker | None = None,
    ) -> None:
        self.configuration = configuration
        self.registry = registry or ModuleRegistry()
        self.broker = broker or PaperBroker(equity=configuration.equity)
        self.profile = get_profile(configuration.strategy)
        self.mode = resolve_mode(
            configuration.strategy, configuration.agop_mode
        )
        self.skills = load_skills(
            configuration.skills_directory, configuration.active_skills
        )
        self.system_prompt = compose_system_prompt(self.skills)
        self.llm = LLMClient(
            base_url=configuration.llm_base_url,
            model=configuration.llm_model,
            api_key=configuration.llm_api_key,
            temperature=configuration.llm_temperature,
            timeout_seconds=configuration.llm_timeout_seconds,
        )
        self.audit: list[dict] = []

        self.last_snapshot: MarketSnapshot | None = None
        self.last_agop_result: AgopResult | None = None
        self.last_intent: TradeIntent | None = None
        self.last_module_contexts: dict[str, dict] = {}

        self._pre_agop_results: dict[str, ModuleResult] = {}
        self._post_agop_results: dict[str, ModuleResult] = {}
        self._pre_llm_results: dict[str, ModuleResult] = {}

    def _run_phase(
        self,
        phase: ModulePhase,
        snapshot: MarketSnapshot,
        agop_result: AgopResult | None = None,
        risk_bound: RiskBound | None = None,
    ) -> dict[str, ModuleResult]:
        results: dict[str, ModuleResult] = {}
        for module in self.registry.all_by_phase(phase):
            module_configuration = self.configuration.module_configuration(
                module.name
            )
            if not module_configuration.enabled:
                continue

            merged_prior: dict[str, ModuleResult] = {}
            if phase is not ModulePhase.PRE_AGOP:
                merged_prior.update(self._pre_agop_results)
            if phase is ModulePhase.PRE_LLM:
                merged_prior.update(self._post_agop_results)
            merged_prior.update(results)

            context = ModuleContext(
                snapshot=snapshot,
                configuration=self.configuration,
                strategy=self.profile,
                phase=phase,
                agop_result=agop_result,
                risk_bound=risk_bound,
                prior_results=merged_prior,
            )
            try:
                result = module.run(context)
                validate_result(result)
                results[module.name] = result
            except Exception as exception:
                on_error = (
                    module_configuration.on_error
                    or self.profile.on_error_default
                )
                if on_error == "fail_closed":
                    results[module.name] = ModuleResult(
                        name=module.name,
                        phase=phase,
                        veto=True,
                        errored=True,
                        error_message=(
                            f"{type(exception).__name__}: {exception}"
                        ),
                        notes="module error; fail_closed",
                    )
                else:
                    results[module.name] = ModuleResult(
                        name=module.name,
                        phase=phase,
                        errored=True,
                        error_message=(
                            f"{type(exception).__name__}: {exception}"
                        ),
                        notes="module error; fail_open",
                    )
        return results

    def _flatten_module_contexts(self) -> dict[str, dict]:
        output: dict[str, dict] = {}
        for phase_results, phase_name in [
            (self._pre_agop_results, "pre_agop"),
            (self._post_agop_results, "post_agop"),
            (self._pre_llm_results, "pre_llm"),
        ]:
            for name, result in phase_results.items():
                entry = {
                    "phase": phase_name,
                    "risk_multiplier": result.risk_multiplier,
                    "veto": result.veto,
                    "context": result.context,
                }
                if result.errored:
                    entry["errored"] = True
                    entry["error_message"] = result.error_message
                output[name] = entry
        return output

    @verify_trade_intent
    def _decide(self, snapshot: MarketSnapshot):
        self._pre_agop_results = {}
        self._post_agop_results = {}
        self._pre_llm_results = {}

        self._pre_agop_results = self._run_phase(
            ModulePhase.PRE_AGOP, snapshot
        )
        pre_agop = self._pre_agop_results

        if any(result.veto for result in pre_agop.values()):
            agop_result = self._empty_agop("vetoed by PRE_AGOP module")
            risk = RiskBound(0.0, 0.0, 0.0, False, "PRE_AGOP veto")
            intent = TradeIntent(
                action=Action.FLAT,
                position_size=0.0,
                rationale="PRE_AGOP veto",
                agop_mode=self.mode,
                strategy=self.configuration.strategy,
                vetoed=True,
            )
            return intent, agop_result, risk, self.configuration.strategy

        axes = build_axes(snapshot)
        for result in pre_agop.values():
            for axis, patch in result.axes_patch.items():
                axes.setdefault(axis, {}).update(patch)

        try:
            agop_result = run_agop(
                mode=self.mode,
                axes=axes,
                profile=self.profile.theta,
                local_path=self.configuration.agop_local_path,
            )
        except AgopUnavailable:
            agop_result = self._empty_agop("AGOP unavailable")

        self._post_agop_results = self._run_phase(
            ModulePhase.POST_AGOP, snapshot, agop_result=agop_result
        )
        post_agop = self._post_agop_results

        if agop_result.contract_verified and agop_result.ranking:
            action = Action(agop_result.ranking[0])
        else:
            action = Action.FLAT

        multiplier = 1.0
        any_veto = False
        for result in post_agop.values():
            multiplier *= result.risk_multiplier
            if result.veto:
                any_veto = True
        multiplier = float(max(0.0, min(1.0, multiplier)))

        if not agop_result.contract_verified or any_veto:
            risk = RiskBound(
                upper_position_size=0.0,
                kelly_fraction=0.0,
                module_multiplier=multiplier,
                toxic=any_veto,
                reason=(
                    "agop contract violated"
                    if not agop_result.contract_verified
                    else "POST_AGOP veto"
                ),
            )
            intent = TradeIntent(
                action=Action.FLAT,
                position_size=0.0,
                rationale=risk.reason,
                agop_mode=self.mode,
                strategy=self.configuration.strategy,
                vetoed=True,
                contract_forced_flat=not agop_result.contract_verified,
            )
            return intent, agop_result, risk, self.configuration.strategy

        risk = bound(
            snapshot=snapshot,
            agop_result=agop_result,
            module_multiplier=multiplier,
            profile=self.profile,
            action=action,
        )

        if risk.toxic or risk.upper_position_size <= 0.0:
            intent = TradeIntent(
                action=Action.FLAT,
                position_size=0.0,
                rationale=risk.reason,
                agop_mode=self.mode,
                strategy=self.configuration.strategy,
                vetoed=True,
            )
            return intent, agop_result, risk, self.configuration.strategy

        self._pre_llm_results = self._run_phase(
            ModulePhase.PRE_LLM,
            snapshot,
            agop_result=agop_result,
            risk_bound=risk,
        )
        pre_llm = self._pre_llm_results

        if any(result.veto for result in pre_llm.values()):
            intent = TradeIntent(
                action=Action.FLAT,
                position_size=0.0,
                rationale="PRE_LLM veto",
                agop_mode=self.mode,
                strategy=self.configuration.strategy,
                vetoed=True,
            )
            return intent, agop_result, risk, self.configuration.strategy

        llm_context = {
            "snapshot": asdict(snapshot),
            "agop": {
                "mode": agop_result.mode.value,
                "ranking": agop_result.ranking,
                "lower_confidence_bound": agop_result.lower_confidence_bound,
                "composite_score": agop_result.composite_score,
                "contract_verified": agop_result.contract_verified,
                "capacity": agop_result.capacity,
            },
            "risk_bound": risk.upper_position_size,
            "risk_reason": risk.reason,
            "allowed_actions": agop_result.ranking,
            "modules": {
                "pre_agop": {
                    name: asdict(result)
                    for name, result in pre_agop.items()
                },
                "post_agop": {
                    name: asdict(result)
                    for name, result in post_agop.items()
                },
                "pre_llm": {
                    name: asdict(result)
                    for name, result in pre_llm.items()
                },
            },
        }
        llm_decision = self.llm.decide(self.system_prompt, llm_context)

        if llm_decision.confidence < self.profile.llm_confidence_floor:
            intent = TradeIntent(
                action=Action.FLAT,
                position_size=0.0,
                rationale=(
                    f"llm confidence {llm_decision.confidence:.2f} below floor "
                    f"{self.profile.llm_confidence_floor}; "
                    f"{llm_decision.rationale}"
                ),
                agop_mode=self.mode,
                strategy=self.configuration.strategy,
                skills_cited=llm_decision.skills_cited,
                vetoed=True,
            )
            return intent, agop_result, risk, self.configuration.strategy

        if llm_decision.action.value in agop_result.ranking:
            final_action = llm_decision.action
        else:
            final_action = action

        position_size = min(
            llm_decision.delta * risk.upper_position_size,
            risk.upper_position_size,
        )

        intent = TradeIntent(
            action=final_action,
            position_size=float(position_size),
            rationale=llm_decision.rationale or "llm decision",
            agop_mode=self.mode,
            strategy=self.configuration.strategy,
            skills_cited=llm_decision.skills_cited,
        )
        return intent, agop_result, risk, self.configuration.strategy

    def _empty_agop(self, reason: str) -> AgopResult:
        return AgopResult(
            mode=self.mode,
            ranking=[],
            survivor_set=[],
            lower_confidence_bound={},
            composite_score={},
            topology_class={},
            convergence_depth=-1,
            capacity=None,
            number_of_weisfeiler_lehman_classes=None,
            contract_verified=False,
            contract_error=reason,
        )

    def tick(self, snapshot: MarketSnapshot) -> dict:
        intent, agop_result, risk, strategy = self._decide(snapshot)

        self.last_snapshot = snapshot
        self.last_agop_result = agop_result
        self.last_intent = intent
        self.last_module_contexts = self._flatten_module_contexts()

        fill = self.broker.execute(
            intent, snapshot.symbol, snapshot.price
        )
        record = {
            "snapshot": asdict(snapshot),
            "agop": {
                "mode": agop_result.mode.value,
                "ranking": agop_result.ranking,
                "contract_verified": agop_result.contract_verified,
                "contract_error": agop_result.contract_error,
                "capacity": agop_result.capacity,
                "number_of_weisfeiler_lehman_classes": (
                    agop_result.number_of_weisfeiler_lehman_classes
                ),
                "nash_dm": list(agop_result.nash_dm),
                "nash_cp": list(agop_result.nash_cp),
            },
            "risk": asdict(risk),
            "intent": asdict(intent),
            "fill": asdict(fill) if fill else None,
            "modules": self.last_module_contexts,
        }
        self.audit.append(record)
        return record

    def audit_json(self) -> str:
        return json.dumps(self.audit, indent=2, default=str)