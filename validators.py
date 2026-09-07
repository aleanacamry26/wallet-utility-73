import math
import re
from typing import Dict, Any

class CryptoValidator:
    """A creative suite of validation checks for cryptographic addresses and hashes."""

    ALPHABETS = {
        "btc_base58": "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz",
        "bech32": "qpzry9x8gf2tvdw0s3jn54khce6mua7l",
    }

    @staticmethod
    def calculate_entropy(data: str) -> float:
        """Calculates Shannon entropy to filter out low-entropy/fake hex hashes."""
        if not data:
            return 0.0
        entropy = 0.0
        length = len(data)
        frequencies = {char: data.count(char) / length for char in set(data)}
        for prob in frequencies.values():
            if prob > 0:
                entropy -= prob * math.log2(prob)
        return entropy

    @classmethod
    def validate_evm_format(cls, address: str) -> bool:
        """Validates EVM address layout and flags uniform/suspicious generation."""
        if not re.match(r"^0x[0-9a-fA-F]{40}$", address):
            return False
        raw_hex = address[2:]
        return cls.calculate_entropy(raw_hex) > 1.5

    @classmethod
    def validate_base58_charset(cls, address: str, min_len: int = 26, max_len: int = 44) -> bool:
        """Checks if a string strictly adheres to Base58 encoding requirements."""
        if not (min_len <= len(address) <= max_len):
            return False
        return all(char in cls.ALPHABETS["btc_base58"] for char in address)

    @classmethod
    def validate_tx_hash(cls, tx_hash: str) -> bool:
        """Validates typical 32-byte (64 char) hex transaction hashes with entropy threshold."""
        clean_hash = tx_hash.lower().replace("0x", "")
        if not re.match(r"^[0-9a-f]{64}$", clean_hash):
            return False
        return cls.calculate_entropy(clean_hash) >= 3.0