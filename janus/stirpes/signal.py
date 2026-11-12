"""
Phylogenetic signal tests: Pagel's λ and Blomberg's K.
"""

from __future__ import annotations

import numpy as np
from scipy import optimize

from janus.stirpes.tree import PhylogeneticTree


def _covariance_matrix(
    tree: PhylogeneticTree,
    leaves: list[str],
    sigma_squared: float = 1.0,
) -> np.ndarray:
    """Brownian motion covariance matrix: Cov[i,j] = sigma^2 * d_T(leaf_i, leaf_j)."""
    n = len(leaves)
    C = np.zeros((n, n), dtype=float)
    for i, a in enumerate(leaves):
        for j, b in enumerate(leaves):
            if i == j:
                # Variance of a single tip equals its distance to the root.
                C[i, j] = sigma_squared * _distance_to_root(tree, a)
            else:
                C[i, j] = sigma_squared * tree.path_distance(a, b)
    return C


def _distance_to_root(tree: PhylogeneticTree, leaf: str) -> float:
    node = tree._find_node(leaf)
    distance = 0.0
    while node.parent is not None:
        distance += node.length
        node = node.parent
    return distance


def pagels_lambda(
    tree: PhylogeneticTree,
    trait: dict[str, float],
    leaves: list[str] | None = None,
) -> float:
    """Maximum-likelihood estimate of Pagel's λ.

    Λ ranges from 0 (no phylogenetic signal) to 1 (full Brownian motion).
    Values above 1 indicate more signal than expected under BM.
    """
    if leaves is None:
        leaves = sorted(tree.leaves)
    if len(leaves) < 3:
        raise ValueError("need at least 3 leaves")

    x = np.array([trait[leaf] for leaf in leaves], dtype=float)
    n = len(x)
    x_centered = x - x.mean()

    C = _covariance_matrix(tree, leaves)
    diag_C = np.diag(np.diag(C))

    def neg_log_likelihood(lambda_value: float) -> float:
        if lambda_value < 0 or lambda_value > 2.0:
            return float("inf")
        V = lambda_value * C + (1 - lambda_value) * diag_C
        try:
            V_inv = np.linalg.inv(V)
            sign, log_det = np.linalg.slogdet(V)
            if sign <= 0:
                return float("inf")
        except np.linalg.LinAlgError:
            return float("inf")
        quadratic = float(x_centered @ V_inv @ x_centered)
        return 0.5 * (n * np.log(quadratic / n) + log_det + n)

    result = optimize.minimize_scalar(
        neg_log_likelihood,
        bounds=(0.0, 1.0),
        method="bounded",
    )
    return float(result.x)


def blombergs_k(
    tree: PhylogeneticTree,
    trait: dict[str, float],
    leaves: list[str] | None = None,
) -> float:
    """Blomberg's K.

    K = 1 indicates that trait variation matches BM expectations.
    K > 1 indicates more phylogenetic signal than BM (conservatism).
    K < 1 indicates less (convergence or noise).
    """
    if leaves is None:
        leaves = sorted(tree.leaves)
    n = len(leaves)
    if n < 3:
        raise ValueError("need at least 3 leaves")

    x = np.array([trait[leaf] for leaf in leaves], dtype=float)
    x_centered = x - x.mean()

    C = _covariance_matrix(tree, leaves)
    try:
        C_inv = np.linalg.inv(C)
    except np.linalg.LinAlgError:
        return float("nan")

    mse_observed = float(x_centered @ C_inv @ x_centered) / (n - 1)

    # MSE under Brownian motion: sum of standardized contrasts.
    # For a star phylogeny, all pairwise distances are equal, so the
    # covariance matrix has a simple form: diagonal = 2*root_depth,
    # off-diagonal = 2*root_depth. The expected MSE under star is
    # just the sample variance times a factor.
    root_depth = _distance_to_root(tree, leaves[0])
    mse_bm = float(np.var(x_centered, ddof=1))

    # Approximate star covariance
    star_variance = root_depth
    mse_star = float(np.var(x_centered, ddof=1) * (n - 1) / n + star_variance / n)

    if mse_bm <= 0:
        return float("nan")

    K = (mse_observed / mse_bm) / (mse_observed / mse_star) if mse_observed > 0 else float("nan")
    return float(K)