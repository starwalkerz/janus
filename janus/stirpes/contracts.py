"""
Typed primitives for STIRPES.

Every value that crosses the STIRPES boundary is a frozen dataclass or a
NewType. No bare dicts or tuples. The types are the specification.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import NewType, Optional


# ─────────────────────────────────────────────────────────────────────
# NewTypes for hashes
# ─────────────────────────────────────────────────────────────────────


ClassHash = NewType("ClassHash", bytes)
"""32-byte SHA-256 hash of the canonical form of a fingerprint."""

CladeHash = NewType("CladeHash", bytes)
"""32-byte SHA-256 hash of a clade's leaf set."""

TickHash = NewType("TickHash", bytes)
"""32-byte composed identifier: SHA256(class_hash ‖ session_id ‖ tick_index ‖ snapshot_hash)."""

PayloadHash = NewType("PayloadHash", bytes)
"""32-byte hash of the encrypted payload."""

SessionId = NewType("SessionId", str)
"""Session identifier, deterministic from (deployment, configuration, seed, start_timestamp)."""


# ─────────────────────────────────────────────────────────────────────
# Fingerprint
# ─────────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class Fingerprint:
    """The extracted, canonicalisable solution fingerprint.

    Every field is deterministic from the JANUS tick inputs. Floating-point
    values are pre-rounded to six decimal places, which is the resolution
    at which the AGOP pipeline's outputs are distinguishable.
    """
    ranking: tuple[str, ...]
    survivor_set: tuple[str, ...]
    topology: tuple[tuple[str, str], ...]         # sorted (action, class) pairs
    convergence_depth: int
    capacity: Optional[int]
    lower_confidence_bound: tuple[tuple[str, float], ...]
    composite_score: tuple[tuple[str, float], ...]
    nash_dm: tuple[float, float]
    nash_cp: tuple[float, float]
    nash_entropy: tuple[float, float]
    modules: tuple[tuple[str, str, float, str], ...]  # (name, phase, multiplier, context_hash)
    verdict: str

    def __post_init__(self) -> None:
        # Enforce sorted ordering of the tuple fields that represent maps.
        for name in ("topology", "lower_confidence_bound", "composite_score"):
            value = getattr(self, name)
            sorted_value = tuple(sorted(value))
            if value != sorted_value:
                raise ValueError(f"fingerprint.{name} must be sorted")


# ─────────────────────────────────────────────────────────────────────
# Settlement
# ─────────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class PendingTick:
    """A tick awaiting settlement. Produced by the recorder, consumed by
    flush(). Not written to chain."""
    fingerprint: Fingerprint
    class_hash: ClassHash
    session_id: SessionId
    tick_index: int
    snapshot_hash: bytes
    payload_hash: PayloadHash


@dataclass(frozen=True)
class TickRecord:
    """The on-chain record for a single tick."""
    tick_hash: TickHash
    class_hash: ClassHash
    historical_clade_hash: CladeHash
    session_id: SessionId
    tick_index: int
    blocktime: int
    payload_hash: PayloadHash


@dataclass(frozen=True)
class SettlementBatch:
    """A batch of ticks flushed together. One tree is built; one Merkle
    root is committed; each tick gets its clade hash from that tree."""
    tick_hashes: tuple[TickHash, ...]
    class_hashes: tuple[ClassHash, ...]
    clade_hashes: tuple[CladeHash, ...]
    session_ids: tuple[SessionId, ...]
    tick_indices: tuple[int, ...]
    payload_hashes: tuple[PayloadHash, ...]
    leaf_set_hash: bytes
    tree_root_hash: bytes

    def __post_init__(self) -> None:
        lengths = {
            len(self.tick_hashes),
            len(self.class_hashes),
            len(self.clade_hashes),
            len(self.session_ids),
            len(self.tick_indices),
            len(self.payload_hashes),
        }
        if len(lengths) != 1:
            raise ValueError("settlement batch columns must have equal length")


@dataclass(frozen=True)
class SettlementRecord:
    """The on-chain record for a settled tick, as returned by query."""
    tick_hash: TickHash
    class_hash: ClassHash
    historical_clade_hash: CladeHash
    session_id: SessionId
    tick_index: int
    blocktime: int
    payload_hash: PayloadHash


# ─────────────────────────────────────────────────────────────────────
# Verdict codes
# ─────────────────────────────────────────────────────────────────────


VERDICT_PASS = "pass"
VERDICT_SIZE_CLAMPED = "size_clamped"
VERDICT_CONTRACT_COLLAPSE = "contract_collapse"
VERDICT_TOXICITY_COLLAPSE = "toxicity_collapse"
VERDICT_CONFIDENCE_FLOOR_COLLAPSE = "confidence_floor_collapse"

ALL_VERDICTS = frozenset({
    VERDICT_PASS,
    VERDICT_SIZE_CLAMPED,
    VERDICT_CONTRACT_COLLAPSE,
    VERDICT_TOXICITY_COLLAPSE,
    VERDICT_CONFIDENCE_FLOOR_COLLAPSE,
})