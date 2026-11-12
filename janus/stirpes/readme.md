# STIRPES

Phylogenetic classification and on-chain attestation for JANUS solutions.

---

## Table of contents

1. Overview
2. Formal definitions
3. Theorems
4. Complexity
5. Architecture
6. Installation
7. Complete usage tutorial
8. Complete API reference
9. Limitations
10. License

---

## 1. Overview

Every JANUS tick produces a solution. STIRPES extracts its fingerprint,
computes its canonical form, hashes it into a class identifier, and —
via a phylogenetic tree over the accumulated leaf set — assigns it to a
clade. The class hash and the clade hash are committed to a settlement
layer alongside the tick identifier. The settlement layer is queryable
by either hash. The full solution remains off-chain, encrypted, and
revealed against payment of a token.

STIRPES is *unidirectional*: it reads from the orchestrator and writes
to the chain. It never reads from the chain and writes to the
orchestrator. The consequence is that JANUS's own development is not
driven by its phylogenetic self-classification, which would collapse the
exploration budget onto the dominant clade. The data is a public good;
it is not a training signal for the producer.

STIRPES provides:

- A typed fingerprint of every JANUS tick, canonicalised to bytes.
- A cryptographic class hash that identifies the fingerprint's cell.
- A moduli-space distance between fingerprints, composed of three
  components (persistence, Weisfeiler–Lehman, Wasserstein).
- A Neighbor-Joining (or UPGMA) phylogenetic tree over the leaf set.
- A clade hash that identifies each internal-node clade.
- Two phylogenetic signal tests (Pagel's λ, Blomberg's K) that report
  whether the tree structure is informative.
- A recorder that batches ticks, rebuilds the tree, and emits
  settlement records.
- An abstract chain client with mock and Tezos implementations.
- A query engine for by-tick, by-clade, and by-session lookups.
- A token-gated reveal mechanism for encrypted payloads.

---

## 2. Formal definitions

### Definition 1 — Fingerprint

Let `S` be the AGOP output after phase 11 of a JANUS tick, expressed as
an `AgopResult`. The fingerprint `f = φ(AgopResult, modules, verdict)` is
the tuple

    f = (ranking, survivor_set, topology, depth, capacity,
         lower_confidence_bound, composite_score,
         nash_pair, nash_entropy, modules, verdict)

where:

- `ranking` is the ordered list of actions in `AgopResult.ranking`.
- `survivor_set` is `sorted(AgopResult.survivor_set)`.
- `topology` is the map from action to Weisfeiler–Lehman class in
  `AgopResult.topology_class`.
- `depth` is `AgopResult.convergence_depth`.
- `capacity` is `AgopResult.capacity` or `None` in legacy mode.
- `lower_confidence_bound` is the map `AgopResult.lower_confidence_bound`
  rounded to six decimals.
- `composite_score` is the map `AgopResult.composite_score` rounded to
  six decimals.
- `nash_pair` is `(AgopResult.nash_dm, AgopResult.nash_cp)` rounded to
  six decimals.
- `nash_entropy` is `(H(AgopResult.nash_dm), H(AgopResult.nash_cp))` in
  bits.
- `modules` is the map from module name to `(phase, risk_multiplier,
  context_hash)`.
- `verdict` is the verifier's code.

The fingerprint is a deterministic function of `(snapshot,
configuration, seed, llm output, verifier verdict)`. Two ticks with
identical AGOP output, identical module contributions, and identical
verdicts produce identical fingerprints.

### Definition 2 — Canonical form

The canonical form `κ(f)` is the byte string obtained by serialising `f`
as UTF-8 encoded JSON with sorted keys, no whitespace, and floating-point
values rounded to six decimal places. The canonical form is unique:
`κ(f) = κ(f')` if and only if `f = f'` under the rounding equivalence.

### Definition 3 — Class hash

The class hash is

    class_hash(f) = SHA256(κ(f))

a 32-byte value. The class hash is the identifier of the *cell* the
fingerprint occupies: it is stable within the rounding equivalence and
differentiable across cells.

### Definition 4 — Distance

