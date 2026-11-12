"""Tests for the STIRPES module."""

import math

import numpy as np
import pytest

from janus.contracts import (
    Action,
    AgopMode,
    AgopResult,
    MarketSnapshot,
    StrategyName,
    TradeIntent,
)
from janus.stirpes.chain import MockChainClient
from janus.stirpes.clade import (
    all_clades,
    clade_hash_for_leaf,
    clade_hash_from_labels,
)
from janus.stirpes.contracts import (
    ClassHash,
    CladeHash,
    Fingerprint,
    PayloadHash,
    SessionId,
    SettlementBatch,
)
from janus.stirpes.distance import (
    distance,
    distance_components,
    distance_matrix,
)
from janus.stirpes.fingerprint import (
    canonical_form,
    class_hash,
    extract_fingerprint,
)
from janus.stirpes.query import QueryEngine
from janus.stirpes.recorder import StirpesRecorder
from janus.stirpes.reveal import XorCipher
from janus.stirpes.signal import blombergs_k, pagels_lambda
from janus.stirpes.tree import build_tree


# ─────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────


def _make_agop_result(
    ranking=("LONG", "FLAT"),
    contract_verified=True,
    nash_dm=(0.0, 1.0),
    nash_cp=(1.0, 0.0),
) -> AgopResult:
    return AgopResult(
        mode=AgopMode.DBC,
        ranking=list(ranking),
        survivor_set=sorted(ranking),
        lower_confidence_bound={a: 0.8 for a in ranking},
        composite_score={a: 0.9 for a in ranking},
        topology_class={a: "T_A" for a in ranking},
        convergence_depth=1,
        capacity=2,
        number_of_weisfeiler_lehman_classes=2,
        contract_verified=contract_verified,
        nash_dm=nash_dm,
        nash_cp=nash_cp,
    )


def _make_intent(action: Action = Action.LONG) -> TradeIntent:
    return TradeIntent(
        action=action,
        position_size=0.05,
        rationale="test",
        agop_mode=AgopMode.DBC,
        strategy=StrategyName.CONSERVATIVE,
    )


def _make_snapshot() -> MarketSnapshot:
    return MarketSnapshot(
        symbol="BTC/USDT",
        price=50000.0,
        expected_return=0.004,
        realized_volatility=0.012,
        slippage=2.0,
        slippage_maximum=20.0,
        venue_risk=0.2,
        signal_agreement=0.6,
        order_flow_imbalance=0.05,
    )


def _make_fingerprint(
    ranking=("LONG", "FLAT"),
    survivor=("LONG", "FLAT"),
    topology=(("FLAT", "T_A"), ("LONG", "T_B")),
    depth=1,
    capacity=2,
    lcb=(("FLAT", 1.0), ("LONG", 0.8)),
    phi=(("FLAT", 1.0), ("LONG", 0.9)),
    verdict="pass",
) -> Fingerprint:
    return Fingerprint(
        ranking=ranking,
        survivor_set=survivor,
        topology=topology,
        convergence_depth=depth,
        capacity=capacity,
        lower_confidence_bound=lcb,
        composite_score=phi,
        nash_dm=(0.0, 1.0),
        nash_cp=(1.0, 0.0),
        nash_entropy=(0.0, 0.0),
        modules=(),
        verdict=verdict,
    )


# ─────────────────────────────────────────────────────────────────────
# Fingerprint extraction
# ─────────────────────────────────────────────────────────────────────


def test_extract_fingerprint_produces_valid_fingerprint():
    fp = extract_fingerprint(
        agop_result=_make_agop_result(),
        module_contexts={},
        verdict="pass",
    )
    assert fp.ranking == ("LONG", "FLAT")
    assert fp.survivor_set == ("FLAT", "LONG")
    assert fp.verdict == "pass"
    assert fp.nash_dm == (0.0, 1.0)
    assert fp.nash_cp == (1.0, 0.0)
    assert fp.nash_entropy == (0.0, 0.0)


def test_extract_fingerprint_uses_module_contexts():
    fp = extract_fingerprint(
        agop_result=_make_agop_result(),
        module_contexts={
            "regime": {
                "phase": "pre_agop",
                "risk_multiplier": 1.0,
                "veto": False,
                "context": {"regime": "calm"},
            }
        },
        verdict="pass",
    )
    assert len(fp.modules) == 1
    name, phase, multiplier, context_hash = fp.modules[0]
    assert name == "regime"
    assert phase == "pre_agop"
    assert multiplier == 1.0
    assert len(context_hash) == 64  # sha256 hex


# ─────────────────────────────────────────────────────────────────────
# Canonical form and class hash
# ─────────────────────────────────────────────────────────────────────


def test_canonical_form_is_deterministic():
    fp = _make_fingerprint()
    assert canonical_form(fp) == canonical_form(fp)


