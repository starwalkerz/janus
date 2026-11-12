"""
Clade hashing.

Given a tree and a leaf label, return the clade hash of the leaf's
parent clade. Given a set of leaves directly, return the clade hash of
that set.
"""

from __future__ import annotations

import hashlib

from janus.stirpes.contracts import CladeHash
from janus.stirpes.tree import PhylogeneticTree


def clade_hash_from_labels(
    labels: frozenset[str] | set[str] | list[str],
    class_hashes: dict[str, bytes],
) -> CladeHash:
    """Definition 7: SHA256 of the sorted concatenation of leaf class hashes."""
    sorted_hashes = sorted(class_hashes[label] for label in labels)
    concatenated = b"".join(sorted_hashes)
    return CladeHash(hashlib.sha256(concatenated).digest())


def clade_hash_for_leaf(
    tree: PhylogeneticTree,
    leaf_label: str,
    class_hashes: dict[str, bytes],
) -> CladeHash:
    """Clade hash of the leaf's parent clade (the most specific clade)."""
    leaf = tree.leaves.get(leaf_label)
    if leaf is None:
        raise KeyError(f"leaf {leaf_label!r} not found")
    parent = leaf.parent
    if parent is None:
        raise RuntimeError(f"leaf {leaf_label!r} has no parent (singleton tree)")
    clade = tree._leaves_under(parent)
    return clade_hash_from_labels(clade, class_hashes)


def all_clades(
    tree: PhylogeneticTree,
    class_hashes: dict[str, bytes],
) -> dict[CladeHash, frozenset[str]]:
    """Return all internal-node clades as a map from clade hash to leaf set."""
    result: dict[CladeHash, frozenset[str]] = {}
    for node in tree.internal_nodes():
        clade = tree._leaves_under(node)
        if len(clade) >= 2:
            result[clade_hash_from_labels(clade, class_hashes)] = clade
    return result