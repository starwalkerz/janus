"""
modules/registry.py — module registry and result validation.
"""

from __future__ import annotations

from janus.contracts import ModulePhase
from janus.modules.base import Module, ModuleResult

KNOWN_AXES = frozenset(
    {"pain", "integration", "regulatory", "readiness", "barrier"}
)


class ModuleRegistry:
    def __init__(self) -> None:
        self._modules: dict[str, Module] = {}

    def register(self, module: Module) -> None:
        if not hasattr(module, "name") or not isinstance(module.name, str):
            raise TypeError("module must define a string attribute 'name'")
        if not hasattr(module, "phase") or not isinstance(
            module.phase, ModulePhase
        ):
            raise TypeError(
                "module must define 'phase' as a ModulePhase enum member"
            )
        if module.name in self._modules:
            raise ValueError(f"module {module.name!r} already registered")
        self._modules[module.name] = module

    def get(self, name: str) -> Module:
        if name not in self._modules:
            raise KeyError(f"module {name!r} not registered")
        return self._modules[name]

    def all_by_phase(self, phase: ModulePhase) -> list[Module]:
        return sorted(
            [
                module
                for module in self._modules.values()
                if module.phase is phase
            ],
            key=lambda module: module.name,
        )

    def names(self) -> list[str]:
        return sorted(self._modules)

    def __len__(self) -> int:
        return len(self._modules)

    def __contains__(self, name: str) -> bool:
        return name in self._modules


def validate_result(result: ModuleResult) -> None:
    if not (0.0 <= result.risk_multiplier <= 1.0):
        raise ValueError(
            f"module {result.name}: risk_multiplier={result.risk_multiplier} "
            f"outside [0,1]"
        )
    if result.axes_patch and result.phase is not ModulePhase.PRE_AGOP:
        raise ValueError(
            f"module {result.name}: axes_patch only allowed in PRE_AGOP, "
            f"got {result.phase.value}"
        )
    for axis, patch in result.axes_patch.items():
        if axis not in KNOWN_AXES:
            raise ValueError(
                f"module {result.name}: unknown axis {axis!r}; "
                f"known: {sorted(KNOWN_AXES)}"
            )
        if not isinstance(patch, dict):
            raise TypeError(
                f"module {result.name}: axes_patch[{axis!r}] must be a dict"
            )
        for action, value in patch.items():
            try:
                numeric_value = float(value)
            except (TypeError, ValueError):
                raise ValueError(
                    f"module {result.name}: {axis}[{action}]={value!r} "
                    f"is not a number"
                )
            if not (0.0 <= numeric_value <= 1.0):
                raise ValueError(
                    f"module {result.name}: {axis}[{action}]={numeric_value} "
                    f"outside [0,1]"
                )