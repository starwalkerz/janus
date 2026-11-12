"""
The batch recorder.

Accumulates ticks, computes fingerprints and class hashes, rebuilds the
tree on flush over the full leaf set (historical + pending), and emits a
SettlementBatch.

Unidirectionality: the recorder has no methods that return data to the
orchestrator beyond the ClassHash of the current tick. The clade
structure is computed inside the recorder, never exposed as a training
signal, and never fed back to the fingerprint extractor.

Historical leaf set: the recorder maintains a persistent `_leaf_fingerprints`
map across flushes, so that the phylogenetic tree is built over the full
leaf set rather than the current batch alone. This gives the tree topology
stability across batches. A maximum size guards against unbounded growth;
leaves are evicted FIFO when the bound is exceeded.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any

from janus.stirpes.chain import AbstractChainClient
from janus.stirpes.clade import (
    clade_hash_for_leaf,
    clade_hash_from_labels,
)
from janus.stirpes.contracts import (
    ClassHash,
    CladeHash,
    Fingerprint,
    PayloadHash,
    PendingTick,
    SessionId,
    SettlementBatch,
    SettlementRecord,
    TickHash,
)
from janus.stirpes.distance import distance_matrix
from janus.stirpes.fingerprint import (
    canonical_form,
    class_hash as compute_class_hash,
    extract_fingerprint,
    snapshot_hash,
)
from janus.stirpes.reveal import PayloadCipher
from janus.stirpes.tree import build_tree


# Maximum number of historical leaves to retain.
MAX_LEAF_SET_SIZE = 2000


@dataclass
class StirpesRecorder:
    """
    The STIRPES batch recorder.

    State
    -----
    chain                       : the settlement client
    cipher                      : the payload cipher
    tree_method                 : "neighbor_joining" | "upgma"
    flush_threshold             : the number of pending ticks that triggers auto-flush
    session_id                  : the current session identifier
    pending                     : ticks awaiting flush
    historical_ticks            : all settled ticks (for query)
    current_clade_hashes        : the latest clade hash assignment per leaf
    _leaf_fingerprints          : persistent leaf set, keyed by class_hash hex
    _leaf_class_hashes          : persistent map from label to class hash
    """
    chain: AbstractChainClient
    cipher: PayloadCipher
    tree_method: str = "neighbor_joining"
    flush_threshold: int = 100
    session_id: SessionId = field(
        default_factory=lambda: SessionId("default-session")
    )
    pending: list[PendingTick] = field(default_factory=list)
    historical_ticks: list[SettlementRecord] = field(default_factory=list)
    current_clade_hashes: dict[ClassHash, CladeHash] = field(
        default_factory=dict
    )
    _leaf_fingerprints: dict[str, Fingerprint] = field(default_factory=dict)
    _leaf_class_hashes: dict[str, ClassHash] = field(default_factory=dict)

    def record(
        self,
        agop_result: Any,
        module_contexts: dict[str, dict[str, Any]],
        snapshot: Any,
        verdict: str = "pass",
    ) -> ClassHash:
        """Record one tick. Returns the class hash of its fingerprint.

        This is the only method that receives the AGOP output and module
        contexts; the return value is a plain hash with no reference to
        the inputs.
        """
        fingerprint = extract_fingerprint(
            agop_result=agop_result,
            module_contexts=module_contexts,
            verdict=verdict,
        )
        ch = compute_class_hash(fingerprint)

        payload_bytes = canonical_form(fingerprint)
        ciphertext = self.cipher.encrypt(payload_bytes)
        ph = PayloadHash(hashlib.sha256(ciphertext).digest())

        pending = PendingTick(
            fingerprint=fingerprint,
            class_hash=ch,
            session_id=self.session_id,
            tick_index=len(self.historical_ticks) + len(self.pending),
            snapshot_hash=snapshot_hash(snapshot),
            payload_hash=ph,
        )
        self.pending.append(pending)

        if len(self.pending) >= self.flush_threshold:
            self.flush()

        return ch

    def flush(self) -> SettlementBatch | None:
        """Rebuild the tree over the full leaf set and produce a settlement batch.

        The tree is built over `historical + pending`, so its topology is
        stable across batches. Only the pending ticks are emitted in the
        batch; historical ticks keep their previously committed clade hash.
        """
        if not self.pending:
            return None

        # Add pending to the persistent leaf set, deduping by class hash.
        for pending in self.pending:
            label = _hash_to_hex(pending.class_hash)
            if label not in self._leaf_fingerprints:
                self._leaf_fingerprints[label] = pending.fingerprint
                self._leaf_class_hashes[label] = pending.class_hash

        # Enforce maximum size (FIFO eviction).
        if len(self._leaf_fingerprints) > MAX_LEAF_SET_SIZE:
            excess = len(self._leaf_fingerprints) - MAX_LEAF_SET_SIZE
            for label in list(self._leaf_fingerprints.keys())[:excess]:
                del self._leaf_fingerprints[label]
                del self._leaf_class_hashes[label]

        all_labels = sorted(self._leaf_fingerprints.keys())
        all_fingerprints = [
            self._leaf_fingerprints[label] for label in all_labels
        ]

        # Build the tree (or handle the singleton case).
        if len(all_labels) < 2:
            # Singleton: the clade of the only leaf is the leaf itself.
            singleton_label = all_labels[0] if all_labels else "unknown"
            singleton_clade = clade_hash_from_labels(
                frozenset([singleton_label]), self._leaf_class_hashes
            )
            clade_by_label = {singleton_label: singleton_clade}
            tree_root_hash = b"\x00" * 32
        else:
            distances = distance_matrix(all_fingerprints)
            tree = build_tree(
                all_labels, distances, method=self.tree_method
            )
            clade_by_label = {
                label: clade_hash_for_leaf(
                    tree, label, self._leaf_class_hashes
                )
                for label in all_labels
            }
            tree_root_hash = hashlib.sha256(
                repr(_tree_signature(tree)).encode()
            ).digest()

        # Compute the batch.
        tick_hashes = []
        for pending in self.pending:
            tick_hash = _compute_tick_hash(
                pending.class_hash,
                pending.session_id,
                pending.tick_index,
                pending.snapshot_hash,
            )
            tick_hashes.append(tick_hash)

        leaf_set_hash = hashlib.sha256(
            b"".join(sorted(t.class_hash for t in self.pending))
        ).digest()

        batch = SettlementBatch(
            tick_hashes=tuple(tick_hashes),
            class_hashes=tuple(t.class_hash for t in self.pending),
            clade_hashes=tuple(
                clade_by_label[_hash_to_hex(t.class_hash)]
                for t in self.pending
            ),
            session_ids=tuple(t.session_id for t in self.pending),
            tick_indices=tuple(t.tick_index for t in self.pending),
            payload_hashes=tuple(t.payload_hash for t in self.pending),
            leaf_set_hash=leaf_set_hash,
            tree_root_hash=tree_root_hash,
        )

        # Update current clade assignments.
        for pending in self.pending:
            label = _hash_to_hex(pending.class_hash)
            self.current_clade_hashes[pending.class_hash] = clade_by_label[
                label
            ]

        self.pending = []
        return batch

    def settle(self, batch: SettlementBatch) -> bytes:
        """Commit a batch to the chain."""
        tx_hash = self.chain.commit(batch)
        blocktime = self.chain.latest_blocktime()
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
            self.historical_ticks.append(record)
        return tx_hash

    def query_by_tick(self, tick_hash: TickHash) -> SettlementRecord | None:
        for record in self.historical_ticks:
            if record.tick_hash == tick_hash:
                return record
        return None

    def query_by_clade(
        self, clade_hash: CladeHash
    ) -> list[SettlementRecord]:
        return [
            record for record in self.historical_ticks
            if record.historical_clade_hash == clade_hash
        ]

    def query_by_session(
        self, session_id: SessionId
    ) -> list[SettlementRecord]:
        return [
            record for record in self.historical_ticks
            if record.session_id == session_id
        ]


def _hash_to_hex(value: bytes) -> str:
    return value.hex()


def _compute_tick_hash(
    class_hash_value: ClassHash,
    session_id: SessionId,
    tick_index: int,
    snapshot_hash_value: bytes,
) -> TickHash:
    payload = (
        bytes(class_hash_value)
        + session_id.encode("utf-8")
        + tick_index.to_bytes(8, "big")
        + snapshot_hash_value
    )
    return TickHash(hashlib.sha256(payload).digest())


def _tree_signature(tree: Any) -> tuple:
    """A deterministic signature of the tree topology, for hashing."""
    def _walk(node: Any) -> tuple:
        if node.is_leaf():
            return ("L", node.label, round(node.length, 6))
        return (
            "N",
            tuple(sorted(_walk(child) for child in node.children)),
            round(node.length, 6),
        )
    return _walk(tree.root)