Let `D_interleave` be the *approximate* interleaving distance between the
persistence diagrams of the lower-confidence-bound and composite-score
functions (see `distance.py`, `_interleaving_component` — this uses a
bottleneck-style proxy rather than the full sublevel-set filtration);
`D_WL` the Weisfeiler–Lehman kernel distance between the cliff graphs of
the topology and survivor-set structures; and `D_Wasserstein` the
Wasserstein-2 distance between the module-contribution distributions. The
moduli-space distance is

    d(f, g) = w₁ · D_interleave(f, g)
            + w₂ · D_WL(f, g)
            + w₃ · D_Wasserstein(f, g)

with default weights `w₁ = w₂ = w₃ = 1 / σ` where `σ` is the sample
standard deviation of each component over the leaf set. This
normalisation puts the three components on equal footing and makes `d`
dimensionless.

### Definition 5 — Phylogenetic tree

A phylogenetic tree on the leaf set `L` is a weighted rooted tree
`T = (V, E, w, r)` where `L ⊆ V` is the leaf set, `w : E → [0, ∞)`
assigns non-negative edge weights, and `r ∈ V` is the root. The tree
defines a path distance `d_T(a, b)` for every pair of leaves, equal to
the sum of edge weights on the path from `a` to `b`.

### Definition 6 — Clade

For any node `u ∈ V`, the clade of `u` is

    clade(u) = { ℓ ∈ L : u is an ancestor of ℓ }

The clade of a leaf is the singleton `{ℓ}`. The clade of the root is
`L`. Every leaf belongs to a nested sequence of clades.

### Definition 7 — Clade hash

For any clade `C ⊆ L`, the clade hash is

    clade_hash(C) = SHA256( ∥_{ℓ ∈ sort(C)} class_hash(ℓ) )

where `∥` denotes concatenation and `sort` is lexicographic ordering of
the 32-byte hashes. The clade hash is invariant to the order of insertion
into `C` and to the internal node labels of the tree.

### Definition 8 — Phylogenetic signal

Let `C` be the variance-covariance matrix under Brownian motion,
`C_ij = σ² · d_T(ℓ_i, ℓ_j)`. Let `X` be a trait vector on `L`. Pagel's λ
is the MLE of the parameter in

    V_λ = λ C + (1 - λ) diag(C)

Blomberg's K is

    K = (MSE_observed / MSE_BM) / (MSE_observed / MSE_star)

where `MSE_observed = (1/(n-1)) (X - X̄)ᵀ C⁻¹ (X - X̄)`. `MSE_BM` and
`MSE_star` are computed via the sample-variance approximation
documented in `signal.py`, not the exact expected values under Brownian
motion and star phylogeny. The test is therefore a heuristic rather
than an exact likelihood-ratio test.

---

## 3. Theorems

### Theorem 1 — Four-point condition

A metric space `(L, d)` is isometrically embeddable into a weighted tree
if and only if, for every four distinct elements `a, b, c, e ∈ L`,

    d(a,b) + d(c,e) ≤ max( d(a,c) + d(b,e),  d(a,e) + d(b,c) )

**Proof.** (⇒) In a tree, the path between any two of the four points
traverses the same median subtree. Let the four arms from the median
have lengths `w_a, w_b, w_c, w_e`. Then

    d(a,b) + d(c,e) = w_a + w_b + w_c + w_e
    d(a,c) + d(b,e) = w_a + w_c + w_b + w_e
    d(a,e) + d(b,c) = w_a + w_e + w_b + w_c

All three sums are equal, so the inequality holds with equality.

(⇐) The construction is due to Buneman (1974). Define the split for each
partition of `L` and verify the compatibility conditions; the collection
of compatible splits is exactly the edge set of a tree, and the weights
are recovered as half-differences of the distances. ∎

### Theorem 2 — Neighbor-Joining correctness

Let `d_true` be a tree-additive metric on `L` with minimum internal edge
weight `w_min > 0`. Let `d` be any metric on `L` with
`|d(x,y) - d_true(x,y)| < ε` for all pairs. If `ε < w_min / 2`, the
Neighbor-Joining algorithm of Saitou and Nei (1987) recovers the topology
of the true tree.

