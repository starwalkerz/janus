"""
bootstrap.py — build the module registry from configuration.
"""

from __future__ import annotations

import importlib

from janus.config import Config
from janus.modules.registry import ModuleRegistry
from janus.modules.kairos import KairosModule
from janus.modules.causality import CausalityModule
from janus.modules.regime import RegimeModule
from janus.modules.sentiment import SentimentModule


def build_default_registry(configuration: Config) -> ModuleRegistry:
    registry = ModuleRegistry()
    registry.register(KairosModule(configuration))
    registry.register(CausalityModule(configuration))
    registry.register(RegimeModule(configuration))
    registry.register(SentimentModule(configuration))

    for path in configuration.module_imports:
        try:
            module = importlib.import_module(path)
        except ImportError as exception:
            raise ImportError(
                f"could not import custom module {path!r}: {exception}"
            ) from exception
        if not hasattr(module, "module"):
            raise ImportError(
                f"{path!r} must export a `module` variable that is a "
                f"Module instance"
            )
        registry.register(module.module)

    return registry