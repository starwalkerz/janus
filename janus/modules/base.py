"""
modules/base.py — the module protocol.

A module is a deterministic function from a ModuleContext to a ModuleResult.
It may patch axes only in the PRE_AGOP phase, may return a risk multiplier in
[0,1], and may veto from any phase.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from janus.contracts import (
    AgopResult,
    MarketSnapshot,
    ModulePhase,
    RiskBound,
)

if TYPE_CHECKING:
    from janus.config import Config, StrategyProfile


@dataclass(frozen=True)
class ModuleContext:
    snapshot: MarketSnapshot
    configuration: "Config"
    strategy: "StrategyProfile"
    phase: ModulePhase
    agop_result: Optional[AgopResult] = None
    risk_bound: Optional[RiskBound] = None
    prior_results: dict = field(default_factory=dict)


@dataclass(frozen=True)
class ModuleResult:
    name: str
    phase: ModulePhase
    axes_patch: dict[str, dict[str, float]] = field(default_factory=dict)
    risk_multiplier: float = 1.0
    veto: bool = False
    context: dict = field(default_factory=dict)
    notes: str = ""
    errored: bool = False
    error_message: str = ""


class Module(ABC):
    name: str
    phase: ModulePhase

    @abstractmethod
    def run(self, context: ModuleContext) -> ModuleResult:
        ...