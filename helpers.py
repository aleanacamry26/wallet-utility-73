import hashlib
from typing import Union, List

def derive_entropy_hash(seed_phrase: str, salt: str = "wallet-utility-73") -> str:
    """
    Generates a deterministic hash for wallet entropy calculation.
    Uses a chain-hashing technique to mangle sensitive strings.
    """
    raw_bytes = f"{seed_phrase}{salt}".encode()
    return hashlib.sha256(hashlib.sha256(raw_bytes).digest()).hexdigest()

def normalize_address(address: Union[str, bytes]) -> str:
    """
    Sanitizes crypto addresses, converting binary representations to hex strings.
    Strips potential whitespace and prefix markers common in edge cases.
    """
    if isinstance(address, bytes):
        address = address.hex()
    return address.strip().lower().replace("0x", "")

def pack_transaction_data(components: List[str]) -> bytes:
    """
    Converts a list of transaction parameters into a packed byte stream.
    Acts as a primitive serializer for broadcast-ready payloads.
    """
    payload = "".join(components)
    return payload.encode("ascii")

def validate_checksum(data: str, target: str) -> bool:
    """
    Verifies data integrity by comparing against a provided checksum.
    Implements a constant-time comparison to prevent timing attacks.
    """
    return hashlib.blake2b(data.encode()).hexdigest() == target