def test_canonical_form_distinguishes_verdicts():
    fp_pass = _make_fingerprint(verdict="pass")
    fp_clamp = _make_fingerprint(verdict="size_clamped")
    assert canonical_form(fp_pass) != canonical_form(fp_clamp)


def test_class_hash_is_32_bytes():
    h = class_hash(_make_fingerprint())
    assert len(h) == 32
    assert isinstance(h, bytes)


def test_same_fingerprint_same_hash():
    assert class_hash(_make_fingerprint()) == class_hash(_make_fingerprint())


def test_different_fingerprint_different_hash():
    fp_1 = _make_fingerprint(verdict="pass")
    fp_2 = _make_fingerprint(verdict="size_clamped")
    assert class_hash(fp_1) != class_hash(fp_2)


# ─────────────────────────────────────────────────────────────────────
# Distance
# ─────────────────────────────────────────────────────────────────────


def test_distance_is_zero_for_identical():
    fp = _make_fingerprint()
    assert distance(fp, fp) == 0.0


def test_distance_is_symmetric():
    fp_a = _make_fingerprint(verdict="pass")
    fp_b = _make_fingerprint(verdict="size_clamped")
    assert abs(distance(fp_a, fp_b) - distance(fp_b, fp_a)) < 1e-12


def test_distance_matrix_is_symmetric():
    fps = [
        _make_fingerprint(verdict="pass"),
        _make_fingerprint(verdict="size_clamped"),
        _make_fingerprint(verdict="contract_collapse"),
    ]
    D = distance_matrix(fps)
    assert D.shape == (3, 3)
    assert np.allclose(D, D.T)
    assert np.allclose(np.diag(D), 0.0)


# ─────────────────────────────────────────────────────────────────────
# Tree
# ─────────────────────────────────────────────────────────────────────


def test_tree_leaf_count():
    labels = ["a", "b", "c", "d"]
    D = np.array([
        [0.0, 1.0, 2.0, 3.0],
        [1.0, 0.0, 2.0, 3.0],
        [2.0, 2.0, 0.0, 1.0],
        [3.0, 3.0, 1.0, 0.0],
    ])
    tree = build_tree(labels, D, method="neighbor_joining")
    assert len(tree.leaves) == 4


# ─────────────────────────────────────────────────────────────────────
# Clade
# ─────────────────────────────────────────────────────────────────────


def test_clade_hash_is_deterministic():
    hashes = {"a": b"\x01" * 32, "b": b"\x02" * 32, "c": b"\x03" * 32}
    h_1 = clade_hash_from_labels({"a", "b"}, hashes)
    h_2 = clade_hash_from_labels({"b", "a"}, hashes)
    assert h_1 == h_2


def test_clade_hash_depends_on_membership():
    hashes = {"a": b"\x01" * 32, "b": b"\x02" * 32, "c": b"\x03" * 32}
    h_ab = clade_hash_from_labels({"a", "b"}, hashes)
    h_ac = clade_hash_from_labels({"a", "c"}, hashes)
    assert h_ab != h_ac


# ─────────────────────────────────────────────────────────────────────
# Signal tests
# ─────────────────────────────────────────────────────────────────────


def test_pagels_lambda_returns_value_in_range():
    labels = ["a", "b", "c", "d", "e"]
    D = np.array([
        [0.0, 1.0, 3.0, 4.0, 5.0],
        [1.0, 0.0, 3.0, 4.0, 5.0],
        [3.0, 3.0, 0.0, 2.0, 3.0],
        [4.0, 4.0, 2.0, 0.0, 1.0],
        [5.0, 5.0, 3.0, 1.0, 0.0],
    ])
    tree = build_tree(labels, D, method="neighbor_joining", root=True)
    trait = {"a": 1.0, "b": 1.1, "c": 2.0, "d": 2.2, "e": 2.1}
    lam = pagels_lambda(tree, trait)
    assert 0.0 <= lam <= 1.0


def test_blombergs_k_returns_value():
    labels = ["a", "b", "c", "d", "e"]
    D = np.array([
        [0.0, 1.0, 3.0, 4.0, 5.0],
        [1.0, 0.0, 3.0, 4.0, 5.0],
        [3.0, 3.0, 0.0, 2.0, 3.0],
        [4.0, 4.0, 2.0, 0.0, 1.0],
        [5.0, 5.0, 3.0, 1.0, 0.0],
    ])
    tree = build_tree(labels, D, method="neighbor_joining", root=True)
    trait = {"a": 1.0, "b": 1.1, "c": 2.0, "d": 2.2, "e": 2.1}
    k = blombergs_k(tree, trait)
    assert not math.isnan(k)


# ─────────────────────────────────────────────────────────────────────
# Recorder (rewritten to actually call record())
# ─────────────────────────────────────────────────────────────────────


