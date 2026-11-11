"""
agop_bridge.py — dual-mode adapter for the AGOP decision engine.

Normalises the legacy and DbC cores into a single AgopResult. In DbC mode a
contract violation is returned as `contract_verified=False` rather than being
raised; the verifier maps that to a flat intent (I3).
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


def _import_agop(local_path: str, module_name: str):
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


def _theta_legacy(theta_class, profile: ThetaProfile, L_R, L_C):
    return theta_class(
        c_b=profile.c_b,
        c_s=profile.c_s,
        w=profile.w,
        ell=profile.ell,
        v_bar=profile.v_bar,
        theta_1=profile.theta_1,
        theta_2=profile.theta_2,
        theta_3=profile.theta_3,
        sigma_R=profile.sigma_R,
        sigma_B=profile.sigma_B,
        alpha_1=profile.alpha_1,
        alpha_2=profile.alpha_2,
        alpha_3=profile.alpha_3,
        M=profile.M,
        alpha=profile.alpha,
        seed=profile.seed,
        h=profile.h,
        K=profile.K,
        L_R=L_R,
        L_C=L_C,
    )


def _theta_dbc(theta_class, profile: ThetaProfile, L_R, L_C):
    return theta_class(
        c_b=profile.c_b,
        c_s=profile.c_s,
        w=profile.w,
        ell=profile.ell,
        v_bar=profile.v_bar,
        theta_1=profile.theta_1,
        theta_2=profile.theta_2,
        theta_3=profile.theta_3,
        sigma_R=profile.sigma_R,
        sigma_B=profile.sigma_B,
        alpha_1=profile.alpha_1,
        alpha_2=profile.alpha_2,
        alpha_3=profile.alpha_3,
        M=profile.M,
        alpha=profile.alpha,
        seed=profile.seed,
        h=profile.h,
        L_R=L_R,
        L_C=L_C,
    )


def run_agop(
    mode: AgopMode,
    axes: dict[str, dict[str, float]],
    profile: ThetaProfile,
    local_path: str = ".",
    actions: Optional[list[str]] = None,
) -> AgopResult:
    actions = actions or ["LONG", "FLAT", "SHORT"]
    graph = _build_graph(actions)

    L_R = {
        action: (100.0 * axes["readiness"].get(action, 0.5), 5.0)
        for action in actions
    }
    L_C = {
        action: (100.0 * axes["barrier"].get(action, 0.5), 3.0)
        for action in actions
    }

    if mode is AgopMode.LEGACY:
        try:
            core = _import_agop(local_path, "agop_core")
        except ImportError as exception:
            raise AgopUnavailable(
                f"agop_core not importable: {exception}"
            ) from exception

        theta = _theta_legacy(core.Theta, profile, L_R, L_C)
        problem = core.Problem(V=actions, axes=axes, G=graph, Theta=theta)
        state = core.agop(problem)
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
            capacity=int(profile.K),
            number_of_weisfeiler_lehman_classes=None,
            contract_verified=True,
        )

    try:
        core = _import_agop(local_path, "agop_core_design_by_contract")
    except ImportError as exception:
        raise AgopUnavailable(
            f"agop_core_design_by_contract not importable: {exception}"
        ) from exception

    theta = _theta_dbc(core.Theta, profile, L_R, L_C)
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
    )