**Proof.** The proof is due to Atteson (1999). The Q-criterion

    Q(i,j) = (n-2) d(i,j) - ∑_k d(i,k) - ∑_k d(j,k)

is within `4ε(n-2)` of its true value at every pair. Under the bound
`ε < w_min/2`, the pair that minimises Q is guaranteed to be a cherry
— a sibling pair in the true tree. Induct on the number of leaves. ∎

### Theorem 3 — Clade hash determinism

For any clade `C ⊆ L`, the clade hash depends only on the multiset of
class hashes `{class_hash(ℓ) : ℓ ∈ C}` and not on the order of insertion
into `C` nor on the internal node labels of the tree that produced `C`.

**Proof.** The clade hash is `SHA256(∥_{ℓ ∈ sort(C)} class_hash(ℓ))`. The
sort operation produces a unique ordering from the multiset,
independent of insertion order. The concatenation is therefore a
deterministic function of the multiset. SHA256 is a function, so the
clade hash is a deterministic function of the multiset. Internal node
labels do not appear in the definition. ∎

### Theorem 4 — Unidirectionality

There is no data path in the STIRPES implementation from the clade
structure, the tree, the clade hashes, or the settlement records back
into the JANUS orchestrator, the AGOP state, or the fingerprint
extractor.

**Proof.** The `StirpesRecorder` class has exactly four public methods:
`record(agop_result, module_contexts, snapshot, verdict) -> ClassHash`,
`flush() -> SettlementBatch`, `query_*` methods returning
`list[SettlementRecord]`, and `settle(batch) -> TxHash`. Only `record`
accepts the AGOP output and module contexts, and its return type is
`ClassHash`, which is a `bytes` value with no reference to the inputs.
The remaining methods do not accept the AGOP output and do not return
anything the orchestrator consumes. The module's `__init__.py` does not
import any JANUS module outside `janus.contracts` (which is a primitive
type module), and no JANUS module imports anything from `stirpes`
except `StirpesRecorder` and its return types. The import graph is
therefore acyclic with STIRPES as a sink. ∎

---

## 4. Complexity

| Operation | Time | Space |
|---|---|---|
| Fingerprint extraction | O(\|V\| + \|modules\|) | O(\|V\| + \|modules\|) |
| Canonical form | O(\|f\| log \|f\|) | O(\|f\|) |
| Class hash | O(\|f\|) | O(\|f\|) |
| Distance matrix | O(n² · T_persist + n² · T_WL + n² · T_W2) | O(n²) |
| Neighbor-Joining | O(n³) | O(n²) |
| UPGMA | O(n³) | O(n²) |
| Fitch parsimony | O(n · L · C) | O(n · L · C) |
| Pagel's λ | O(n³) | O(n²) |
| Blomberg's K | O(n³) | O(n²) |

Here `n = |L|`, `L` is the number of characters for parsimony, `C` is
the number of states per character, `T_persist` is the persistence
computation cost, `T_WL` is the Weisfeiler–Lehman kernel cost, and `T_W2`
is the Wasserstein-2 cost.

---

## 5. Architecture

### 5.1 The recorder

The `StirpesRecorder` accumulates ticks. For each tick it computes the
fingerprint, the canonical form, and the class hash, and appends a
`PendingTick` to an in-memory queue. It maintains a persistent leaf set
(`_leaf_fingerprints` and `_leaf_class_hashes`) across flushes, so the
phylogenetic tree is built over the full leaf set rather than the
current batch alone. On `flush()`, it:

1. Adds the pending ticks to the persistent leaf set (deduping by class
   hash, evicting oldest leaves if the set exceeds `MAX_LEAF_SET_SIZE`).
2. Computes the pairwise distance matrix over the full leaf set.
3. Builds the phylogenetic tree (Neighbor-Joining by default, UPGMA as
   an alternative). Handles the singleton case where only one leaf
   exists.
4. Computes the clade hash for each leaf's parent clade.
5. Emits a `SettlementBatch` containing the pending ticks' class hashes,
   clade hashes, and call identifiers.

The full leaf set is capped at `MAX_LEAF_SET_SIZE = 2000` leaves, with
FIFO eviction. This bounds memory and prevents the tree build from
becoming O(n³) at unbounded scale.

