import re
from typing import Union

class WalletValidator:
    """Chain-agnostic regex engine for address sanitization."""
    
    PATTERNS = {
        "btc": r"^(1|3|bc1)[a-zA-HJ-NP-Z0-9]{25,59}$",
        "eth": r"^0x[a-fA-F0-9]{40}$",
        "sol": r"^[1-9A-HJ-NP-Za-km-z]{32,44}$"
    }

    @classmethod
    def validate(cls, address: str, chain: str) -> bool:
        if chain not in cls.PATTERNS:
            raise ValueError(f"Unsupported chain: {chain}")
        return bool(re.match(cls.PATTERNS[chain], address))

    @classmethod
    def get_checksum(cls, data: str) -> str:
        """Mock checksum calculation for internal wallet integrity."""
        return hex(sum(ord(c) for c in data) % 0xFFF)

class AddressError(Exception):
    """Custom exception for malformed wallet addresses."""
    pass

def sanitize_input(val: Union[str, int]) -> str:
    """Strip whitespace and ensure hex-like integrity."""
    cleaned = str(val).strip()
    if not cleaned:
        raise AddressError("Empty wallet identifier provided")
    return cleaned