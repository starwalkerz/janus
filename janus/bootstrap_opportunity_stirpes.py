"""
bootstrap.py — build the module registry and optional STIRPES recorder
from configuration.

The module registry (build_default_registry) registers the ten built-in
modules: the two dampening modules (kairos, causality), the volatility
proxy (regime), the sentiment placeholder, the two quantum econophysics
modules (econophysics_tunneling, econophysics_herding), and the four
opportunity modules (agop_opportunity, causality_opportunity,
kairos_opportunity, opportunity_synthesizer).

The optional STIRPES recorder (build_stirpes_recorder) is constructed
only when configuration.stirpes_enabled is true. The import of
janus.stirpes is deferred into the function body so that the core does
not statically depend on STIRPES: deleting the janus/stirpes/ directory
leaves this file importable and the rest of JANUS fully functional. This
is the mechanism by which STIRPES remains optional while being fully
included in the pipeline's configuration surface.

The caller decides whether to inject the recorder into the orchestrator.
The orchestrator treats the recorder as an opaque object with a
`record(...)` method; it does not import janus.stirpes and does not
depend on the concrete class.
"""

from __future__ import annotations

import importlib
import os
from typing import Any, Optional

from janus.config import Config
from janus.modules.registry import ModuleRegistry
from janus.modules.kairos import KairosModule
from janus.modules.causality import CausalityModule
from janus.modules.regime import RegimeModule
from janus.modules.sentiment import SentimentModule
from janus.modules.econophysics import (
    EconophysicsTunnelingModule,
    EconophysicsHerdingModule,
)
from janus.modules.agop_opportunity import AgopOpportunityModule
from janus.modules.causality_opportunity import CausalityOpportunityModule
from janus.modules.kairos_opportunity import KairosOpportunityModule
from janus.modules.opportunity_synthesizer import OpportunitySynthesizerModule


def build_default_registry(configuration: Config) -> ModuleRegistry:
    """Build the registry of phase-based modules.

    Both the dampening modules and the opportunity modules are registered.
    The two sets are alternatives; the strategy profile and the per-module
    enable flags in configuration determine which set fires in practice.
    Under the OPPORTUNITY strategy, the dampening modules are expected to
    be disabled (see config.example.toml) so that the opportunity modules
    are the sole interpretation of KAIROS anomalies and Causalitybot
    horizons.
    """
    registry = ModuleRegistry()

    registry.register(KairosModule(configuration))
    registry.register(CausalityModule(configuration))
    registry.register(RegimeModule(configuration))
    registry.register(SentimentModule(configuration))

    registry.register(EconophysicsTunnelingModule(configuration))
    registry.register(EconophysicsHerdingModule(configuration))

    registry.register(AgopOpportunityModule(configuration))
    registry.register(CausalityOpportunityModule(configuration))
    registry.register(KairosOpportunityModule(configuration))
    registry.register(OpportunitySynthesizerModule(configuration))

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


def build_stirpes_recorder(configuration: Config) -> Optional[Any]:
    """Build a STIRPES recorder from the configuration.

    Returns None if configuration.stirpes_enabled is false. When true,
    the recorder is constructed from the [stirpes] section of the
    configuration:

        chain_type:           "mock" (default) or "tezos"
        tezos_rpc_url:        RPC endpoint for the Tezos L2
        tezos_contract_address: deployed StirpesRegistry address
        tezos_private_key_env: environment variable holding the private key
        cipher_seed:          seed for the placeholder XOR cipher
        tree_method:          "neighbor_joining" (default) or "upgma"
        flush_threshold:      number of pending ticks before auto-flush
        session_id:           the session identifier for this deployment

    The import of janus.stirpes is deferred to this function so that the
    core remains importable when STIRPES is not installed or not wanted.

    The return type is Any rather than a concrete StirpesRecorder so that
    the caller does not need to import janus.stirpes either. The
    orchestrator's Protocol accepts any object with a `record(...)`
    method that matches the expected signature.
    """
    if not configuration.stirpes_enabled:
        return None

    try:
        from janus.stirpes import (
            StirpesRecorder,
            MockChainClient,
            TezosChainClient,
            XorCipher,
        )
        from janus.stirpes.contracts import SessionId
    except ImportError as exception:
        raise ImportError(
            "configuration.stirpes_enabled is true but janus.stirpes "
            f"is not importable: {exception}"
        ) from exception

    if configuration.stirpes_chain_type == "mock":
        chain = MockChainClient(blocktime_seconds=1)
    elif configuration.stirpes_chain_type == "tezos":
        private_key = os.environ.get(
            configuration.stirpes_tezos_private_key_env, ""
        )
        if not private_key:
            raise ValueError(
                f"stirpes_chain_type is 'tezos' but "
                f"{configuration.stirpes_tezos_private_key_env} is not set"
            )
        if not configuration.stirpes_tezos_rpc_url:
            raise ValueError(
                "stirpes_chain_type is 'tezos' but stirpes_tezos_rpc_url "
                "is empty"
            )
        if not configuration.stirpes_tezos_contract_address:
            raise ValueError(
                "stirpes_chain_type is 'tezos' but "
                "stirpes_tezos_contract_address is empty"
            )
        chain = TezosChainClient(
            rpc_url=configuration.stirpes_tezos_rpc_url,
            contract_address=configuration.stirpes_tezos_contract_address,
            private_key=private_key,
        )
    else:
        raise ValueError(
            f"stirpes_chain_type must be 'mock' or 'tezos', "
            f"got {configuration.stirpes_chain_type!r}"
        )

    cipher = XorCipher(seed=configuration.stirpes_cipher_seed.encode("utf-8"))
    recorder = StirpesRecorder(
        chain=chain,
        cipher=cipher,
        tree_method=configuration.stirpes_tree_method,
        flush_threshold=configuration.stirpes_flush_threshold,
        session_id=SessionId(configuration.stirpes_session_id),
    )
    return recorder