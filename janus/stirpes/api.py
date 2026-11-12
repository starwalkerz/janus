"""
FastAPI endpoints for STIRPES.

These endpoints wrap the recorder and the query engine. The recorder is
typically an instance created at startup and shared across requests.
"""

from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from janus.stirpes.chain import MockChainClient
from janus.stirpes.contracts import (
    CladeHash,
    SessionId,
    TickHash,
)
from janus.stirpes.query import QueryEngine
from janus.stirpes.recorder import StirpesRecorder
from janus.stirpes.reveal import PayloadCipher, RevealGate, XorCipher


# Default instances; production deployments wire these to real
# configuration values.
_chain = MockChainClient()
_cipher = XorCipher()
_recorder = StirpesRecorder(chain=_chain, cipher=_cipher)
_query_engine = QueryEngine(chain=_chain)


router = APIRouter(prefix="/api/stirpes", tags=["stirpes"])


class FlushRequest(BaseModel):
    pass


class RevealRequest(BaseModel):
    caller_address: str
    tick_hash: str  # hex
    ciphertext_hex: str


class CladeResponse(BaseModel):
    clade_hash: str
    tick_hashes: list[str]


class SignalResponse(BaseModel):
    pagels_lambda: float
    blombergs_k: float


@router.post("/flush")
async def flush() -> dict[str, Any]:
    batch = _recorder.flush()
    if batch is None:
        return {"flushed": False, "reason": "no pending ticks"}
    tx_hash = _recorder.settle(batch)
    return {
        "flushed": True,
        "tx_hash": tx_hash.hex(),
        "tick_count": len(batch.tick_hashes),
        "clade_count": len(set(batch.clade_hashes)),
    }


@router.get("/clade/{clade_hash_hex}")
async def get_clade(clade_hash_hex: str) -> CladeResponse:
    clade_bytes = bytes.fromhex(clade_hash_hex)
    records = _query_engine.by_clade(CladeHash(clade_bytes))
    return CladeResponse(
        clade_hash=clade_hash_hex,
        tick_hashes=[r.tick_hash.hex() for r in records],
    )


@router.get("/tick/{tick_hash_hex}")
async def get_tick(tick_hash_hex: str) -> dict[str, Any]:
    tick_bytes = bytes.fromhex(tick_hash_hex)
    record = _query_engine.by_tick(TickHash(tick_bytes))
    if record is None:
        raise HTTPException(status_code=404, detail="tick not found")
    return {
        "tick_hash": record.tick_hash.hex(),
        "class_hash": record.class_hash.hex(),
        "clade_hash": record.historical_clade_hash.hex(),
        "session_id": record.session_id,
        "tick_index": record.tick_index,
        "blocktime": record.blocktime,
        "payload_hash": record.payload_hash.hex(),
    }


@router.get("/session/{session_id}")
async def get_session(session_id: str) -> list[dict[str, Any]]:
    records = _query_engine.by_session(SessionId(session_id))
    return [
        {
            "tick_hash": r.tick_hash.hex(),
            "class_hash": r.class_hash.hex(),
            "clade_hash": r.historical_clade_hash.hex(),
            "tick_index": r.tick_index,
            "blocktime": r.blocktime,
        }
        for r in records
    ]


@router.post("/reveal")
async def reveal(request: RevealRequest) -> dict[str, Any]:
    # In a real deployment, we would look up the ciphertext by hash from
    # a data-availability layer. Here the caller provides the ciphertext
    # directly, which is only useful for testing.
    tick_bytes = bytes.fromhex(request.tick_hash)
    record = _query_engine.by_tick(TickHash(tick_bytes))
    if record is None:
        raise HTTPException(status_code=404, detail="tick not found")

    gate = RevealGate(token_ledger=_token_ledger_stub(), min_balance=0)
    ciphertext = bytes.fromhex(request.ciphertext_hex)
    plaintext = gate.check_and_reveal(
        caller_address=request.caller_address,
        payload_hash=record.payload_hash,
        ciphertext=ciphertext,
        cipher=_cipher,
    )
    if plaintext is None:
        raise HTTPException(status_code=402, detail="payment required")
    return {"plaintext_hex": plaintext.hex()}


def _token_ledger_stub():
    from janus.stirpes.reveal import TokenLedger

    class _Stub(TokenLedger):
        def balance_of(self, address: str) -> int:
            return 0

        def transferred_to(self, from_address: str, to_address: str) -> int:
            return 0

    return _Stub()