# STIRPES API Reference

Complete API documentation for the STIRPES module. Every public type,
function, class, and method is documented in full.

---

## Module `janus.stirpes`

The package's `__init__.py` re-exports the public surface. Import
everything from the top-level package:

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

---

## Module `janus.stirpes.contracts`

### `ClassHash`

A `NewType` alias for `bytes`. 32-byte SHA-256 hash of a fingerprint's
canonical form.

```python
ClassHash = NewType("ClassHash", bytes)
```

### `CladeHash`

A `NewType` alias for `bytes`. 32-byte hash of a clade's leaf set.

```python
CladeHash = NewType("CladeHash", bytes)
```

### `TickHash`

A `NewType` alias for `bytes`. 32-byte composed identifier per tick.

```python
TickHash = NewType("TickHash", bytes)
```

### `PayloadHash`

A `NewType` alias for `bytes`. 32-byte hash of the encrypted payload.

```python
PayloadHash = NewType("PayloadHash", bytes)
```

### `SessionId`

A `NewType` alias for `str`. Session identifier.

```python
SessionId = NewType("SessionId", str)
```

### `Fingerprint`

A frozen dataclass with the following fields:

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

**Invariants:**

- `topology`, `lower_confidence_bound`, `composite_score` must be sorted.
- `verdict` must be one of `ALL_VERDICTS`.

### `PendingTick`

Frozen dataclass. A tick awaiting settlement.

| Field | Type |
|---|---|
| `fingerprint` | `Fingerprint` |
| `class_hash` | `ClassHash` |
| `session_id` | `SessionId` |
| `tick_index` | `int` |
| `snapshot_hash` | `bytes` |
| `payload_hash` | `PayloadHash` |

### `TickRecord`

Frozen dataclass. The on-chain record for a settled tick.

| Field | Type |
|---|---|
| `tick_hash` | `TickHash` |
| `class_hash` | `ClassHash` |
| `historical_clade_hash` | `CladeHash` |
| `session_id` | `SessionId` |
| `tick_index` | `int` |
| `blocktime` | `int` |
| `payload_hash` | `PayloadHash` |

### `SettlementBatch`

Frozen dataclass. A batch of ticks flushed together.

| Field | Type |
|---|---|
| `tick_hashes` | `tuple[TickHash, ...]` |
| `class_hashes` | `tuple[ClassHash, ...]` |
| `clade_hashes` | `tuple[CladeHash, ...]` |
| `session_ids` | `tuple[SessionId, ...]` |
| `tick_indices` | `tuple[int, ...]` |
| `payload_hashes` | `tuple[PayloadHash, ...]` |
| `leaf_set_hash` | `bytes` |
| `tree_root_hash` | `bytes` |

**Invariant:** all columns must have equal length.

### `SettlementRecord`

Frozen dataclass. The record returned by query. Identical fields to
`TickRecord`.

### Verdict constants

```python
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
```

---

## Module `janus.stirpes.fingerprint`

### `extract_fingerprint(agop_result, module_contexts, verdict="pass") -> Fingerprint`

Extract the fingerprint from a completed JANUS tick.

**Parameters:**

- `agop_result` (`AgopResult`) — the normalised bridge output, which now
  includes `nash_dm` and `nash_cp`.
- `module_contexts` (`dict[str, dict[str, Any]]`) — module contexts by
  name, from `Orchestrator.last_module_contexts`.
- `verdict` (`str`) — the verifier's code, default `"pass"`.

**Returns:** a `Fingerprint` with all fields populated and pre-rounded to
six decimals.

**Raises:** `ValueError` if any sorted field is unsorted (which cannot
happen through this function).

### `canonical_form(fingerprint) -> bytes`

Return the unique canonical byte string of a fingerprint.

**Parameters:** `fingerprint` (`Fingerprint`)

**Returns:** `bytes` — UTF-8 encoded compact JSON with sorted keys.

### `class_hash(fingerprint) -> ClassHash`

Return the SHA-256 hash of the canonical form.

