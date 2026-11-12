"""
agop_bridge.py — dual-mode adapter for the AGOP decision engine.

Normalises the legacy and design-by-contract cores into a single AgopResult.
In design-by-contract mode a contract violation is returned as
contract_verified=False rather than being raised; the verifier maps that to
a flat intent (I3).

The bridge now populates AgopResult.nash_dm and AgopResult.nash_cp from the
AGOP State, so that downstream consumers (STIRPES) have the Nash strategies
without needing the raw State object.
"""

from __future__ import annotations

import importlib
import sys
from typing import Optional

import networkx as nx

from janus.config import ThetaProfile
from janus.contracts import AgopMode, AgopResult


class AgopUnavailable(RuntimeError):
    pass


def _import_agop_module(local_path: str, module_name: str):
    if local_path and local_path not in sys.path:
        sys.path.insert(0, local_path)
    return importlib.import_module(module_name)


def _build_graph(actions: list[str]) -> nx.DiGraph:
    graph = nx.DiGraph()
    for action in actions:
        graph.add_node(action)
    if "LONG" in actions and "SHORT" in actions:
        graph.add_edge("LONG", "SHORT", sign=-1)
        graph.add_edge("SHORT", "LONG", sign=-1)
    for action in actions:
        if action != "FLAT":
            graph.add_edge(action, "FLAT", sign=1)
            graph.add_edge("FLAT", action, sign=1)
    return graph


def _build_legacy_theta(
    theta_class,
    profile: ThetaProfile,
    likelihood_revenue: dict,
    likelihood_cost: dict,
):
    return theta_class(
        c_b=profile.bespoke_cost,
        c_s=profile.standard_cost,
        w=profile.willingness_to_pay,
        ell=profile.liability_exposure,
        v_bar=profile.mean_client_value,
        theta_1=profile.pain_threshold,
        theta_2=profile.integration_threshold,
        theta_3=profile.regulatory_threshold,
        sigma_R=profile.readiness_sigma,
        sigma_B=profile.barrier_sigma,
        alpha_1=profile.degree_weight,
        alpha_2=profile.betweenness_weight,
        alpha_3=profile.eigenvector_weight,
        M=profile.monte_carlo_draws,
        alpha=profile.confidence_level,
        seed=profile.random_seed,
        h=profile.weisfeiler_lehman_depth,
        K=profile.legacy_capacity_override,
        L_R=likelihood_revenue,
        L_C=likelihood_cost,
    )


def _build_dbc_theta(
    theta_class,
    profile: ThetaProfile,
    likelihood_revenue: dict,
    likelihood_cost: dict,
):
    return theta_class(
        c_b=profile.bespoke_cost,
        c_s=profile.standard_cost,
        w=profile.willingness_to_pay,
        ell=profile.liability_exposure,
        v_bar=profile.mean_client_value,
        theta_1=profile.pain_threshold,
        theta_2=profile.integration_threshold,
        theta_3=profile.regulatory_threshold,
        sigma_R=profile.readiness_sigma,
        sigma_B=profile.barrier_sigma,
        alpha_1=profile.degree_weight,
        alpha_2=profile.betweenness_weight,
        alpha_3=profile.eigenvector_weight,
        M=profile.monte_carlo_draws,
        alpha=profile.confidence_level,
        seed=profile.random_seed,
        h=profile.weisfeiler_lehman_depth,
        L_R=likelihood_revenue,
        L_C=likelihood_cost,
    )


def _extract_nash(state) -> tuple[tuple[float, float], tuple[float, float]]:
    """Extract the (dm, cp) Nash strategies from an AGOP State."""
    sigma_dm = tuple(float(p) for p in state.e_1[0])
    sigma_cp = tuple(float(p) for p in state.e_1[1])
    return sigma_dm, sigma_cp


def run_agop(
    mode: AgopMode,
    axes: dict[str, dict[str, float]],
    profile: ThetaProfile,
    local_path: str = ".",
    actions: Optional[list[str]] = None,
) -> AgopResult:
    actions = actions or ["LONG", "FLAT", "SHORT"]
    graph = _build_graph(actions)

    likelihood_revenue = {
        action: (100.0 * axes["readiness"].get(action, 0.5), 5.0)
        for action in actions
    }
    likelihood_cost = {
        action: (100.0 * axes["barrier"].get(action, 0.5), 3.0)
        for action in actions
    }

    if mode is AgopMode.LEGACY:
        try:
            core = _import_agop_module(local_path, "agop_core")
        except ImportError as exception:
            raise AgopUnavailable(
                f"agop_core not importable: {exception}"
            ) from exception

        theta = _build_legacy_theta(
            core.Theta, profile, likelihood_revenue, likelihood_cost
        )
        problem = core.Problem(V=actions, axes=axes, G=graph, Theta=theta)
        state = core.agop(problem)
        sigma_dm, sigma_cp = _extract_nash(state)
        return AgopResult(
            mode=mode,
            ranking=list(state.R),
            survivor_set=sorted(state.D_star),
            lower_confidence_bound={
                key: float(value) for key, value in state.LCB.items()
            },
            composite_score={
                key: float(value) for key, value in state.Phi.items()
            },
            topology_class=dict(state.T),
            convergence_depth=int(state.convergence_depth),
            capacity=int(profile.legacy_capacity_override),
            number_of_weisfeiler_lehman_classes=None,
            contract_verified=True,
            nash_dm=sigma_dm,
            nash_cp=sigma_cp,
        )

    try:
        core = _import_agop_module(
            local_path, "agop_core_design_by_contract"
        )
    except ImportError as exception:
        raise AgopUnavailable(
            f"agop_core_design_by_contract not importable: {exception}"
        ) from exception

    theta = _build_dbc_theta(
        core.Theta, profile, likelihood_revenue, likelihood_cost
    )
    problem = core.Problem(V=actions, axes=axes, G=graph, Theta=theta)

    try:
        state = core.agop(problem)
    except AssertionError as exception:
        return AgopResult(
            mode=mode,
            ranking=[],
            survivor_set=[],
            lower_confidence_bound={},
            composite_score={},
            topology_class={},
            convergence_depth=-1,
            capacity=None,
            number_of_weisfeiler_lehman_classes=None,
            contract_verified=False,
            contract_error=str(exception),
        )

    sigma_dm, sigma_cp = _extract_nash(state)
    return AgopResult(
        mode=mode,
        ranking=list(state.R),
        survivor_set=sorted(state.D_star),
        lower_confidence_bound={
            key: float(value) for key, value in state.LCB.items()
        },
        composite_score={
            key: float(value) for key, value in state.Phi.items()
        },
        topology_class=dict(state.T),
        convergence_depth=int(state.convergence_depth),
        capacity=int(state.K_derived),
        number_of_weisfeiler_lehman_classes=int(state.n_wl_classes),
        contract_verified=True,
        nash_dm=sigma_dm,
        nash_cp=sigma_cp,
    )