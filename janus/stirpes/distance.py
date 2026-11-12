"""
Distance computation between fingerprints.

The distance is a weighted sum of three components:
    - interleaving distance on persistence diagrams of LCB and Phi
    - Weisfeiler–Lehman kernel distance on the cliff graphs
    - Wasserstein-2 distance on the module-contribution distributions

The weights are the inverse of each component's sample standard deviation,
which makes the composite dimensionless.
"""

from __future__ import annotations

import hashlib
from typing import Iterable

import numpy as np

from janus.stirpes.contracts import Fingerprint


# ─────────────────────────────────────────────────────────────────────
# Component 1: interleaving distance (simplified persistence)
# ─────────────────────────────────────────────────────────────────────


def _persistence_diagram(fingerprint: Fingerprint) -> list[tuple[float, float]]:
    """
    A simplified persistence diagram of the (LCB, Phi) pair per action.

    For each action present in both maps, we produce a pair
    (min(LCB, Phi), max(LCB, Phi)). This is a proxy for the persistence
    of the action's score as we scan the (LCB, Phi) plane. The real
    interleaving distance would require a full sublevel-set filtration;
    the proxy captures the same qualitative structure — which actions
    are "persistent" (small spread) vs. "transient" (large spread).
    """
    lcb = dict(fingerprint.lower_confidence_bound)
    phi = dict(fingerprint.composite_score)
    pairs: list[tuple[float, float]] = []
    for action in sorted(set(lcb) & set(phi)):
        lo = min(lcb[action], phi[action])
        hi = max(lcb[action], phi[action])
        pairs.append((lo, hi))
    return pairs


def _interleaving_component(f: Fingerprint, g: Fingerprint) -> float:
    """Bottleneck-style distance between the simplified diagrams."""
    diag_f = _persistence_diagram(f)
    diag_g = _persistence_diagram(g)
    if not diag_f and not diag_g:
        return 0.0
    # Match each point in diag_f to its nearest point in diag_g and vice
    # versa, take the maximum of the two minimum distances.
    def _min_dist_to(p: tuple[float, float],
                     diag: list[tuple[float, float]]) -> float:
        if not diag:
            return float(abs(p[1] - p[0]))
        return min(
            max(abs(p[0] - q[0]), abs(p[1] - q[1])) for q in diag
        )
    forward = max((_min_dist_to(p, diag_g) for p in diag_f), default=0.0)
    backward = max((_min_dist_to(q, diag_f) for q in diag_g), default=0.0)
    return max(forward, backward)


# ─────────────────────────────────────────────────────────────────────
# Component 2: Weisfeiler–Lehman kernel distance
# ─────────────────────────────────────────────────────────────────────


def _wl_signature(fingerprint: Fingerprint, depth: int = 3) -> dict[str, int]:
    """A Weisfeiler–Lehman-style signature of the topology / survivor graph.

    Nodes are actions in the survivor set. Edges connect actions with
    adjacent LCB values (within the sorted order). Each node is coloured
    by its topology class. The signature counts colour occurrences at
    each depth of the WL refinement.
    """
    survivor = list(fingerprint.survivor_set)
    topology = dict(fingerprint.topology)
    lcb = dict(fingerprint.lower_confidence_bound)

    # Build the adjacency: sorted by LCB, adjacent nodes are connected.
    ordered = sorted(survivor, key=lambda a: lcb.get(a, 0.0))
    adjacency: dict[str, set[str]] = {a: set() for a in survivor}
    for left, right in zip(ordered, ordered[1:]):
        adjacency[left].add(right)
        adjacency[right].add(left)

    # Initial colours: topology class
    colours = {a: topology.get(a, "unknown") for a in survivor}

    # WL refinement
    signature: dict[str, int] = {}
    for _ in range(depth):
        next_colours = {}
        for a in survivor:
            neighbour_colours = tuple(sorted(colours[n] for n in adjacency[a]))
            key = (colours[a], neighbour_colours)
            digest = hashlib.sha256(repr(key).encode()).hexdigest()[:16]
            next_colours[a] = digest
            signature[digest] = signature.get(digest, 0) + 1
        colours = next_colours
    return signature


