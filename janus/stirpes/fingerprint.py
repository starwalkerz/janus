"""
Fingerprint extraction and canonical form.

The fingerprint is a deterministic function of the AGOP output and the
module contributions. Its canonical form is the unique byte string such
that two fingerprints are equal iff their canonical forms are equal.

Note on approximations: this module uses the Weisfeiler-Lehman kernel
distance as the discrete component of the fingerprint distance, and the
Wasserstein-2 distance on module multipliers as the continuous component.
Both are called out explicitly in the docstrings. The Pagel's lambda and
Blomberg's K signal tests in signal.py are also approximate — see their
docstrings.
"""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any

from janus.contracts import AgopResult
from janus.stirpes.contracts import (
    ClassHash,
    Fingerprint,
    PayloadHash,
    VERDICT_PASS,
)


# Rounding precision for continuous components.
ROUND_DIGITS = 6


def _round(value: float) -> float:
    return round(float(value), ROUND_DIGITS)


def _shannon_entropy(probabilities: tuple[float, ...]) -> float:
    total = 0.0
    for p in probabilities:
        if p > 0.0:
            total -= p * math.log2(p)
    return round(total, ROUND_DIGITS)


def extract_fingerprint(
    agop_result: AgopResult,
    module_contexts: dict[str, dict[str, Any]],
    verdict: str = VERDICT_PASS,
) -> Fingerprint:
    """Extract the fingerprint from a completed JANUS tick.

    Parameters
    ----------
    agop_result       : the normalised AgopResult from the bridge
    module_contexts   : a map from module name to its flattened context
                        dict, produced by the orchestrator's
                        last_module_contexts attribute
    verdict           : the verifier's code for this tick

    Returns
    -------
    A Fingerprint with all fields populated and pre-rounded.
    """
    # Discrete components.
    ranking = tuple(agop_result.ranking)
    survivor_set = tuple(sorted(agop_result.survivor_set))
    topology = tuple(sorted(agop_result.topology_class.items()))
    convergence_depth = int(agop_result.convergence_depth)
    capacity = (
        int(agop_result.capacity) if agop_result.capacity is not None else None
    )

    # Continuous components.
    lower_confidence_bound = tuple(sorted(
        (action, _round(value))
        for action, value in agop_result.lower_confidence_bound.items()
    ))
    composite_score = tuple(sorted(
        (action, _round(value))
        for action, value in agop_result.composite_score.items()
    ))

    # Nash strategies come from AgopResult now, not from State.
    sigma_dm = tuple(_round(float(p)) for p in agop_result.nash_dm)
    sigma_cp = tuple(_round(float(p)) for p in agop_result.nash_cp)
    nash_entropy = (
        _shannon_entropy(sigma_dm),
        _shannon_entropy(sigma_cp),
    )

    # Module contributions, canonicalised by context hash.
    modules = []
    for name in sorted(module_contexts):
        context = module_contexts[name]
        phase = context.get("phase", "unknown")
        multiplier = _round(float(context.get("risk_multiplier", 1.0)))
        context_bytes = json.dumps(
            context,
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        ).encode("utf-8")
        context_hash = hashlib.sha256(context_bytes).hexdigest()
        modules.append((name, phase, multiplier, context_hash))
    modules_tuple = tuple(modules)

    return Fingerprint(
        ranking=ranking,
        survivor_set=survivor_set,
        topology=topology,
        convergence_depth=convergence_depth,
        capacity=capacity,
        lower_confidence_bound=lower_confidence_bound,
        composite_score=composite_score,
        nash_dm=sigma_dm,
        nash_cp=sigma_cp,
        nash_entropy=nash_entropy,
        modules=modules_tuple,
        verdict=verdict,
    )


def canonical_form(fingerprint: Fingerprint) -> bytes:
    """The unique canonical byte string of a fingerprint.

    The canonical form is JSON with sorted keys, compact separators, and
    floating-point values already pre-rounded by extract_fingerprint.
    """
    payload = {
        "ranking": list(fingerprint.ranking),
        "survivor_set": list(fingerprint.survivor_set),
        "topology": [list(pair) for pair in fingerprint.topology],
        "convergence_depth": fingerprint.convergence_depth,
        "capacity": fingerprint.capacity,
        "lower_confidence_bound": [
            [action, value] for action, value in fingerprint.lower_confidence_bound
        ],
        "composite_score": [
            [action, value] for action, value in fingerprint.composite_score
        ],
        "nash_dm": list(fingerprint.nash_dm),
        "nash_cp": list(fingerprint.nash_cp),
        "nash_entropy": list(fingerprint.nash_entropy),
        "modules": [
            [name, phase, multiplier, context_hash]
            for name, phase, multiplier, context_hash in fingerprint.modules
        ],
        "verdict": fingerprint.verdict,
    }
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def class_hash(fingerprint: Fingerprint) -> ClassHash:
    """Definition 3: SHA256 of the canonical form."""
    return ClassHash(hashlib.sha256(canonical_form(fingerprint)).digest())


def payload_hash(ciphertext: bytes) -> PayloadHash:
    """Hash of the encrypted payload, for on-chain storage."""
    return PayloadHash(hashlib.sha256(ciphertext).digest())


def snapshot_hash(snapshot: Any) -> bytes:
    """Deterministic hash of a market snapshot."""
    payload = json.dumps(
        {
            "symbol": snapshot.symbol,
            "price": round(float(snapshot.price), ROUND_DIGITS),
            "expected_return": round(
                float(snapshot.expected_return), ROUND_DIGITS
            ),
            "realized_volatility": round(
                float(snapshot.realized_volatility), ROUND_DIGITS
            ),
            "slippage": round(float(snapshot.slippage), ROUND_DIGITS),
            "slippage_maximum": round(
                float(snapshot.slippage_maximum), ROUND_DIGITS
            ),
            "venue_risk": round(float(snapshot.venue_risk), ROUND_DIGITS),
            "signal_agreement": round(
                float(snapshot.signal_agreement), ROUND_DIGITS
            ),
            "order_flow_imbalance": round(
                float(snapshot.order_flow_imbalance), ROUND_DIGITS
            ),
            "history_length": len(snapshot.history),
            "timestamps_length": len(snapshot.timestamps),
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).digest()