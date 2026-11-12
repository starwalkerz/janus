"""
Abstract chain client and mock implementation.

The TezosChainClient is a stub. It requires `web3` and a deployed
`StirpesRegistry.sol` contract. It is not exercised by the test suite;
the MockChainClient is.
"""

from __future__ import annotations

import hashlib
import time
from abc import ABC, abstractmethod

from janus.stirpes.contracts import (
    SettlementBatch,
    SettlementRecord,
)


class AbstractChainClient(ABC):
    """The settlement client interface."""

    @abstractmethod
    def commit(self, batch: SettlementBatch) -> bytes:
        """Commit a settlement batch. Returns the transaction hash."""
        ...

    @abstractmethod
    def query(
        self,
        class_hash: bytes | None = None,
        clade_hash: bytes | None = None,
        session_id: str | None = None,
        time_range: tuple[int, int] | None = None,
    ) -> list[SettlementRecord]:
        """Query the settlement layer."""
        ...

    @abstractmethod
    def latest_blocktime(self) -> int:
        """The latest block's timestamp."""
        ...


class MockChainClient(AbstractChainClient):
    """In-memory chain for testing. Every commit produces a
    deterministic transaction hash and appends to an in-memory log."""

    def __init__(self, blocktime_seconds: int = 1) -> None:
        self.blocktime_seconds = blocktime_seconds
        self.records: list[SettlementRecord] = []
        self._block_counter = 0

    def commit(self, batch: SettlementBatch) -> bytes:
        self._block_counter += 1
        blocktime = self._block_counter * self.blocktime_seconds
        tx_hash = hashlib.sha256(
            f"batch-{self._block_counter}".encode()
        ).digest()
        for i in range(len(batch.tick_hashes)):
            record = SettlementRecord(
                tick_hash=batch.tick_hashes[i],
                class_hash=batch.class_hashes[i],
                historical_clade_hash=batch.clade_hashes[i],
                session_id=batch.session_ids[i],
                tick_index=batch.tick_indices[i],
                blocktime=blocktime,
                payload_hash=batch.payload_hashes[i],
            )
            self.records.append(record)
        return tx_hash

    def query(
        self,
        class_hash: bytes | None = None,
        clade_hash: bytes | None = None,
        session_id: str | None = None,
        time_range: tuple[int, int] | None = None,
    ) -> list[SettlementRecord]:
        results = self.records
        if class_hash is not None:
            results = [r for r in results if r.class_hash == class_hash]
        if clade_hash is not None:
            results = [r for r in results if r.historical_clade_hash == clade_hash]
        if session_id is not None:
            results = [r for r in results if r.session_id == session_id]
        if time_range is not None:
            lo, hi = time_range
            results = [r for r in results if lo <= r.blocktime <= hi]
        return list(results)

    def latest_blocktime(self) -> int:
        return self._block_counter * self.blocktime_seconds


class TezosChainClient(AbstractChainClient):
    """Placeholder for real Tezos L2 interaction.

    Requires `web3` and a deployed StirpesRegistry.sol contract. The
    deployment and configuration are out of scope for this module.
    """

    def __init__(
        self,
        rpc_url: str,
        contract_address: str,
        private_key: str,
    ) -> None:
        try:
            from web3 import Web3
        except ImportError as exception:
            raise ImportError(
                "TezosChainClient requires the 'web3' package. "
                "Install it with: pip install web3"
            ) from exception
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        self.contract_address = contract_address
        self.private_key = private_key
        self._contract = None  # set on first use

    def commit(self, batch: SettlementBatch) -> bytes:
        raise NotImplementedError(
            "TezosChainClient.commit requires the deployed contract ABI. "
            "This is deployment-specific and out of scope for STIRPES."
        )

    def query(
        self,
        class_hash: bytes | None = None,
        clade_hash: bytes | None = None,
        session_id: str | None = None,
        time_range: tuple[int, int] | None = None,
    ) -> list[SettlementRecord]:
        raise NotImplementedError(
            "TezosChainClient.query requires the deployed contract ABI. "
            "This is deployment-specific and out of scope for STIRPES."
        )

    def latest_blocktime(self) -> int:
        return int(self.web3.eth.get_block("latest")["timestamp"])