"""
Query engine for the settlement layer.

Provides the three canonical query patterns: by tick, by clade, by session.
"""

from __future__ import annotations

from janus.stirpes.chain import AbstractChainClient
from janus.stirpes.contracts import (
    CladeHash,
    SessionId,
    SettlementRecord,
    TickHash,
)


class QueryEngine:
    """Wraps the chain client with the STIRPES query patterns."""

    def __init__(self, chain: AbstractChainClient) -> None:
        self.chain = chain

    def by_tick(self, tick_hash: TickHash) -> SettlementRecord | None:
        """Single-record lookup by tick hash."""
        results = self.chain.query()
        for record in results:
            if record.tick_hash == tick_hash:
                return record
        return None

    def by_clade(
        self,
        clade_hash: CladeHash,
        time_range: tuple[int, int] | None = None,
    ) -> list[SettlementRecord]:
        """All ticks in a clade, optionally restricted by time."""
        return self.chain.query(clade_hash=clade_hash, time_range=time_range)

    def by_session(
        self,
        session_id: SessionId,
        time_range: tuple[int, int] | None = None,
    ) -> list[SettlementRecord]:
        """All ticks in a session, optionally restricted by time."""
        return self.chain.query(session_id=str(session_id), time_range=time_range)