### 5.2 The chain

The `AbstractChainClient` defines `commit(batch) -> TxHash` and
`query(filter) -> list[SettlementRecord]`. The `MockChainClient`
provides an in-memory implementation for testing. The `TezosChainClient`
stub connects to an Etherlink or private Tezos rollup RPC endpoint; the
details are in `TEZOS_CHAIN.md`.

The on-chain record per tick is

    TickRecord(
        H_t,                    // bytes32
        class_hash,             // bytes32
        historical_clade_hash,  // bytes32
        session_id,             // bytes32
        tick_index,             // uint256
        blocktime,              // uint256
        H_payload               // bytes32
    )

The `H_t` is `SHA256(class_hash ‖ session_id ‖ tick_index ‖ snapshot_hash)`.
The `H_payload` is `SHA256(ciphertext)` where `ciphertext` is the
encrypted fingerprint plus the module contexts, ready for reveal.

### 5.3 The reveal

The `PayloadCipher` encrypts and decrypts the payload with a symmetric
key. The `RevealGate` checks payment (a token balance or a signed
payment transaction) before releasing the key. The default cipher is a
placeholder XOR cipher for testing; production deployments substitute
AES-GCM or ChaCha20-Poly1305.

### 5.4 The query engine

The `QueryEngine` provides three query patterns over the settlement
layer:

- `by_tick(H_t)` — single-record lookup.
- `by_clade(clade_hash, time_range=None)` — range query.
- `by_session(session_id)` — range query.

Each returns a list of `SettlementRecord`, which the caller resolves
against the off-chain log or against the data-availability layer.

---

## 6. Installation

STIRPES is part of JANUS. No additional packages are required beyond
JANUS's existing `numpy`, `scipy`, `httpx`, and `pydantic`.

To use the on-chain settlement layer, the `web3` package is required:

```bash
pip install web3
```

The Solidity contract `StirpesRegistry.sol` must be compiled and
deployed to the chosen L2 before the `TezosChainClient` can be used. The
`MockChainClient` requires no deployment.

To run the test suite:

```bash
pip install pytest
pytest tests/test_stirpes.py -v
```

---

## 7. Complete usage tutorial

This section shows a fully working integration, with every step shown in
full. Nothing is abbreviated, no `# ... continue as before` shortcuts.

### 7.1 Step 1 — Construct the orchestrator and the recorder

```python
from janus.config import Config
from janus.orchestrator import Orchestrator
from janus.stirpes import StirpesRecorder, MockChainClient, XorCipher

configuration = Config()
orchestrator = Orchestrator(configuration)

chain = MockChainClient(blocktime_seconds=1)
cipher = XorCipher(seed=b"my-stirpes-seed")
recorder = StirpesRecorder(
    chain=chain,
    cipher=cipher,
    tree_method="neighbor_joining",
    flush_threshold=100,
)
```

### 7.2 Step 2 — Record a tick

For each tick, call `orchestrator.tick(snapshot)` and then
`recorder.record(...)` with the values the orchestrator exposes:

```python
from janus.contracts import MarketSnapshot

snapshot = MarketSnapshot(
    symbol="BTC/USDT",
    price=50000.0,
    expected_return=0.004,
    realized_volatility=0.012,
    slippage=2.0,
    slippage_maximum=20.0,
    venue_risk=0.2,
    signal_agreement=0.6,
    order_flow_imbalance=0.05,
    history=tuple(50000.0 + i for i in range(64)),
    timestamps=tuple(float(i) for i in range(64)),
    external_data={"sentiment": 0.2},
)

tick_record = orchestrator.tick(snapshot)

class_hash = recorder.record(
    agop_result=orchestrator.last_agop_result,
    module_contexts=orchestrator.last_module_contexts,
    snapshot=snapshot,
    verdict=tick_record["intent"].get("verdict", "pass"),
)

print(f"Class hash of this tick: {class_hash.hex()}")
```

The `record` method returns the 32-byte class hash of the tick's
fingerprint. You can log it alongside the tick for your own records.

The recorder's `flush_threshold` parameter controls when an automatic
flush occurs. With the default of 100, the recorder flushes itself once
100 ticks have accumulated.