def test_recorder_records_and_auto_flushes():
    chain = MockChainClient()
    cipher = XorCipher()
    recorder = StirpesRecorder(chain=chain, cipher=cipher, flush_threshold=3)

    for _ in range(3):
        recorder.record(
            agop_result=_make_agop_result(),
            module_contexts={},
            snapshot=_make_snapshot(),
            verdict="pass",
        )

    # Auto-flush triggered at threshold.
    assert len(recorder.pending) == 0
    # A manual flush now returns None because nothing is pending.
    assert recorder.flush() is None


def test_recorder_settles_batch():
    chain = MockChainClient()
    cipher = XorCipher()
    recorder = StirpesRecorder(chain=chain, cipher=cipher, flush_threshold=1000)

    for verdict in ["pass", "size_clamped", "contract_collapse"]:
        recorder.record(
            agop_result=_make_agop_result(),
            module_contexts={},
            snapshot=_make_snapshot(),
            verdict=verdict,
        )

    batch = recorder.flush()
    assert batch is not None
    assert len(batch.tick_hashes) == 3
    # All three ticks have distinct verdicts, hence distinct fingerprints.
    assert len(set(batch.class_hashes)) == 3

    tx_hash = recorder.settle(batch)
    assert isinstance(tx_hash, bytes)
    assert len(tx_hash) == 32

    records = recorder.query_by_session(SessionId("default-session"))
    assert len(records) == 3

    by_clade = recorder.query_by_clade(batch.clade_hashes[0])
    assert len(by_clade) >= 1


def test_recorder_historical_leaf_set_persists():
    chain = MockChainClient()
    cipher = XorCipher()
    recorder = StirpesRecorder(chain=chain, cipher=cipher, flush_threshold=1000)

    # First batch: two distinct verdicts -> two leaves.
    for verdict in ["pass", "size_clamped"]:
        recorder.record(
            agop_result=_make_agop_result(),
            module_contexts={},
            snapshot=_make_snapshot(),
            verdict=verdict,
        )
    batch_1 = recorder.flush()
    assert batch_1 is not None
    assert len(recorder._leaf_fingerprints) == 2

    # Second batch: two more verdicts -> four leaves total.
    for verdict in ["contract_collapse", "toxicity_collapse"]:
        recorder.record(
            agop_result=_make_agop_result(),
            module_contexts={},
            snapshot=_make_snapshot(),
            verdict=verdict,
        )
    batch_2 = recorder.flush()
    assert batch_2 is not None
    assert len(recorder._leaf_fingerprints) == 4


def test_recorder_singleton_leaf():
    chain = MockChainClient()
    cipher = XorCipher()
    recorder = StirpesRecorder(chain=chain, cipher=cipher, flush_threshold=1000)

    recorder.record(
        agop_result=_make_agop_result(),
        module_contexts={},
        snapshot=_make_snapshot(),
        verdict="pass",
    )
    batch = recorder.flush()
    assert batch is not None
    assert len(batch.tick_hashes) == 1
    assert len(batch.clade_hashes[0]) == 32


# ─────────────────────────────────────────────────────────────────────
# Chain and query
# ─────────────────────────────────────────────────────────────────────


def test_chain_commit_and_query():
    chain = MockChainClient()

    class_hash_value = b"\x01" * 32
    clade_hash_value = b"\x02" * 32
    tick_hash_value = b"\x03" * 32
    session = SessionId("s1")
    payload = PayloadHash(b"\x04" * 32)

    batch = SettlementBatch(
        tick_hashes=(tick_hash_value,),
        class_hashes=(ClassHash(class_hash_value),),
        clade_hashes=(CladeHash(clade_hash_value),),
        session_ids=(session,),
        tick_indices=(0,),
        payload_hashes=(payload,),
        leaf_set_hash=b"\x05" * 32,
        tree_root_hash=b"\x06" * 32,
    )
    tx = chain.commit(batch)
    assert len(tx) == 32

    records = chain.query(clade_hash=clade_hash_value)
    assert len(records) == 1
    assert records[0].tick_hash == tick_hash_value


def test_query_engine_by_clade():
    chain = MockChainClient()
    engine = QueryEngine(chain=chain)
    assert engine.by_clade(CladeHash(b"\x02" * 32)) == []


# ─────────────────────────────────────────────────────────────────────
# Unidirectionality
# ─────────────────────────────────────────────────────────────────────


def test_stirpes_does_not_import_janus_orchestrator():
    """The unidirectionality property, structurally: stirpes modules must
    not import from janus.orchestrator or janus.api."""
    import janus.stirpes as stirpes_pkg
    import inspect

    for name in dir(stirpes_pkg):
        obj = getattr(stirpes_pkg, name)
        if inspect.ismodule(obj):
            source = inspect.getsource(obj)
            assert "from janus.orchestrator" not in source, (
                f"{name} imports from janus.orchestrator"
            )
            assert "from janus.api" not in source, (
                f"{name} imports from janus.api"
            )