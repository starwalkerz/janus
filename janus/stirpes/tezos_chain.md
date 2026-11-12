# STIRPES Tezos Chain Integration

Documentation for the `TezosChainClient` stub and the `StirpesRegistry`
Solidity contract. Every step is shown in full; no procedure is
abbreviated.

---

## 1. What the stub does

The `TezosChainClient` class in `janus/stirpes/chain.py` provides:

- A `commit(batch)` method that raises `NotImplementedError`.
- A `query(...)` method that raises `NotImplementedError`.
- A `latest_blocktime()` method that queries the connected RPC node for
  the latest block's timestamp.

The stub exists to define the interface. It does not implement
settlement, because settlement requires a deployed contract, an ABI, and
a signing key — all deployment-specific and not part of the STIRPES
mathematical core.

The `MockChainClient` is fully implemented and is what the test suite
exercises. It provides an in-memory equivalent that can be used for
development, testing, and dry runs.

---

## 2. What the stub does not do

The stub does not:

- Compile Solidity.
- Deploy contracts.
- Manage private keys.
- Handle gas estimation.
- Handle transaction retries.
- Handle reorgs.
- Verify the on-chain state against the off-chain log.

These are the responsibilities of the deployment layer, which is a
separate concern from STIRPES itself.

---

## 3. Prerequisites

To deploy the STIRPES settlement contract, you need:

### 3.1 The `web3` package

```bash
pip install web3
```

### 3.2 A Tezos L2 RPC endpoint

Etherlink mainnet public RPC is available at
`https://node.mainnet.etherlink.com`. For a private Tezos rollup, use the
operator-provided RPC URL.

### 3.3 An account with gas funds

The account that deploys and commits to the contract must have XTZ (on
Etherlink) or the L2's gas token (on a private rollup) to pay for
transaction gas. At $0.001 per transaction on Etherlink, the deployment
cost is negligible.

### 3.4 The `StirpesRegistry.sol` contract

The contract is at `contracts/StirpesRegistry.sol`. It must be compiled
with `solc` version 0.8.20 or later.

---

## 4. Deployment steps

### 4.1 Compile

Using `solc`:

```bash
solc --bin --abi --optimize -o build/ contracts/StirpesRegistry.sol
```

Using Hardhat:

```bash
npx hardhat compile
```

Using Foundry:

```bash
forge build
```

The output is two files: `StirpesRegistry.bin` (bytecode) and
`StirpesRegistry.abi` (ABI).

### 4.2 Deploy

Using `web3.py`:

```python
import json
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://node.mainnet.etherlink.com"))
account = w3.eth.account.from_key("0x...")

with open("build/StirpesRegistry.abi") as f:
    abi = json.load(f)
with open("build/StirpesRegistry.bin") as f:
    bytecode = f.read().strip()

contract = w3.eth.contract(abi=abi, bytecode=bytecode)
tx = contract.constructor().build_transaction({
    "from": account.address,
    "nonce": w3.eth.get_transaction_count(account.address),
    "gas": 3_000_000,
    "gasPrice": w3.eth.gas_price,
})
signed = account.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Deployed at {receipt.contractAddress}")
```

Record the deployed address. You will need it for the client
configuration.

### 4.3 Verify

Confirm the deployment by calling a read-only function:

```python
deployed = w3.eth.contract(address=receipt.contractAddress, abi=abi)
assert deployed.functions.getTicksByClass(b"\x00" * 32).call() == []
```

---

## 5. Contract interface

### `commitBatch`

```solidity
function commitBatch(
    bytes32[] calldata tickHashes,
    bytes32[] calldata classHashes,
    bytes32[] calldata cladeHashes,
    bytes32[] calldata sessionIds,
    uint256[] calldata tickIndices,
    bytes32[] calldata payloadHashes,
    bytes32 leafSetHash,
    bytes32 treeRootHash
) external;
```

Emits `TickCommitted` once per tick and `BatchCommitted` once for the
batch. Rejects duplicate tick hashes.

### `getTicksByClass`

```solidity
function getTicksByClass(bytes32 classHash) external view returns (bytes32[] memory);
```

Returns all tick hashes with the given class hash.

### `getTicksByClade`

```solidity
function getTicksByClade(bytes32 cladeHash) external view returns (bytes32[] memory);
```

Returns all tick hashes in the given clade.

### `getTicksBySession`

```solidity
function getTicksBySession(bytes32 sessionId) external view returns (bytes32[] memory);
```

Returns all tick hashes in the given session.

### `ticks`

```solidity
mapping(bytes32 => TickRecord) public ticks;
```

The public getter for the per-tick record.

---

## 6. Implementing the client

Extend `TezosChainClient` to implement `commit` and `query` against the
deployed contract:

```python
import json
from janus.stirpes.chain import TezosChainClient
from janus.stirpes.contracts import (
    SettlementBatch,
    SettlementRecord,
    SessionId,
)

class EtherlinkClient(TezosChainClient):
    def __init__(self, rpc_url, contract_address, private_key, abi_path):
        super().__init__(rpc_url, contract_address, private_key)
        with open(abi_path) as f:
            self.abi = json.load(f)
        self._contract = self.web3.eth.contract(
            address=contract_address, abi=self.abi,
        )

    def commit(self, batch: SettlementBatch) -> bytes:
        account = self.web3.eth.account.from_key(self.private_key)
        tx = self._contract.functions.commitBatch(
            list(batch.tick_hashes),
            list(batch.class_hashes),
            list(batch.clade_hashes),
            [s.encode("utf-8") for s in batch.session_ids],
            list(batch.tick_indices),
            list(batch.payload_hashes),
            batch.leaf_set_hash,
            batch.tree_root_hash,
        ).build_transaction({
            "from": account.address,
            "nonce": self.web3.eth.get_transaction_count(account.address),
            "gas": 3_000_000,
            "gasPrice": self.web3.eth.gas_price,
        })
        signed = account.sign_transaction(tx)
        tx_hash = self.web3.eth.send_raw_transaction(signed.rawTransaction)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt.transactionHash

    def query(
        self,
        class_hash=None,
        clade_hash=None,
        session_id=None,
        time_range=None,
    ) -> list[SettlementRecord]:
        if class_hash is not None:
            tick_hashes = self._contract.functions.getTicksByClass(
                class_hash,
            ).call()
        elif clade_hash is not None:
            tick_hashes = self._contract.functions.getTicksByClade(
                clade_hash,
            ).call()
        elif session_id is not None:
            tick_hashes = self._contract.functions.getTicksBySession(
                session_id.encode("utf-8"),
            ).call()
        else:
            raise ValueError("at least one filter is required")

        records = []
        for tick_hash in tick_hashes:
            tick_record = self._contract.functions.ticks(tick_hash).call()
            record = SettlementRecord(
                tick_hash=tick_record[0],
                class_hash=tick_record[1],
                historical_clade_hash=tick_record[2],
                session_id=tick_record[3].decode("utf-8"),
                tick_index=tick_record[4],
                blocktime=tick_record[5],
                payload_hash=tick_record[6],
            )
            if time_range is not None:
                lo, hi = time_range
                if not (lo <= record.blocktime <= hi):
                    continue
            records.append(record)
        return records
```

The extension preserves the `AbstractChainClient` interface and can be
used in place of `MockChainClient` in the `StirpesRecorder`.

---

## 7. Configuration

Configuration for the deployment, in `config.toml`:

```toml
[stirpes]
rpc_url = "https://node.mainnet.etherlink.com"
contract_address = "0x..."
private_key_env = "STIRPES_PRIVATE_KEY"
```

The `private_key_env` field points at an environment variable, not a
literal key. The client reads the key from the environment at
construction time and never stores it in configuration.

The recommended deployment workflow is:

1. Deploy the contract once per L2 network (mainnet, testnet, private).
2. Record the deployed address in the configuration.
3. Set the private key as an environment variable.
4. Use `EtherlinkClient` (or the private-rollup equivalent) in place of
   `MockChainClient`.

---

## 8. Testing without Tezos

`MockChainClient` is fully functional and requires no deployment. The
test suite uses it exclusively. For local development:

```python
from janus.stirpes import MockChainClient, StirpesRecorder, XorCipher

chain = MockChainClient(blocktime_seconds=1)
recorder = StirpesRecorder(chain=chain, cipher=XorCipher())

# Record and flush; the mock handles commit and query in memory.
```

The mock's `latest_blocktime()` returns
`block_counter * blocktime_seconds`, which is deterministic. Its
`commit` produces a deterministic tx hash. Its `query` filters the
in-memory list.

When you are ready to test against a real chain, swap `MockChainClient`
for `EtherlinkClient`. The interface is identical.

---

## 9. Gas costs

The contract's `commitBatch` function writes:

- 7 storage slots per tick (one `TickRecord` struct).
- 3 storage slot appends per tick (`classIndex`, `cladeIndex`,
  `sessionIndex`).
- 2 event emissions per tick (`TickCommitted`, one per tick).

The per-tick gas cost is approximately:

| Operation | Gas |
|---|---|
| Struct write | ~80,000 |
| Three index appends | ~60,000 |
| Event emission | ~2,000 |
| **Total per tick** | **~142,000** |

At Etherlink's gas price (typically 1 gwei or less), the per-tick cost
is approximately $0.00014. A batch of 100 ticks costs approximately
$0.014. This is well within any operational budget.

For a private Tezos rollup, the gas price is set by the rollup
operator. The same computation applies with the operator's gas price.

---

## 10. Reorg handling

Etherlink and Tezos Smart Rollups provide finality through Tezos'
two-block guarantee, which is approximately 30 seconds. Transactions
that have received two confirmations are final and will not be reorged.

For STIRPES, this means:

- Wait for two confirmations before treating a settlement record as
  final.
- The `MockChainClient` does not model reorgs; production clients must.

If a reorg occurs before finality, the settlement record may disappear.
The recorder's `historical_ticks` list is the local record; if the
on-chain record disappears but the local record persists, the operator
must re-commit the batch. This is an operational concern, not an
architectural one.

---

## 11. Limitations

**ABI dependency.** The client requires the ABI JSON file. This file is
the interface; if the contract changes, the ABI changes, and the client
must be updated.

**No data availability.** The contract stores hashes; it does not store
the payloads. The payloads must be stored in a data-availability layer
(IPFS, Arweave, or a dedicated DA layer). The reveal endpoint in
`api.py` accepts the ciphertext directly, which is only useful for
testing; production must retrieve it from the DA layer by hash.

**No token integration.** The `RevealGate` checks a `TokenLedger`, but
the ledger is abstract. The deployment must wire it to an actual token
contract. The token's mechanics (minting, burning, transferring) are out
of scope for STIRPES.

**No ZK.** STIRPES does not implement zero-knowledge proofs. The
on-chain record is a commitment to the off-chain content; verifying the
content against the commitment requires the off-chain payload, not a
ZK proof. This is the right choice for the current deployment scale, but
a future version may add ZK selective disclosure for specific
predicates.

**Single deployer.** The contract's `commitBatch` function has no access
control. In a production deployment with multiple operators, an
`onlyOperator` modifier is required to prevent arbitrary parties from
committing records. The current version assumes a single trusted
deployer.

**No pausing or upgrading.** The contract is immutable. If a bug is
found, the fix requires deploying a new contract and migrating. The
migration is the operator's responsibility.