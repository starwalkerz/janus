"""
Payload encryption and token-gated reveal.

The default cipher is a placeholder XOR cipher for testing. Production
deployments substitute AES-GCM or ChaCha20-Poly1305.
"""

from __future__ import annotations

import hashlib
import os
from abc import ABC, abstractmethod

from janus.stirpes.contracts import PayloadHash


class PayloadCipher(ABC):
    """The payload encryption interface."""

    @abstractmethod
    def encrypt(self, plaintext: bytes) -> bytes:
        ...

    @abstractmethod
    def decrypt(self, ciphertext: bytes) -> bytes:
        ...


class XorCipher(PayloadCipher):
    """Placeholder XOR cipher. NOT secure. For testing only.

    The key is derived from a fixed seed. The same seed must be used for
    encrypt and decrypt.
    """

    def __init__(self, seed: bytes = b"stirpes-test-seed") -> None:
        self.key = hashlib.sha256(seed).digest() * 32  # 1024-byte keystream

    def encrypt(self, plaintext: bytes) -> bytes:
        return bytes(b ^ self.key[i % len(self.key)] for i, b in enumerate(plaintext))

    def decrypt(self, ciphertext: bytes) -> bytes:
        return self.encrypt(ciphertext)  # XOR is its own inverse


class RevealGate:
    """Token-gated reveal.

    Two payment modes:
        - balance-based: the caller must hold at least `min_balance` tokens
        - transfer-based: the caller must have transferred at least
          `min_transfer` tokens to the operator's address in the
          current epoch

    Both are checked against an abstract `TokenLedger` interface, which
    the deployment wires to the actual token contract.
    """

    def __init__(
        self,
        token_ledger: "TokenLedger",
        min_balance: int = 0,
        min_transfer: int = 0,
        operator_address: str = "0x0",
    ) -> None:
        self.token_ledger = token_ledger
        self.min_balance = min_balance
        self.min_transfer = min_transfer
        self.operator_address = operator_address

    def check_and_reveal(
        self,
        caller_address: str,
        payload_hash: PayloadHash,
        ciphertext: bytes,
        cipher: PayloadCipher,
    ) -> bytes | None:
        """Return the plaintext if payment is sufficient, else None."""
        if not self._is_paid(caller_address):
            return None
        # Verify the ciphertext matches the committed hash
        computed_hash = hashlib.sha256(ciphertext).digest()
        if computed_hash != bytes(payload_hash):
            raise ValueError("ciphertext does not match payload hash")
        return cipher.decrypt(ciphertext)

    def _is_paid(self, caller_address: str) -> bool:
        if self.min_balance > 0:
            balance = self.token_ledger.balance_of(caller_address)
            if balance < self.min_balance:
                return False
        if self.min_transfer > 0:
            transferred = self.token_ledger.transferred_to(
                caller_address, self.operator_address,
            )
            if transferred < self.min_transfer:
                return False
        return True


class TokenLedger(ABC):
    """Abstract token ledger interface."""

    @abstractmethod
    def balance_of(self, address: str) -> int:
        ...

    @abstractmethod
    def transferred_to(self, from_address: str, to_address: str) -> int:
        ...