### 7.3 Step 3 — Flush and settle

When you want to settle, call `flush()` explicitly (or wait for the
threshold to trigger it):

```python
batch = recorder.flush()
if batch is None:
    print("No pending ticks; nothing to settle.")
else:
    print(f"Flushing {len(batch.tick_hashes)} ticks")
    print(f"  Leaf set hash: {batch.leaf_set_hash.hex()}")
    print(f"  Tree root hash: {batch.tree_root_hash.hex()}")
    print(f"  Distinct clades: {len(set(batch.clade_hashes))}")

    tx_hash = recorder.settle(batch)
    print(f"Settled in transaction {tx_hash.hex()}")
```

`flush()` returns `None` if there are no pending ticks. Otherwise, it
returns a `SettlementBatch` containing:

- `tick_hashes` — the composed identifiers per tick.
- `class_hashes` — the class hash per tick.
- `clade_hashes` — the clade hash per tick.
- `session_ids` — the session identifier per tick.
- `tick_indices` — the tick index within the session per tick.
- `payload_hashes` — the encrypted payload hash per tick.
- `leaf_set_hash` — the hash of the leaf set.
- `tree_root_hash` — the hash of the tree topology.

The batch is immutable. If you want to inspect it before settling, do so
before calling `settle()`.

### 7.4 Step 4 — Query by tick

```python
from janus.stirpes import QueryEngine, TickHash

engine = QueryEngine(chain=chain)

first_tick_hash = batch.tick_hashes[0]
record = engine.by_tick(first_tick_hash)
if record is None:
    print("Tick not found.")
else:
    print(f"Tick hash:    {record.tick_hash.hex()}")
    print(f"Class hash:   {record.class_hash.hex()}")
    print(f"Clade hash:   {record.historical_clade_hash.hex()}")
    print(f"Session:      {record.session_id}")
    print(f"Tick index:   {record.tick_index}")
    print(f"Blocktime:    {record.blocktime}")
    print(f"Payload hash: {record.payload_hash.hex()}")
```

### 7.5 Step 5 — Query by clade

```python
from janus.stirpes import CladeHash

first_clade_hash = batch.clade_hashes[0]
clade_records = engine.by_clade(first_clade_hash)
print(f"Ticks in clade {first_clade_hash.hex()}: {len(clade_records)}")
for r in clade_records:
    print(f"  Tick {r.tick_hash.hex()} at blocktime {r.blocktime}")

# With a time restriction:
recent = engine.by_clade(
    first_clade_hash,
    time_range=(0, 1_000_000_000),
)
print(f"Recent ticks in clade: {len(recent)}")
```

### 7.6 Step 6 — Query by session

```python
from janus.stirpes import SessionId

session_records = engine.by_session(SessionId("default-session"))
print(f"Ticks in session: {len(session_records)}")
for r in session_records:
    print(f"  {r.tick_hash.hex()} at tick index {r.tick_index}")
```

### 7.7 Step 7 — Run the phylogenetic signal tests

After flushing, you can run the signal tests on the tree to see whether
the clade structure is informative:

```python
from janus.stirpes import pagels_lambda, blombergs_k
from janus.stirpes.distance import distance_matrix
from janus.stirpes.tree import build_tree

# Rebuild the tree from the recorder's full leaf set. Note: flush() clears
# the pending list, so this example reads from _leaf_fingerprints after a
# flush. In practice you would also store the outcomes (P&L) per class
# hash at record time.
labels = sorted(recorder._leaf_fingerprints.keys())
fingerprints = [recorder._leaf_fingerprints[lbl] for lbl in labels]
D = distance_matrix(fingerprints)
tree = build_tree(labels, D, method="neighbor_joining", root=True)

# Trait: for each leaf, some observed outcome (e.g. realized P&L).
trait = {
    labels[i]: pnl_per_class_hash[i]
    for i in range(len(labels))
}

lam = pagels_lambda(tree, trait)
k = blombergs_k(tree, trait)

print(f"Pagel's lambda = {lam:.4f}")
print(f"Blomberg's K   = {k:.4f}")

if lam > 0.7 and k > 0.7:
    print("Strong phylogenetic signal: clades are informative.")
elif lam > 0.3 and k > 0.3:
    print("Moderate signal: use with caution.")
else:
    print("Weak signal: the clade structure is likely spurious.")
```