**Parameters:** `fingerprint` (`Fingerprint`)

**Returns:** `ClassHash` (32 bytes)

### `payload_hash(ciphertext) -> PayloadHash`

Return the SHA-256 hash of the encrypted payload.

**Parameters:** `ciphertext` (`bytes`)

**Returns:** `PayloadHash` (32 bytes)

### `snapshot_hash(snapshot) -> bytes`

Return the deterministic hash of a market snapshot.

**Parameters:** `snapshot` (any object with `symbol`, `price`,
`expected_return`, `realized_volatility`, `slippage`, `slippage_maximum`,
`venue_risk`, `signal_agreement`, `order_flow_imbalance`, `history`,
`timestamps`).

**Returns:** `bytes` (32 bytes).

### `ROUND_DIGITS`

Module constant. The rounding precision for continuous components.
Default `6`.

---

## Module `janus.stirpes.distance`

### `distance_components(f, g) -> tuple[float, float, float]`

Compute the three distance components separately.

**Parameters:**

- `f` (`Fingerprint`)
- `g` (`Fingerprint`)

**Returns:** `(interleaving, WL, Wasserstein2)` tuple.

### `distance_matrix(fingerprints, weights=None) -> np.ndarray`

Compute the pairwise distance matrix.

**Parameters:**

- `fingerprints` (`Iterable[Fingerprint]`)
- `weights` (`tuple[float, float, float] | None`) — if `None`, computes
  inverse-variance weights from the sample; otherwise uses the given
  weights directly.

**Returns:** `numpy.ndarray` of shape `(n, n)`, symmetric with zero
diagonal.

**Complexity:** `O(n² · (T_persist + T_WL + T_W2))`.

### `distance(f, g, weights=(1/3, 1/3, 1/3)) -> float`

Compute a single-pair distance.

**Parameters:**

- `f` (`Fingerprint`)
- `g` (`Fingerprint`)
- `weights` (`tuple[float, float, float]`) — component weights.

**Returns:** `float`.

---

## Module `janus.stirpes.tree`

### `TreeNode`

Dataclass. A node in a phylogenetic tree.

| Field | Type | Default |
|---|---|---|
| `label` | `str` | required |
| `children` | `list[TreeNode]` | `[]` |
| `parent` | `TreeNode \| None` | `None` |
| `length` | `float` | `0.0` |

**Method:** `is_leaf() -> bool`.

### `PhylogeneticTree`

Dataclass. A weighted rooted tree.

| Field | Type |
|---|---|
| `root` | `TreeNode` |
| `leaves` | `dict[str, TreeNode]` |

**Methods:**

- `clade(label) -> frozenset[str]` — the leaves under the given node.
- `lca(a, b) -> TreeNode` — the lowest common ancestor of two leaves.
- `path_distance(a, b) -> float` — total edge weight between two leaves.
- `internal_nodes() -> list[TreeNode]` — all non-leaf nodes.

**Raises:**

- `KeyError` in `clade` if `label` not found.
- `RuntimeError` in `lca` if the tree is disconnected.

### `build_tree(labels, distances, method="neighbor_joining", root=True) -> PhylogeneticTree`

Build a phylogenetic tree from a distance matrix.

**Parameters:**

- `labels` (`list[str]`) — leaf labels.
- `distances` (`np.ndarray`) — square symmetric distance matrix.
- `method` (`str`) — `"neighbor_joining"` (default) or `"upgma"`.
- `root` (`bool`) — whether to apply midpoint rooting, default `True`.

**Returns:** `PhylogeneticTree`.

**Raises:** `ValueError` if the distance matrix shape does not match the
label count, or if `method` is unknown.

**Complexity:**

- Neighbor-Joining: `O(n³)`.
- UPGMA: `O(n³)`.

---

## Module `janus.stirpes.clade`

### `clade_hash_from_labels(labels, class_hashes) -> CladeHash`

Compute the clade hash of a leaf set.

**Parameters:**

