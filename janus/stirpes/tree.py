"""
Phylogenetic tree construction.

Implements:
    - Neighbor-Joining (Saitou & Nei 1987)
    - UPGMA (Sokal & Michener 1958)
    - Fitch parsimony for discrete characters
    - Midpoint rooting
    - Tree utilities (path distance, clade, LCA)
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from janus.stirpes.contracts import Fingerprint


# ─────────────────────────────────────────────────────────────────────
# Tree data structure
# ─────────────────────────────────────────────────────────────────────


@dataclass
class TreeNode:
    """A node in a phylogenetic tree."""
    label: str
    children: list["TreeNode"] = field(default_factory=list)
    parent: "TreeNode | None" = None
    length: float = 0.0  # branch length to parent

    def is_leaf(self) -> bool:
        return len(self.children) == 0


@dataclass
class PhylogeneticTree:
    """A weighted rooted tree with leaves labelled by class hashes."""
    root: TreeNode
    leaves: dict[str, TreeNode]  # label -> TreeNode

    def clade(self, label: str) -> frozenset[str]:
        """Return the set of leaf labels descended from the node with this label.

        If `label` is a leaf, returns the singleton. If `label` is an
        internal node, returns all leaves under it. If `label` is not
        found, raises KeyError.
        """
        node = self._find_node(label)
        if node is None:
            raise KeyError(f"node {label!r} not found")
        return self._leaves_under(node)

    def lca(self, a: str, b: str) -> TreeNode:
        """Return the lowest common ancestor of two leaves."""
        ancestors_a = self._ancestors(self._find_node(a))
        ancestors_b = self._ancestors(self._find_node(b))
        for node_a in ancestors_a:
            if node_a in ancestors_b:
                return node_a
        raise RuntimeError("tree is disconnected")

    def path_distance(self, a: str, b: str) -> float:
        """Total edge weight along the path from leaf a to leaf b."""
        return self._distance(self._find_node(a), self._find_node(b))

    def internal_nodes(self) -> list[TreeNode]:
        """All non-leaf nodes."""
        result = []
        def _walk(node: TreeNode) -> None:
            if not node.is_leaf():
                result.append(node)
                for child in node.children:
                    _walk(child)
        _walk(self.root)
        return result

    # ── internals ──────────────────────────────────────────────────

    def _find_node(self, label: str) -> TreeNode | None:
        if label in self.leaves:
            return self.leaves[label]
        def _walk(node: TreeNode) -> TreeNode | None:
            if node.label == label:
                return node
            for child in node.children:
                found = _walk(child)
                if found is not None:
                    return found
            return None
        return _walk(self.root)

    def _leaves_under(self, node: TreeNode) -> frozenset[str]:
        if node.is_leaf():
            return frozenset([node.label])
        result = set()
        for child in node.children:
            result |= self._leaves_under(child)
        return frozenset(result)

    def _ancestors(self, node: TreeNode | None) -> list[TreeNode]:
        result = []
        while node is not None:
            result.append(node)
            node = node.parent
        return result

    def _distance(self, a: TreeNode, b: TreeNode) -> float:
        ancestors_a = self._ancestors(a)
        ancestors_b = self._ancestors(b)
        ancestor_set_b = {id(n): n for n in ancestors_b}
        for node in ancestors_a:
            if id(node) in ancestor_set_b:
                lca = node
                break
        else:
            raise RuntimeError("no common ancestor")
        dist_a = sum(n.length for n in ancestors_a if n is not lca)
        dist_b = sum(n.length for n in ancestors_b if n is not lca)
        return float(dist_a + dist_b)


# ─────────────────────────────────────────────────────────────────────
# Neighbor-Joining
# ─────────────────────────────────────────────────────────────────────


def _neighbor_joining(
    labels: list[str],
    distances: np.ndarray,
) -> PhylogeneticTree:
    """Saitou–Nei neighbor-joining.

    Returns an unrooted tree; call `midpoint_root` afterward.
    """
    n = len(labels)
    if n < 2:
        raise ValueError("need at least 2 leaves")

    # Mutable state
    active_labels = list(labels)
    D = distances.copy().astype(float)
    # Node registry: label -> TreeNode, with internal nodes named U1, U2, ...
    nodes: dict[str, TreeNode] = {
        label: TreeNode(label=label) for label in labels
    }
    next_internal = 1

    while len(active_labels) > 2:
        n_current = len(active_labels)
        # Compute Q-criterion
        r = D.sum(axis=1)
        Q = (n_current - 2) * D - r[:, None] - r[None, :]
        np.fill_diagonal(Q, np.inf)

        # Find minimum
        i, j = np.unravel_index(np.argmin(Q), Q.shape)
        label_i, label_j = active_labels[i], active_labels[j]

        # Compute branch lengths from i and j to new node u
        d_ij = D[i, j]
        length_i = 0.5 * d_ij + (r[i] - r[j]) / (2 * (n_current - 2))
        length_j = d_ij - length_i

        # Create the new internal node
        u_label = f"U{next_internal}"
        next_internal += 1
        u_node = TreeNode(label=u_label)
        node_i = nodes[label_i]
        node_j = nodes[label_j]
        node_i.parent = u_node
        node_j.parent = u_node
        node_i.length = max(0.0, length_i)
        node_j.length = max(0.0, length_j)
        u_node.children = [node_i, node_j]
        nodes[u_label] = u_node

        # New distance row: d(u, k) = 0.5 * (d(i,k) + d(j,k) - d(i,j))
        new_distances = 0.5 * (D[i, :] + D[j, :] - d_ij)
        # Remove i, j; add u at the end
        keep = [k for k in range(n_current) if k not in (i, j)]
        D_new = np.zeros((n_current - 1, n_current - 1), dtype=float)
        D_new[:-1, :-1] = D[np.ix_(keep, keep)]
        new_row = new_distances[keep]
        D_new[:-1, -1] = new_row
        D_new[-1, :-1] = new_row
        D = D_new

        active_labels = [active_labels[k] for k in keep] + [u_label]

    # Final merge of the last two nodes
    final_i, final_j = active_labels[0], active_labels[1]
    d_final = D[0, 1]
    root_node = TreeNode(label="ROOT")
    node_i = nodes[final_i]
    node_j = nodes[final_j]
    node_i.parent = root_node
    node_j.parent = root_node
    node_i.length = max(0.0, d_final / 2.0)
    node_j.length = max(0.0, d_final / 2.0)
    root_node.children = [node_i, node_j]

    leaves = {label: nodes[label] for label in labels}
    return PhylogeneticTree(root=root_node, leaves=leaves)


# ─────────────────────────────────────────────────────────────────────
# UPGMA
# ─────────────────────────────────────────────────────────────────────


def _upgma(
    labels: list[str],
    distances: np.ndarray,
) -> PhylogeneticTree:
    """Unweighted Pair Group Method with Arithmetic Mean.

    Assumes ultrametric distances. Useful as a baseline.
    """
    n = len(labels)
    if n < 2:
        raise ValueError("need at least 2 leaves")

    clusters: dict[int, TreeNode] = {
        i: TreeNode(label=label) for i, label in enumerate(labels)
    }
    cluster_members: dict[int, set[int]] = {i: {i} for i in range(n)}
    D = {i: {j: float(distances[i, j]) for j in range(n) if j != i} for i in range(n)}
    heights: dict[int, float] = {i: 0.0 for i in range(n)}
    next_internal = 1
    active = set(range(n))

    while len(active) > 1:
        # Find minimum distance pair
        best_pair = None
        best_d = float("inf")
        for i in active:
            for j in active:
                if i < j and D[i][j] < best_d:
                    best_d = D[i][j]
                    best_pair = (i, j)
        if best_pair is None:
            raise RuntimeError("no pair found")
        i, j = best_pair

        # New height is half the merge distance
        new_height = best_d / 2.0
        u_label = f"U{next_internal}"
        next_internal += 1
        u_node = TreeNode(label=u_label)
        node_i = clusters[i]
        node_j = clusters[j]
        node_i.parent = u_node
        node_j.parent = u_node
        node_i.length = max(0.0, new_height - heights[i])
        node_j.length = max(0.0, new_height - heights[j])
        u_node.children = [node_i, node_j]

        # New distance to each remaining cluster
        new_members = cluster_members[i] | cluster_members[j]
        new_u = next(k for k in range(next_internal * 100) if k not in clusters)
        # (the next_internal counter is already incremented; use a fresh id)
        u = len(clusters)
        clusters[u] = u_node
        cluster_members[u] = new_members
        heights[u] = new_height
        D[u] = {}
        for k in active - {i, j}:
            weighted = (
                len(cluster_members[i]) * D[i][k]
                + len(cluster_members[j]) * D[j][k]
            ) / len(new_members)
            D[u][k] = weighted
            D[k][u] = weighted
        # Remove i, j
        for k in active - {i, j}:
            del D[k][i]
            del D[k][j]
        del D[i]
        del D[j]
        active -= {i, j}
        active.add(u)

    final = next(iter(active))
    root_node = clusters[final]
    leaves = {label: TreeNode(label=label) for label in labels}
    # Rebuild leaves with parent pointers already set by UPGMA
    def _walk(node: TreeNode) -> None:
        if node.is_leaf():
            leaves[node.label] = node
        else:
            for child in node.children:
                _walk(child)
    _walk(root_node)
    return PhylogeneticTree(root=root_node, leaves=leaves)


# ─────────────────────────────────────────────────────────────────────
# Fitch parsimony
# ─────────────────────────────────────────────────────────────────────


def _fitch_score(
    tree: PhylogeneticTree,
    characters: list[tuple[str, ...]],  # characters[leaf_idx] = tuple of states
    leaf_labels: list[str],
) -> int:
    """Fitch parsimony score for a tree and a set of characters.

    Each character is a discrete trait with a small state set. The
    Fitch algorithm assigns sets of possible states to internal nodes
    and counts the number of state changes.
    """
    char_map = dict(zip(leaf_labels, characters))
    total_score = 0
    for char_index in range(len(characters[0])):
        score = _fitch_single(tree.root, char_map, char_index)
        total_score += score[1]
    return total_score


def _fitch_single(
    node: TreeNode,
    char_map: dict[str, tuple[str, ...]],
    char_index: int,
) -> tuple[frozenset[str], int]:
    """Return (state set, score) for the subtree rooted at node."""
    if node.is_leaf():
        return frozenset([char_map[node.label][char_index]]), 0
    child_sets_scores = [_fitch_single(child, char_map, char_index) for child in node.children]
    state_sets = [s for s, _ in child_sets_scores]
    scores = [c for _, c in child_sets_scores]
    # Intersection
    intersection = set(state_sets[0])
    for s in state_sets[1:]:
        intersection &= s
    if intersection:
        return frozenset(intersection), sum(scores)
    # Union + penalty
    union = set(state_sets[0])
    for s in state_sets[1:]:
        union |= s
    return frozenset(union), sum(scores) + 1


# ─────────────────────────────────────────────────────────────────────
# Rooting
# ─────────────────────────────────────────────────────────────────────


def midpoint_root(tree: PhylogeneticTree) -> PhylogeneticTree:
    """Reroot the tree at the midpoint of the longest leaf-to-leaf path."""
    # Find the pair with maximum path distance
    leaves = list(tree.leaves)
    best_pair = (leaves[0], leaves[1])
    best_distance = tree.path_distance(*best_pair)
    for i, a in enumerate(leaves):
        for b in leaves[i + 1:]:
            d = tree.path_distance(a, b)
            if d > best_distance:
                best_distance = d
                best_pair = (a, b)
    # The midpoint lies on the path between the two leaves. We need to
    # insert a new node at that midpoint. For simplicity, we reroot at
    # the node closest to the midpoint.
    a, b = best_pair
    target_distance = best_distance / 2.0
    node = tree._find_node(a)
    accumulated = 0.0
    ancestors = tree._ancestors(node)
    path_to_b = tree._ancestors(tree._find_node(b))
    path_to_b_ids = {id(n) for n in path_to_b}
    lca = next(n for n in ancestors if id(n) in path_to_b_ids)
    # Walk from a to lca, accumulating
    current = tree._find_node(a)
    while current is not lca:
        if accumulated + current.length >= target_distance:
            break
        accumulated += current.length
        current = current.parent
    new_root = current
    # Reroot: reverse the parent chain
    _reroot(tree, new_root)
    return tree


def _reroot(tree: PhylogeneticTree, new_root: TreeNode) -> None:
    """Reverse the parent chain so that new_root becomes the root."""
    # Collect the path from new_root to old root
    path = []
    node = new_root
    while node is not None:
        path.append(node)
        node = node.parent
    # Reverse: each node's parent becomes its child, except the last
    for i in range(len(path) - 1):
        child = path[i]
        parent = path[i + 1]
        child.parent = parent
        # Update children lists
        if child in parent.children:
            parent.children.remove(child)
        if parent not in child.children:
            child.children.append(parent)
    # The last node was the old root; its parent is None, and it now
    # has one child (the previous root). Set new_root.parent = None.
    path[-1].parent = None
    tree.root = path[0]


# ─────────────────────────────────────────────────────────────────────
# Public entry point
# ─────────────────────────────────────────────────────────────────────


def build_tree(
    labels: list[str],
    distances: np.ndarray,
    method: str = "neighbor_joining",
    root: bool = True,
) -> PhylogeneticTree:
    """Build a phylogenetic tree from a distance matrix.

    Parameters
    ----------
    labels    : leaf labels (typically hex class hashes)
    distances : square symmetric distance matrix
    method    : "neighbor_joining" (default), "upgma", or "parsimony"
    root      : whether to apply midpoint rooting (default True)

    Returns
    -------
    A PhylogeneticTree.
    """
    n = len(labels)
    if distances.shape != (n, n):
        raise ValueError(
            f"distance matrix shape {distances.shape} does not match {n} labels"
        )

    if method == "neighbor_joining":
        tree = _neighbor_joining(labels, distances)
    elif method == "upgma":
        tree = _upgma(labels, distances)
    else:
        raise ValueError(f"unknown method {method!r}")

    if root:
        midpoint_root(tree)
    return tree