def _wl_component(f: Fingerprint, g: Fingerprint) -> float:
    """L1 distance between normalized WL signature histograms."""
    sig_f = _wl_signature(f)
    sig_g = _wl_signature(g)
    keys = set(sig_f) | set(sig_g)
    total_f = sum(sig_f.values()) or 1
    total_g = sum(sig_g.values()) or 1
    distance = 0.0
    for key in keys:
        p = sig_f.get(key, 0) / total_f
        q = sig_g.get(key, 0) / total_g
        distance += abs(p - q)
    return distance / 2.0  # Normalize to [0, 1]


# ─────────────────────────────────────────────────────────────────────
# Component 3: Wasserstein-2 on module contributions
# ─────────────────────────────────────────────────────────────────────


def _module_distribution(fingerprint: Fingerprint) -> np.ndarray:
    """The vector of module risk multipliers, one per module name."""
    # Sort by module name for stable ordering.
    sorted_modules = sorted(fingerprint.modules, key=lambda m: m[0])
    return np.array([m[2] for m in sorted_modules], dtype=float)


def _wasserstein2_component(f: Fingerprint, g: Fingerprint) -> float:
    """Wasserstein-2 distance between empirical distributions.

    For one-dimensional distributions, the Wasserstein-2 distance is
    the L² distance between the sorted values. If the two fingerprints
    have different module counts, pad the shorter vector with 1.0
    (the neutral multiplier).
    """
    dist_f = np.sort(_module_distribution(f))
    dist_g = np.sort(_module_distribution(g))
    n = max(len(dist_f), len(dist_g))
    if n == 0:
        return 0.0
    dist_f = np.pad(dist_f, (0, n - len(dist_f)), constant_values=1.0)
    dist_g = np.pad(dist_g, (0, n - len(dist_g)), constant_values=1.0)
    return float(np.sqrt(np.mean((dist_f - dist_g) ** 2)))


# ─────────────────────────────────────────────────────────────────────
# Composed distance
# ─────────────────────────────────────────────────────────────────────


def distance_components(
    f: Fingerprint, g: Fingerprint
) -> tuple[float, float, float]:
    """Return the three components separately."""
    return (
        _interleaving_component(f, g),
        _wl_component(f, g),
        _wasserstein2_component(f, g),
    )


def distance_matrix(
    fingerprints: Iterable[Fingerprint],
    weights: tuple[float, float, float] | None = None,
) -> np.ndarray:
    """Pairwise distance matrix over a set of fingerprints.

    If `weights` is None, computes the inverse-variance weights from the
    sample of components, which normalises each component to unit
    variance. If `weights` is provided, uses it directly.
    """
    fps = list(fingerprints)
    n = len(fps)
    if n < 2:
        return np.zeros((n, n), dtype=float)

    components = np.zeros((n, n, 3), dtype=float)
    for i in range(n):
        for j in range(i + 1, n):
            c = distance_components(fps[i], fps[j])
            components[i, j] = c
            components[j, i] = c

    if weights is None:
        # Compute inverse-variance weights from the off-diagonal components
        off_diag = np.concatenate([
            components[i, j] for i in range(n) for j in range(i + 1, n)
        ])
        variances = off_diag.var(axis=0)
        variances = np.where(variances > 1e-12, variances, 1.0)
        w = 1.0 / np.sqrt(variances)
        w = w / w.sum()
    else:
        w = np.array(weights, dtype=float)

    distances = (components * w).sum(axis=2)
    return distances


def distance(
    f: Fingerprint,
    g: Fingerprint,
    weights: tuple[float, float, float] = (1 / 3, 1 / 3, 1 / 3),
) -> float:
    """Single-pair distance with fixed weights."""
    c = distance_components(f, g)
    return float(sum(w * c_k for w, c_k in zip(weights, c)))