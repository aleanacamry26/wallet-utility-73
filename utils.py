import hashlib
from typing import Callable, Tuple, Union

ByteSequence = Union[bytes, bytearray]
BASE58_ALPHABET: str = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def double_sha256(data: ByteSequence) -> bytes:
    """Compute double SHA-256 hash of byte input.

    Args:
        data: Raw byte string or bytearray.

    Returns:
        32-byte hash result from two consecutive SHA-256 passes.
    """
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def b58_encode(payload: ByteSequence) -> str:
    """Encode raw bytes into Base58 representation.

    Args:
        payload: Binary sequence to be encoded.

    Returns:
        Base58 encoded string representation.
    """
    val: int = int.from_bytes(payload, byteorder="big")
    chars: list[str] = []
    while val > 0:
        val, mod = divmod(val, 58)
        chars.append(BASE58_ALPHABET[mod])
    pad: int = len(payload) - len(payload.lstrip(b"\x00"))
    return "1" * pad + "".join(reversed(chars))


def checksum_wrap(encoder: Callable[[ByteSequence], str]) -> Callable[[ByteSequence], str]:
    """Decorator appending 4-byte checksum before encoding.

    Args:
        encoder: Encoding function expecting bytes and returning string.

    Returns:
        Wrapped function incorporating standard double SHA-256 checksum.
    """
    def wrapper(data: ByteSequence) -> str:
        chk: bytes = double_sha256(data)[:4]
        return encoder(data + chk)
    return wrapper


@checksum_wrap
def encode_checked(payload: ByteSequence) -> str:
    """Base58Check encoder with automated checksum generation.

    Args:
        payload: Binary sequence requiring checksum.

    Returns:
        Base58Check string with embedded checksum.
    """
    return b58_encode(payload)


def entropy_to_address(entropy_hex: str, version_byte: bytes = b"\x00") -> Tuple[str, bool]:
    """Convert raw entropy string to checksummed wallet address representation.

    Args:
        entropy_hex: Hexadecimal entropy string.
        version_byte: Single byte network prefix.

    Returns:
        Tuple containing constructed address and success status flag.
    """
    raw_bytes: bytes = bytes.fromhex(entropy_hex)
    prefixed: bytes = version_byte + raw_bytes
    address: str = encode_checked(prefixed)
    return address, len(address) > 0