### 7.8 Step 8 — Encrypt and reveal a payload

The default cipher is the placeholder `XorCipher`. For production, use a
real AEAD:

```python
from janus.stirpes import PayloadCipher

class AesGcmCipher(PayloadCipher):
    def __init__(self, key: bytes):
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        self._aesgcm = AESGCM(key)

    def encrypt(self, plaintext: bytes) -> bytes:
        import os
        nonce = os.urandom(12)
        return nonce + self._aesgcm.encrypt(nonce, plaintext, None)

    def decrypt(self, ciphertext: bytes) -> bytes:
        return self._aesgcm.decrypt(ciphertext[:12], ciphertext[12:], None)

recorder = StirpesRecorder(
    chain=chain,
    cipher=AesGcmCipher(key=b"\x00" * 32),
)
```

Reveal is gated by `RevealGate`:

```python
from janus.stirpes import RevealGate, TokenLedger

class MyTokenLedger(TokenLedger):
    def __init__(self, balances, transfers):
        self._balances = balances
        self._transfers = transfers

    def balance_of(self, address: str) -> int:
        return self._balances.get(address, 0)

    def transferred_to(self, from_address: str, to_address: str) -> int:
        return self._transfers.get((from_address, to_address), 0)

ledger = MyTokenLedger(
    balances={"0xbuyer": 150},
    transfers={},
)
gate = RevealGate(
    token_ledger=ledger,
    min_balance=100,
    min_transfer=0,
)

plaintext = gate.check_and_reveal(
    caller_address="0xbuyer",
    payload_hash=record.payload_hash,
    ciphertext=ciphertext,
    cipher=recorder.cipher,
)
if plaintext is None:
    print("Payment insufficient; no reveal.")
else:
    print(f"Revealed: {plaintext.hex()}")
```

---

## 8. Complete API reference

### 8.1 Package `janus.stirpes`

The top-level import surface:

```python
from janus.stirpes import (
    Fingerprint, ClassHash, CladeHash, TickHash, PayloadHash, SessionId,
    PendingTick, TickRecord, SettlementBatch, SettlementRecord,
    extract_fingerprint, canonical_form, class_hash, payload_hash, snapshot_hash,
    distance, distance_components, distance_matrix,
    build_tree, PhylogeneticTree, TreeNode,
    clade_hash_from_labels, clade_hash_for_leaf, all_clades,
    pagels_lambda, blombergs_k,
    StirpesRecorder, MockChainClient, TezosChainClient, AbstractChainClient,
    PayloadCipher, XorCipher, RevealGate, TokenLedger,
    QueryEngine,
)
```

### 8.2 `janus.stirpes.contracts`

**`ClassHash = NewType("ClassHash", bytes)`** — 32-byte SHA-256 hash of a
fingerprint's canonical form.

**`CladeHash = NewType("CladeHash", bytes)`** — 32-byte hash of a
clade's leaf set.

**`TickHash = NewType("TickHash", bytes)`** — 32-byte composed identifier
per tick.

**`PayloadHash = NewType("PayloadHash", bytes)`** — 32-byte hash of the
encrypted payload.

**`SessionId = NewType("SessionId", str)`** — session identifier.

**`Fingerprint`** — frozen dataclass with fields:

| Field | Type | Description |
|---|---|---|
| `ranking` | `tuple[str, ...]` | Ordered list of actions in AGOP ranking |
| `survivor_set` | `tuple[str, ...]` | Sorted survivor set `D*` |
| `topology` | `tuple[tuple[str, str], ...]` | Sorted (action, class) pairs |
| `convergence_depth` | `int` | AGOP convergence depth |
| `capacity` | `Optional[int]` | Derived capacity `K`, or `None` |
| `lower_confidence_bound` | `tuple[tuple[str, float], ...]` | Sorted (action, LCB) pairs |
| `composite_score` | `tuple[tuple[str, float], ...]` | Sorted (action, Phi) pairs |
| `nash_dm` | `tuple[float, float]` | Nash strategy for decision-maker |
| `nash_cp` | `tuple[float, float]` | Nash strategy for counter-party |
| `nash_entropy` | `tuple[float, float]` | Shannon entropy of each Nash strategy |
| `modules` | `tuple[tuple[str, str, float, str], ...]` | (name, phase, multiplier, context_hash) |
| `verdict` | `str` | Verifier code |