- `labels` (`frozenset[str] | set[str] | list[str]`) — leaf labels.
- `class_hashes` (`dict[str, bytes]`) — map from label to class hash.

**Returns:** `CladeHash` (32 bytes).

### `clade_hash_for_leaf(tree, leaf_label, class_hashes) -> CladeHash`

Compute the clade hash of a leaf's parent clade.

**Parameters:**

- `tree` (`PhylogeneticTree`)
- `leaf_label` (`str`)
- `class_hashes` (`dict[str, bytes]`)

**Returns:** `CladeHash`.

**Raises:** `KeyError` if the leaf is not in the tree; `RuntimeError` if
the leaf has no parent.

### `all_clades(tree, class_hashes) -> dict[CladeHash, frozenset[str]]`

Compute all internal-node clades as a map.

**Parameters:**

- `tree` (`PhylogeneticTree`)
- `class_hashes` (`dict[str, bytes]`)

**Returns:** `dict[CladeHash, frozenset[str]]` — map from clade hash to
leaf set, for every internal node with at least two leaves.

---

## Module `janus.stirpes.signal`

### `pagels_lambda(tree, trait, leaves=None) -> float`

Compute the maximum-likelihood estimate of Pagel's λ.

**Parameters:**

- `tree` (`PhylogeneticTree`)
- `trait` (`dict[str, float]`) — map from leaf label to trait value.
- `leaves` (`list[str] | None`) — the leaf order; if `None`, uses
  `sorted(tree.leaves)`.

**Returns:** `float` in `[0, 1]`.

**Raises:** `ValueError` if there are fewer than 3 leaves.

**Complexity:** `O(n³)` per likelihood evaluation.

### `blombergs_k(tree, trait, leaves=None) -> float`

Compute Blomberg's K.

**Parameters:** same as `pagels_lambda`.

**Returns:** `float` — `K = 1` indicates expected phylogenetic signal;
`K > 1` indicates conservatism; `K < 1` indicates convergence or noise.

**Raises:** `ValueError` if there are fewer than 3 leaves.

**Complexity:** `O(n³)`.

**Note:** The `MSE_BM` and `MSE_star` computations use sample-variance
approximations rather than the exact BM/star expected values. The result
is a heuristic indicator, not an exact likelihood-ratio test.

---

## Module `janus.stirpes.recorder`

### `StirpesRecorder`

Dataclass. The batch recorder.

**Constructor fields:**

| Field | Type | Default |
|---|---|---|
| `chain` | `AbstractChainClient` | required |
| `cipher` | `PayloadCipher` | required |
| `tree_method` | `str` | `"neighbor_joining"` |
| `flush_threshold` | `int` | `100` |
| `session_id` | `SessionId` | `SessionId("default-session")` |
| `pending` | `list[PendingTick]` | `[]` |
| `historical_ticks` | `list[SettlementRecord]` | `[]` |
| `current_clade_hashes` | `dict[ClassHash, CladeHash]` | `{}` |
| `_leaf_fingerprints` | `dict[str, Fingerprint]` | `{}` |
| `_leaf_class_hashes` | `dict[str, ClassHash]` | `{}` |

**Methods:**

#### `record(agop_result, module_contexts, snapshot, verdict="pass") -> ClassHash`

Record one tick. Returns the class hash of the fingerprint. This is the
only method that receives the AGOP output and module contexts; the
return value is a plain hash with no reference to the inputs.

#### `flush() -> SettlementBatch | None`

Rebuild the tree over the full leaf set (historical + pending) and emit
a settlement batch. Returns `None` if there are no pending ticks.
Handles the singleton case (only one unique leaf) without a tree build.

#### `settle(batch) -> bytes`

Commit a batch to the chain. Returns the transaction hash. Appends
`SettlementRecord` entries to `historical_ticks`.

#### `query_by_tick(tick_hash) -> SettlementRecord | None`

Single-record lookup.

#### `query_by_clade(clade_hash) -> list[SettlementRecord]`

Range query by clade hash.

#### `query_by_session(session_id) -> list[SettlementRecord]`

Range query by session.

