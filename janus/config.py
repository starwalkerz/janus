"""
config.py — configuration model and strategy profiles.

Capacity is not a configuration parameter. It is derived inside AGOP in
DbC mode and is a legacy-only field in the theta profile.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import tomli

from janus.contracts import AgopMode, StrategyName


@dataclass(frozen=True)
class ThetaProfile:
    c_b: float = 10.0
    c_s: float = 3.0
    w: float = 15.0
    ell: float = 2.0
    v_bar: float = 20.0
    theta_1: float = 0.5
    theta_2: float = 0.5
    theta_3: float = 0.5
    sigma_R: float = 0.2
    sigma_B: float = 0.2
    alpha_1: float = 0.4
    alpha_2: float = 0.4
    alpha_3: float = 0.2
    M: int = 5_000
    alpha: float = 0.05
    seed: int = 42
    h: int = 3
    K: int = 3


@dataclass(frozen=True)
class StrategyProfile:
    name: StrategyName
    default_agop_mode: AgopMode
    theta: ThetaProfile
    lower_confidence_bound_floor: float
    kelly_coefficient: float
    position_cap: float
    toxicity_threshold: float
    kairos_dampening: float
    causality_h0: float
    causality_kappa: float
    llm_confidence_floor: float
    require_contract: bool
    on_error_default: str


CONSERVATIVE = StrategyProfile(
    name=StrategyName.CONSERVATIVE,
    default_agop_mode=AgopMode.DBC,
    theta=ThetaProfile(theta_1=0.70, theta_2=0.70, theta_3=0.30, K=1),
    lower_confidence_bound_floor=0.00,
    kelly_coefficient=0.25,
    position_cap=0.10,
    toxicity_threshold=0.15,
    kairos_dampening=0.80,
    causality_h0=0.60,
    causality_kappa=4.0,
    llm_confidence_floor=0.65,
    require_contract=True,
    on_error_default="fail_closed",
)

AGGRESSIVE = StrategyProfile(
    name=StrategyName.AGGRESSIVE,
    default_agop_mode=AgopMode.LEGACY,
    theta=ThetaProfile(theta_1=0.40, theta_2=0.50, theta_3=0.60, K=3),
    lower_confidence_bound_floor=-0.05,
    kelly_coefficient=0.60,
    position_cap=0.35,
    toxicity_threshold=0.30,
    kairos_dampening=0.00,
    causality_h0=0.30,
    causality_kappa=4.0,
    llm_confidence_floor=0.45,
    require_contract=False,
    on_error_default="fail_open",
)

PROFILES = {
    StrategyName.CONSERVATIVE: CONSERVATIVE,
    StrategyName.AGGRESSIVE: AGGRESSIVE,
}


@dataclass(frozen=True)
class ModuleConfiguration:
    enabled: bool = True
    on_error: Optional[str] = None


@dataclass
class Config:
    strategy: StrategyName = StrategyName.CONSERVATIVE
    agop_mode: AgopMode = AgopMode.DBC
    agop_local_path: str = "."
    agop_http_url: str = ""
    kairos_local_path: str = ""
    kairos_http_url: str = ""
    kairos_quantum: bool = False
    causality_local_path: str = ""
    causality_http_url: str = ""
    llm_base_url: str = "http://localhost:11434/v1"
    llm_model: str = "qwen2.5:7b-instruct"
    llm_api_key: str = "ollama"
    llm_temperature: float = 0.0
    llm_timeout_seconds: float = 30.0
    skills_directory: str = "skills"
    active_skills: list[str] = field(
        default_factory=lambda: [
            "toxic-flow-gate",
            "regime-classifier",
            "sizing-discipline",
        ]
    )
    equity: float = 100_000.0
    seed: int = 42
    module_configurations: dict[str, ModuleConfiguration] = field(
        default_factory=dict
    )
    module_imports: list[str] = field(default_factory=list)

    @property
    def profile(self) -> StrategyProfile:
        return PROFILES[self.strategy]

    def module_configuration(self, name: str) -> ModuleConfiguration:
        return self.module_configurations.get(name, ModuleConfiguration())


def _validate_on_error(value: Optional[str]) -> None:
    if value is not None and value not in {"fail_open", "fail_closed"}:
        raise ValueError(
            f"on_error must be 'fail_open' or 'fail_closed', got {value!r}"
        )


def load_config(path: str | Path) -> Config:
    file_path = Path(path)
    if not file_path.exists():
        return Config()
    data = tomli.loads(file_path.read_text(encoding="utf-8"))
    configuration = Config()

    if "strategy" in data:
        configuration.strategy = StrategyName(data["strategy"]["name"])
    if "agop" in data:
        configuration.agop_mode = AgopMode(
            data["agop"].get("mode", configuration.agop_mode.value)
        )
        configuration.agop_local_path = data["agop"].get(
            "local_path", configuration.agop_local_path
        )
        configuration.agop_http_url = data["agop"].get(
            "http_url", configuration.agop_http_url
        )
    if "kairos" in data:
        configuration.kairos_local_path = data["kairos"].get(
            "local_path", configuration.kairos_local_path
        )
        configuration.kairos_http_url = data["kairos"].get(
            "http_url", configuration.kairos_http_url
        )
        configuration.kairos_quantum = bool(
            data["kairos"].get("quantum", configuration.kairos_quantum)
        )
    if "causality" in data:
        configuration.causality_local_path = data["causality"].get(
            "local_path", configuration.causality_local_path
        )
        configuration.causality_http_url = data["causality"].get(
            "http_url", configuration.causality_http_url
        )
    if "llm" in data:
        configuration.llm_base_url = data["llm"].get(
            "base_url", configuration.llm_base_url
        )
        configuration.llm_model = data["llm"].get(
            "model", configuration.llm_model
        )
        configuration.llm_api_key = data["llm"].get(
            "api_key", configuration.llm_api_key
        )
        configuration.llm_temperature = data["llm"].get(
            "temperature", configuration.llm_temperature
        )
        configuration.llm_timeout_seconds = data["llm"].get(
            "timeout_s", configuration.llm_timeout_seconds
        )
    if "skills" in data:
        configuration.skills_directory = data["skills"].get(
            "directory", configuration.skills_directory
        )
        configuration.active_skills = data["skills"].get(
            "active", configuration.active_skills
        )
    if "risk" in data:
        configuration.equity = data["risk"].get("equity", configuration.equity)
        configuration.seed = data["risk"].get("seed", configuration.seed)
    if "modules" in data:
        modules = data["modules"]
        configuration.module_imports = modules.get("imports", [])
        for name, module_configuration in modules.items():
            if name == "imports":
                continue
            on_error = module_configuration.get("on_error")
            _validate_on_error(on_error)
            configuration.module_configurations[name] = ModuleConfiguration(
                enabled=bool(module_configuration.get("enabled", True)),
                on_error=on_error,
            )

    return configuration