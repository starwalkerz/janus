"""
strategies.py — strategy profile lookup and AGOP mode resolution.
"""

from __future__ import annotations

from janus.config import PROFILES, StrategyName, StrategyProfile
from janus.contracts import AgopMode


def get_profile(name: StrategyName) -> StrategyProfile:
    return PROFILES[name]


def resolve_mode(
    strategy: StrategyName,
    override: AgopMode | None,
) -> AgopMode:
    if override is not None:
        return override
    return PROFILES[strategy].default_agop_mode