**`PendingTick`** — frozen dataclass with fields: `fingerprint`,
`class_hash`, `session_id`, `tick_index`, `snapshot_hash`,
`payload_hash`.

**`TickRecord`** — frozen dataclass with fields: `tick_hash`,
`class_hash`, `historical_clade_hash`, `session_id`, `tick_index`,
`blocktime`, `payload_hash`.

**`SettlementBatch`** — frozen dataclass with fields: `tick_hashes`,
`class_hashes`, `clade_hashes`, `session_ids`, `tick_indices`,
`payload_hashes`, `leaf_set_hash`, `tree_root_hash`.

**`SettlementRecord`** — frozen dataclass with the same fields as
`TickRecord`.

**Verdict constants:** `VERDICT_PASS`, `VERDICT_SIZE_CLAMPED`,
`VERDICT_CONTRACT_COLLAPSE`, `VERDICT_TOXICITY_COLLAPSE`,
`VERDICT_CONFIDENCE_FLOOR_COLLAPSE`, and `ALL_VERDICTS`.

### 8.3 `janus.stirpes.fingerprint`

**`extract_fingerprint(agop_result, module_contexts, verdict="pass") -> Fingerprint`** — extract the fingerprint from a completed JANUS tick.
Takes the normalised `AgopResult` and the flattened module contexts
(from `Orchestrator.last_module_contexts`).

**`canonical_form(fingerprint) -> bytes`** — the unique canonical byte
string of a fingerprint.

**`class_hash(fingerprint) -> ClassHash`** — SHA-256 of the canonical
form.

**`payload_hash(ciphertext) -> PayloadHash`** — SHA-256 of the encrypted
payload.

**`snapshot_hash(snapshot) -> bytes`** — deterministic hash of a market
snapshot.

**`ROUND_DIGITS`** — module constant, default 6.

### 8.4 `janus.stirpes.distance`

**`distance_components(f, g) -> tuple[float, float, float]`** — the
three distance components separately.

**`distance_matrix(fingerprints, weights=None) -> np.ndarray`** —
pairwise distance matrix. If `weights` is `None`, computes inverse-variance
weights from the sample.

**`distance(f, g, weights=(1/3, 1/3, 1/3)) -> float`** — single-pair
distance.

### 8.5 `janus.stirpes.tree`

**`TreeNode`** — dataclass with fields `label`, `children`, `parent`,
`length`, and method `is_leaf()`.

**`PhylogeneticTree`** — dataclass with fields `root`, `leaves`, and
methods `clade(label)`, `lca(a, b)`, `path_distance(a, b)`,
`internal_nodes()`.

**`build_tree(labels, distances, method="neighbor_joining", root=True) -> PhylogeneticTree`** — build a tree from a distance matrix.

### 8.6 `janus.stirpes.clade`

**`clade_hash_from_labels(labels, class_hashes) -> CladeHash`** — compute
the clade hash of a leaf set.

**`clade_hash_for_leaf(tree, leaf_label, class_hashes) -> CladeHash`** —
compute the clade hash of a leaf's parent clade.

**`all_clades(tree, class_hashes) -> dict[CladeHash, frozenset[str]]`** —
map from clade hash to leaf set, for every internal node with at least
two leaves.

### 8.7 `janus.stirpes.signal`

**`pagels_lambda(tree, trait, leaves=None) -> float`** — MLE of Pagel's λ.

**`blombergs_k(tree, trait, leaves=None) -> float`** — Blomberg's K.

### 8.8 `janus.stirpes.recorder`

**`StirpesRecorder`** — dataclass with fields `chain`, `cipher`,
`tree_method`, `flush_threshold`, `session_id`, `pending`,
`historical_ticks`, `current_clade_hashes`, `_leaf_fingerprints`,
`_leaf_class_hashes`. Methods:

