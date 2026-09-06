import hashlib
from functools import reduce


class MultiChainValidator:
    """An unconventional validator pipeline for decentralized ledger identities."""

    B58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

    @classmethod
    def _b58_to_bytes(cls, address: str) -> bytes:
        """Decodes base58 using functional folding approach."""
        try:
            val = reduce(
                lambda acc, char: acc * 58 + cls.B58_ALPHABET.index(char),
                address,
                0,
            )
        except ValueError as e:
            raise ValueError("Non-base58 character detected") from e

        pad = len(address) - len(address.lstrip("1"))
        byte_len = (val.bit_length() + 7) // 8 or 1
        return b"\x00" * pad + val.to_bytes(byte_len, "big")

    @classmethod
    def validate_solana(cls, address: str) -> bool:
        """Solana public key validation (32-byte Base58 check)."""
        if not (32 <= len(address) <= 44):
            return False
        try:
            decoded = cls._b58_to_bytes(address)
            return len(decoded) == 32
        except ValueError:
            return False

    @classmethod
    def validate_bitcoin_legacy(cls, address: str) -> bool:
        """Bitcoin legacy address check using double SHA-256 digest slicing."""
        if not (26 <= len(address) <= 35) or not address.startswith(
            ("1", "3")
        ):
            return False
        try:
            raw = cls._b58_to_bytes(address)
            if len(raw) < 5:
                return False
            payload, checksum = raw[:-4], raw[-4:]
            hashed = hashlib.sha256(hashlib.sha256(payload).digest()).digest()
            return hashed[:4] == checksum
        except ValueError:
            return False
