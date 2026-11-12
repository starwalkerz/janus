# STIRPES Usage Guide

A complete tutorial for integrating STIRPES into a JANUS deployment.
Every example is shown in full. No step is abbreviated.

---

## 1. Prerequisites

STIRPES is part of the JANUS package. It requires no additional
dependencies beyond what JANUS already installs, except for the `web3`
package if you intend to use the on-chain settlement layer.

```bash
pip install web3
```

The test suite requires `pytest`:

```bash
pip install pytest
```

---

## 2. The complete flow

A complete STIRPES flow has four steps:

1. **Record** — after each JANUS tick, extract the fingerprint and
   compute the class hash.
2. **Flush** — periodically, rebuild the phylogenetic tree and emit a
   settlement batch.
3. **Settle** — commit the batch to the chain.
4. **Query** — retrieve records by tick hash, clade hash, or session.

Each of these is shown below with complete code.

---

## 3. Constructing the recorder

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

---

## 4. Recording ticks

For every tick, call `orchestrator.tick(snapshot)` and then
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

The recorder maintains a persistent leaf set across flushes, so the
phylogenetic tree is built over the full history rather than the current
batch alone. This gives the tree topology stability across flushes.
Leaves are evicted FIFO once the set exceeds `MAX_LEAF_SET_SIZE = 2000`.

---

## 5. Flushing

When you want to settle, call `flush()` explicitly:

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

---

## 6. Querying

### 6.1 By tick

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

### 6.2 By clade

```python
from janus.stirpes import CladeHash

first_clade_hash = batch.clade_hashes[0]
clade_records = engine.by_clade(first_clade_hash)
print(f"Ticks in clade {first_clade_hash.hex()}: {len(clade_records)}")
for r in clade_records:
    print(f"  Tick {r.tick_hash.hex()} at blocktime {r.blocktime}")

recent = engine.by_clade(
    first_clade_hash,
    time_range=(0, 1_000_000_000),
)
print(f"Recent ticks in clade: {len(recent)}")
```

### 6.3 By session

```python
from janus.stirpes import SessionId

session_records = engine.by_session(SessionId("default-session"))
print(f"Ticks in session: {len(session_records)}")
for r in session_records:
    print(f"  {r.tick_hash.hex()} at tick index {r.tick_index}")
```

---

## 7. Signal tests

After flushing, you can run the phylogenetic signal tests on the tree:

```python
from janus.stirpes import pagels_lambda, blombergs_k
from janus.stirpes.distance import distance_matrix
from janus.stirpes.tree import build_tree

# Rebuild the tree from the recorder's full leaf set.
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

Interpretation:

- `λ ≈ 1`, `K ≈ 1`: strong phylogenetic signal, clades are informative.
- `λ ≈ 0.5`, `K ≈ 0.5`: moderate signal, use with caution.
- `λ ≈ 0`, `K ≈ 0`: no signal, do not use the clade structure.

Both tests are heuristics, not exact likelihood-ratio tests. The
Blomberg's K approximation uses sample variance rather than the exact
BM/star expected MSE. Treat the values as indicators.

---

## 8. Encryption and reveal

The default cipher is `XorCipher`. For production, use a real AEAD:

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

## 9. Integration patterns

### 9.1 Pattern A — synchronous recording

Call `recorder.record(...)` after every `orchestrator.tick(...)`:

```python
def trading_loop():
    while True:
        snapshot = fetch_snapshot()
        tick_record = orchestrator.tick(snapshot)
        recorder.record(
            agop_result=orchestrator.last_agop_result,
            module_contexts=orchestrator.last_module_contexts,
            snapshot=snapshot,
            verdict=tick_record["intent"].get("verdict", "pass"),
        )
```

This is the simplest pattern. The recorder accumulates pending ticks and
flushes when the threshold is reached.

### 9.2 Pattern B — asynchronous recording via queue

Push the tick record onto a queue and have a separate worker call
`record`:

```python
import queue
import threading

queue_in = queue.Queue()

def recorder_worker():
    while True:
        args = queue_in.get()
        if args is None:
            break
        recorder.record(**args)

thread = threading.Thread(target=recorder_worker, daemon=True)
thread.start()

# In the trading loop:
queue_in.put({
    "agop_result": orchestrator.last_agop_result,
    "module_contexts": orchestrator.last_module_contexts,
    "snapshot": snapshot,
    "verdict": tick_record["intent"].get("verdict", "pass"),
})
```

This decouples the trading loop from the recorder. The recorder's tree
rebuild is the expensive operation, so doing it off the hot path is
recommended for high-frequency strategies.

---

## 10. Configuration

STIRPES does not require configuration in `config.toml`. Its parameters
are passed to the `StirpesRecorder` constructor:

| Parameter | Default | Meaning |
|---|---|---|
| `chain` | required | The chain client (Mock or Tezos). |
| `cipher` | required | The payload cipher. |
| `tree_method` | `"neighbor_joining"` | `"neighbor_joining"` or `"upgma"`. |
| `flush_threshold` | 100 | Auto-flush after this many pending ticks. |
| `session_id` | `"default-session"` | Session identifier. |

---

## 11. Testing

The module ships with a test suite that exercises:

- Fingerprint extraction from `AgopResult` + module contexts.
- Fingerprint canonicalisation determinism.
- Class hash determinism and discrimination.
- Distance symmetry and triangle inequality.
- Tree construction correctness on tree-additive metrics.
- Clade hash determinism and membership sensitivity.
- Signal test range.
- Recorder record, flush, settle, and query.
- Historical leaf set persistence across flushes.
- Singleton leaf handling.
- Unidirectionality (structural).

Run with:

```bash
pytest tests/test_stirpes.py -v
```

---

## 12. Troubleshooting

**`ImportError: cannot import name '_shannon_entropy' from 'agop_core'`**
— STIRPES does not import from `agop_core`. If you see this error, you
are importing the wrong module. STIRPES is `janus.stirpes`, not
`agop_core`.

**`ValueError: fingerprint.topology must be sorted`**
— The `Fingerprint` constructor enforces sorted ordering of the tuple
fields. If you construct a `Fingerprint` directly (bypassing
`extract_fingerprint`), sort the tuples first.

**`KeyError: leaf 'xyz' not found`**
— The leaf label you passed to `clade_hash_for_leaf` is not in the tree.
Verify that the label matches the tree's leaf set.

**`RuntimeError: tree is disconnected`**
— The `lca` method found no common ancestor. This should not happen for
a properly constructed tree; if it does, the tree construction has a
bug. Report it.

**`Signal tests return NaN`**
— The trait vector has zero variance, or the covariance matrix is
singular. Check that the trait values are not constant.