**Note on persistent leaf set:** The recorder maintains
`_leaf_fingerprints` and `_leaf_class_hashes` across flushes. They are
capped at `MAX_LEAF_SET_SIZE = 2000` with FIFO eviction. Access them
directly for signal tests; they are documented as accessible state
despite the leading underscore convention.

---

## Module `janus.stirpes.chain`

### `AbstractChainClient`

Abstract base class. Subclasses must implement:

- `commit(batch: SettlementBatch) -> bytes`
- `query(class_hash=None, clade_hash=None, session_id=None, time_range=None) -> list[SettlementRecord]`
- `latest_blocktime() -> int`

### `MockChainClient`

In-memory implementation. Constructor:

```python
MockChainClient(blocktime_seconds: int = 1)
```

Maintains an in-memory list of `SettlementRecord` and a monotone block
counter. Every `commit` produces a deterministic `tx_hash`. Every
`query` filters the list.

### `TezosChainClient`

Stub for real L2 interaction. Constructor:

```python
TezosChainClient(rpc_url: str, contract_address: str, private_key: str)
```

**Requires:** `pip install web3`.

**Behavior:** `commit` and `query` raise `NotImplementedError` because
the deployment-specific contract ABI is not part of STIRPES.
`latest_blocktime` works via `web3.eth.get_block("latest")`.

---

## Module `janus.stirpes.reveal`

### `PayloadCipher`

Abstract base class. Subclasses must implement:

- `encrypt(plaintext: bytes) -> bytes`
- `decrypt(ciphertext: bytes) -> bytes`

### `XorCipher`

Placeholder XOR cipher. **Not secure.** For testing only. Constructor:

```python
XorCipher(seed: bytes = b"stirpes-test-seed")
```

### `RevealGate`

Token-gated reveal.

**Constructor:**

```python
RevealGate(
    token_ledger: TokenLedger,
    min_balance: int = 0,
    min_transfer: int = 0,
    operator_address: str = "0x0",
)
```

**Method:** `check_and_reveal(caller_address, payload_hash, ciphertext, cipher) -> bytes | None`.

Returns the decrypted plaintext if payment is sufficient; `None` if
insufficient. Verifies the ciphertext hash against `payload_hash` and
raises `ValueError` if they don't match.

### `TokenLedger`

Abstract base class. Subclasses must implement:

- `balance_of(address: str) -> int`
- `transferred_to(from_address: str, to_address: str) -> int`

---

## Module `janus.stirpes.query`

### `QueryEngine`

Wraps a chain client with the three canonical query patterns.

**Constructor:** `QueryEngine(chain: AbstractChainClient)`.

**Methods:**

- `by_tick(tick_hash) -> SettlementRecord | None`
- `by_clade(clade_hash, time_range=None) -> list[SettlementRecord]`
- `by_session(session_id, time_range=None) -> list[SettlementRecord]`

---

## Module `janus.stirpes.api`

FastAPI router mounted at `/api/stirpes`.

### `POST /api/stirpes/flush`

Flush pending ticks and settle. Returns:

```json
{
  "flushed": true,
  "tx_hash": "...",
  "tick_count": 3,
  "clade_count": 2
}
```

### `GET /api/stirpes/clade/{clade_hash_hex}`

Return the tick hashes in a clade. Response:

```json
{
  "clade_hash": "...",
  "tick_hashes": ["...", "..."]
}
```

### `GET /api/stirpes/tick/{tick_hash_hex}`

Return the settlement record for a tick. 404 if not found. Response:

```json
{
  "tick_hash": "...",
  "class_hash": "...",
  "clade_hash": "...",
  "session_id": "...",
  "tick_index": 42,
  "blocktime": 1700000000,
  "payload_hash": "..."
}
```

### `GET /api/stirpes/session/{session_id}`

Return the settlement records for a session. Response: a list of the
above shape.

### `POST /api/stirpes/reveal`

Reveal a payload against payment. Request:

```json
{
  "caller_address": "0xbuyer",
  "tick_hash": "...",
  "ciphertext_hex": "..."
}
```

Response:

```json
{
  "plaintext_hex": "..."
}
```

**Errors:**

- `404` if the tick is not found.
- `402` if payment is insufficient.

---

## `janus.contracts.AgopResult`

The bridge output, now extended with the Nash strategies.

| Field | Type | Description |
|---|---|---|
| `mode` | `AgopMode` | `"legacy"` or `"dbc"` |
| `ranking` | `list[str]` | Ordered list of actions |
| `survivor_set` | `list[str]` | Sorted survivor set |
| `lower_confidence_bound` | `dict[str, float]` | Map from action to LCB |
| `composite_score` | `dict[str, float]` | Map from action to Phi |
| `topology_class` | `dict[str, str]` | Map from action to WL class |
| `convergence_depth` | `int` | Fixed-point depth |
| `capacity` | `Optional[int]` | Derived or supplied capacity |
| `number_of_weisfeiler_lehman_classes` | `Optional[int]` | WL class count |
| `contract_verified` | `bool` | True if Theorem 5 held |
| `nash_dm` | `tuple[float, float]` | Decision-maker's Nash strategy |
| `nash_cp` | `tuple[float, float]` | Counter-party's Nash strategy |
| `contract_error` | `Optional[str]` | Breach reason, if any |

**Defaults:** `nash_dm = (0.5, 0.5)`, `nash_cp = (0.5, 0.5)`.

---

## `janus.orchestrator.Orchestrator`

The public attributes added for downstream consumers:

| Attribute | Type | Description |
|---|---|---|
| `last_snapshot` | `MarketSnapshot \| None` | The snapshot passed to the most recent `tick()` |
| `last_agop_result` | `AgopResult \| None` | The normalised AGOP output from the most recent tick |
| `last_intent` | `TradeIntent \| None` | The certified intent from the most recent tick |
| `last_module_contexts` | `dict[str, dict]` | The flattened module contributions |

These are populated on every call to `tick()`. STIRPES consumes them.

---

## Complexity summary

| Operation | Time | Space |
|---|---|---|
| `extract_fingerprint` | `O(\|V\| + \|modules\|)` | `O(\|V\| + \|modules\|)` |
| `canonical_form` | `O(\|f\| log \|f\|)` | `O(\|f\|)` |
| `class_hash` | `O(\|f\|)` | `O(\|f\|)` |
| `distance_components` | `O(T_persist + T_WL + T_W2)` | `O(1)` |
| `distance_matrix` | `O(n² · (T_persist + T_WL + T_W2))` | `O(n²)` |
| `build_tree` (NJ) | `O(n³)` | `O(n²)` |
| `build_tree` (UPGMA) | `O(n³)` | `O(n²)` |
| `clade_hash_from_labels` | `O(\|C\| log \|C\|)` | `O(\|C\|)` |
| `pagels_lambda` | `O(n³)` | `O(n²)` |
| `blombergs_k` | `O(n³)` | `O(n²)` |
| `StirpesRecorder.record` | `O(\|f\|)` | `O(\|f\|)` |
| `StirpesRecorder.flush` | `O(n³)` | `O(n²)` |
| `StirpesRecorder.settle` | `O(\|chain\|)` | `O(\|chain\|)` |

---

## Type invariants

1. `Fingerprint.topology` is sorted.
2. `Fingerprint.lower_confidence_bound` is sorted.
3. `Fingerprint.composite_score` is sorted.
4. `Fingerprint.verdict ∈ ALL_VERDICTS`.
5. `SettlementBatch` columns have equal length.
6. `ClassHash`, `CladeHash`, `TickHash`, `PayloadHash` are 32-byte
   `bytes` values.
7. `TreeNode.parent` is consistent with the parent's `children` list.
8. `AgopResult.nash_dm` and `AgopResult.nash_cp` are 2-tuples of floats
   in `[0, 1]`.

The `__post_init__` methods of `Fingerprint` and `SettlementBatch`
enforce invariants 1–5.