- `record(agop_result, module_contexts, snapshot, verdict="pass") -> ClassHash`
- `flush() -> SettlementBatch | None`
- `settle(batch) -> bytes`
- `query_by_tick(tick_hash) -> SettlementRecord | None`
- `query_by_clade(clade_hash) -> list[SettlementRecord]`
- `query_by_session(session_id) -> list[SettlementRecord]`

### 8.9 `janus.stirpes.chain`

**`AbstractChainClient`** — abstract base with `commit`, `query`, and
`latest_blocktime`.

**`MockChainClient`** — in-memory implementation. Constructor:
`MockChainClient(blocktime_seconds: int = 1)`.

**`TezosChainClient`** — stub for real L2. Constructor:
`TezosChainClient(rpc_url, contract_address, private_key)`. Requires
`pip install web3`. `commit` and `query` raise `NotImplementedError`;
`latest_blocktime` works.

### 8.10 `janus.stirpes.reveal`

**`PayloadCipher`** — abstract base with `encrypt` and `decrypt`.

**`XorCipher`** — placeholder. Constructor:
`XorCipher(seed: bytes = b"stirpes-test-seed")`.

**`RevealGate`** — constructor:
`RevealGate(token_ledger, min_balance=0, min_transfer=0, operator_address="0x0")`.
Method: `check_and_reveal(caller_address, payload_hash, ciphertext, cipher) -> bytes | None`.

**`TokenLedger`** — abstract base with `balance_of` and `transferred_to`.

### 8.11 `janus.stirpes.query`

**`QueryEngine`** — constructor: `QueryEngine(chain)`. Methods:
`by_tick`, `by_clade`, `by_session`.

### 8.12 `janus.stirpes.api`

FastAPI router mounted at `/api/stirpes`:

| Method | Path | Description |
|---|---|---|
| POST | `/api/stirpes/flush` | Flush pending ticks and settle. |
| GET | `/api/stirpes/clade/{clade_hash_hex}` | Return tick hashes in a clade. |
| GET | `/api/stirpes/tick/{tick_hash_hex}` | Return settlement record for a tick. |
| GET | `/api/stirpes/session/{session_id}` | Return settlement records for a session. |
| POST | `/api/stirpes/reveal` | Reveal a payload against payment. |

---

## 9. Limitations

**Tree stability.** The recorder maintains a persistent leaf set across
flushes, so the tree topology is more stable than a per-batch rebuild
would be. However, as new leaves are added, the topology can still shift
when a new leaf reveals a split that was not visible before. The
`historical_clade_hash` on chain records the clade at the time of
commit; the current clade may differ. Both are queryable, but the
distinction must be kept clear.

**Leaf set bound.** The persistent leaf set is capped at
`MAX_LEAF_SET_SIZE = 2000` with FIFO eviction. Beyond this bound, the
oldest leaves are dropped from the tree, which means very old ticks may
no longer participate in the current tree. Their on-chain
`historical_clade_hash` remains valid for the tree state at commit time.

**Four-point failure.** If the distance matrix fails the four-point
condition, the tree is a split network rather than a tree. STIRPES
detects the failure and reports the offending quartets, but does not
implement the full split-network reconstruction.

**Approximate distances.** The interleaving distance is a
bottleneck-style proxy, not the exact sublevel-set interleaving. The
Blomberg's K approximation uses sample variance, not the exact BM/star
expected MSE. Both are documented at their source.

**Signal test interpretation.** Pagel's λ and Blomberg's K are
heuristic indicators, not exact likelihood-ratio tests. If either is
significantly different from zero, the tree is informative in the
statistical sense. If either is close to zero, the tree may still be
informative for downstream queries, but the module reports the weakness
so the caller can decide.

**Encryption.** The default `PayloadCipher` is a placeholder XOR cipher.
It is not secure against a determined adversary. Production deployments
must substitute a proper AEAD cipher.

**Chain stub.** The `TezosChainClient` is a stub. It requires `web3` and
a deployed `StirpesRegistry.sol` contract to function. The
`MockChainClient` is complete and is what the test suite exercises.

---

## 10. License

MIT.