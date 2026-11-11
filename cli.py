"""JANUS command-line interface."""

import argparse
import json
import sys
from pathlib import Path

from janus.bootstrap import build_default_registry
from janus.config import Config, ModuleConfiguration, load_config
from janus.contracts import AgopMode, MarketSnapshot, StrategyName
from janus.orchestrator import Orchestrator


def _sample_snapshot() -> MarketSnapshot:
    return MarketSnapshot(
        symbol="BTC/USDT",
        price=50_000.0,
        expected_return=0.004,
        realized_volatility=0.012,
        slippage=2.0,
        slippage_maximum=20.0,
        venue_risk=0.2,
        signal_agreement=0.6,
        order_flow_imbalance=0.05,
        history=tuple(50_000.0 + index for index in range(32)),
        timestamps=tuple(float(index) for index in range(32)),
        external_data={"sentiment": 0.2},
    )


def main() -> int:
    parser = argparse.ArgumentParser(prog="janus")
    subcommands = parser.add_subparsers(dest="command", required=True)

    tick_parser = subcommands.add_parser("tick")
    tick_parser.add_argument(
        "--strategy",
        choices=["conservative", "aggressive"],
        default="conservative",
    )
    tick_parser.add_argument(
        "--agop-mode",
        choices=["legacy", "dbc"],
        default=None,
    )
    tick_parser.add_argument(
        "--disable",
        nargs="*",
        default=[],
        help="module names to disable for this run",
    )

    arguments = parser.parse_args()

    config_path = Path("config.toml")
    configuration = load_config(config_path) if config_path.exists() else Config()
    configuration.strategy = StrategyName(arguments.strategy)
    if arguments.agop_mode is not None:
        configuration.agop_mode = AgopMode(arguments.agop_mode)
    else:
        configuration.agop_mode = configuration.profile.default_agop_mode

    for module_name in arguments.disable:
        existing = configuration.module_configuration(module_name)
        configuration.module_configurations[module_name] = ModuleConfiguration(
            enabled=False,
            on_error=existing.on_error,
        )

    registry = build_default_registry(configuration)
    orchestrator = Orchestrator(configuration, registry=registry)
    record = orchestrator.tick(_sample_snapshot())
    print(json.dumps(record, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())