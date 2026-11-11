"""
api.py — FastAPI surface for JANUS.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from janus.bootstrap import build_default_registry
from janus.config import Config, ModuleConfiguration, load_config
from janus.contracts import AgopMode, MarketSnapshot, StrategyName
from janus.orchestrator import Orchestrator


CONFIG_PATH = Path("config.toml")
CONFIGURATION: Config = (
    load_config(CONFIG_PATH) if CONFIG_PATH.exists() else Config()
)
REGISTRY = build_default_registry(CONFIGURATION)
ORCHESTRATOR = Orchestrator(CONFIGURATION, registry=REGISTRY)

app = FastAPI(title="JANUS", version="1.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UI_FILE = Path(__file__).parent / "ui.html"


class SnapshotInput(BaseModel):
    symbol: str = "BTC/USDT"
    price: float = 50_000.0
    expected_return: float = 0.0
    realized_volatility: float = 0.01
    slippage: float = 2.0
    slippage_maximum: float = 20.0
    venue_risk: float = Field(default=0.2, ge=0.0, le=1.0)
    signal_agreement: float = Field(default=0.0, ge=-1.0, le=1.0)
    order_flow_imbalance: float = 0.0
    history: list[float] = []
    timestamps: list[float] = []
    external_data: dict = {}

    def to_snapshot(self) -> MarketSnapshot:
        return MarketSnapshot(
            symbol=self.symbol,
            price=self.price,
            expected_return=self.expected_return,
            realized_volatility=self.realized_volatility,
            slippage=self.slippage,
            slippage_maximum=self.slippage_maximum,
            venue_risk=self.venue_risk,
            signal_agreement=self.signal_agreement,
            order_flow_imbalance=self.order_flow_imbalance,
            history=tuple(self.history),
            timestamps=tuple(self.timestamps),
            external_data=dict(self.external_data),
        )


class ConfigInput(BaseModel):
    strategy: Optional[StrategyName] = None
    agop_mode: Optional[AgopMode] = None
    llm_model: Optional[str] = None


class ModuleToggleInput(BaseModel):
    enabled: bool


class ModuleOnErrorInput(BaseModel):
    on_error: Optional[str] = None


@app.get("/", include_in_schema=False)
async def root():
    return FileResponse(UI_FILE, media_type="text/html")


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "strategy": ORCHESTRATOR.configuration.strategy.value,
        "agop_mode": ORCHESTRATOR.mode.value,
        "llm_model": ORCHESTRATOR.configuration.llm_model,
        "skills": [skill.name for skill in ORCHESTRATOR.skills],
        "modules": REGISTRY.names(),
    }


@app.get("/api/config")
async def get_config():
    return {
        "strategy": ORCHESTRATOR.configuration.strategy.value,
        "agop_mode": ORCHESTRATOR.mode.value,
        "llm_model": ORCHESTRATOR.configuration.llm_model,
        "position_cap": ORCHESTRATOR.profile.position_cap,
        "kelly_coefficient": ORCHESTRATOR.profile.kelly_coefficient,
        "on_error_default": ORCHESTRATOR.profile.on_error_default,
    }


@app.post("/api/config")
async def set_config(body: ConfigInput):
    global ORCHESTRATOR
    if body.strategy is not None:
        ORCHESTRATOR.configuration.strategy = body.strategy
    if body.agop_mode is not None:
        ORCHESTRATOR.configuration.agop_mode = body.agop_mode
    if body.llm_model is not None:
        ORCHESTRATOR.configuration.llm_model = body.llm_model
    ORCHESTRATOR = Orchestrator(
        ORCHESTRATOR.configuration,
        registry=REGISTRY,
        broker=ORCHESTRATOR.broker,
    )
    return await get_config()


@app.get("/api/modules")
async def list_modules():
    output = []
    for name in REGISTRY.names():
        module = REGISTRY.get(name)
        module_configuration = ORCHESTRATOR.configuration.module_configuration(
            name
        )
        output.append(
            {
                "name": name,
                "phase": module.phase.value,
                "enabled": module_configuration.enabled,
                "on_error": module_configuration.on_error,
                "effective_on_error": (
                    module_configuration.on_error
                    or ORCHESTRATOR.profile.on_error_default
                ),
            }
        )
    return {"modules": output}


@app.post("/api/modules/{name}/toggle")
async def toggle_module(name: str, body: ModuleToggleInput):
    if name not in REGISTRY:
        raise HTTPException(
            status_code=404, detail=f"module {name} not registered"
        )
    current = ORCHESTRATOR.configuration.module_configuration(name)
    ORCHESTRATOR.configuration.module_configurations[name] = (
        ModuleConfiguration(enabled=body.enabled, on_error=current.on_error)
    )
    return {"name": name, "enabled": body.enabled}


@app.post("/api/modules/{name}/on_error")
async def set_on_error(name: str, body: ModuleOnErrorInput):
    if name not in REGISTRY:
        raise HTTPException(
            status_code=404, detail=f"module {name} not registered"
        )
    if body.on_error is not None and body.on_error not in {
        "fail_open",
        "fail_closed",
    }:
        raise HTTPException(
            status_code=400,
            detail="on_error must be 'fail_open' or 'fail_closed'",
        )
    current = ORCHESTRATOR.configuration.module_configuration(name)
    ORCHESTRATOR.configuration.module_configurations[name] = (
        ModuleConfiguration(enabled=current.enabled, on_error=body.on_error)
    )
    return {"name": name, "on_error": body.on_error}


@app.post("/api/tick")
async def tick(body: SnapshotInput):
    try:
        return ORCHESTRATOR.tick(body.to_snapshot())
    except Exception as exception:
        raise HTTPException(
            status_code=500,
            detail=f"{type(exception).__name__}: {exception}",
        )


@app.get("/api/audit")
async def audit():
    return ORCHESTRATOR.audit[-50:]


@app.websocket("/ws/stream")
async def stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_json()
            if message.get("type") != "tick":
                continue
            try:
                snapshot = SnapshotInput(**message["snapshot"]).to_snapshot()
                await websocket.send_json(ORCHESTRATOR.tick(snapshot))
            except Exception as exception:
                await websocket.send_json(
                    {"error": f"{type(exception).__name__}: {exception}"}
                )
    except WebSocketDisconnect:
        pass