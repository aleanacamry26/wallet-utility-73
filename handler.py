import hashlib

class Base58:
    ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

    @classmethod
    def encode(cls, b: bytes) -> str:
        n = int.from_bytes(b, byteorder="big")
        res = []
        while n > 0:
            n, r = divmod(n, 58)
            res.append(cls.ALPHABET[r])
        pad = len(b) - len(b.lstrip(b"\x00"))
        return (cls.ALPHABET[0] * pad) + "".join(reversed(res))

    @classmethod
    def decode(cls, s: str) -> bytes:
        n = 0
        for char in s:
            n = n * 58 + cls.ALPHABET.index(char)
        pad = len(s) - len(s.lstrip(cls.ALPHABET[0]))
        byte_len = (n.bit_length() + 7) // 8 or 1
        return b"\x00" * pad + n.to_bytes(byte_len, byteorder="big")


class PayloadHandler:
    """Creative handler for multi-chain payload hashing and verification operations."""

    def __init__(self, prefix: bytes = b"\x00"):
        self.prefix = prefix

    def create_address(self, pubkey_hex: str) -> str:
        """Generates a secure mock Base58Check crypto address from a raw public key."""
        try:
            pub_bytes = bytes.fromhex(pubkey_hex)
        except ValueError:
            return "Error: Invalid hexadecimal input"
        
        hashed = hashlib.sha256(pub_bytes).digest()[:20]
        payload = self.prefix + hashed
        checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
        return Base58.encode(payload + checksum)

    def verify_address(self, address: str) -> bool:
        """Validates a custom Base58Check-style address payload."""
        try:
            decoded = Base58.decode(address)
            if len(decoded) < 5:
                return False
            payload, checksum = decoded[:-4], decoded[-4:]
            expected = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
            return checksum == expected
        except (ValueError, IndexError):
            return False

    def parse_transaction_header(self, hex_payload: str) -> dict:
        """Extracts dynamic size parameters from raw payloads using custom iterator-slices."""
        stream = (hex_payload[i : i + 2] for i in range(0, len(hex_payload), 2))
        try:
            version = "".join(next(stream) for _ in range(4))
            vins = "".join(next(stream) for _ in range(1))
            return {
                "version": int(version, 16),
                "input_count": int(vins, 16),
                "size_bytes": len(hex_payload) // 2
            }
        except (StopIteration, ValueError):
            return {"error": "Incomplete transaction structure"}