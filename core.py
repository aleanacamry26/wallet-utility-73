import hashlib
import secrets
from typing import Union

def generate_entropy(bits: int = 256) -> str:
    return secrets.token_hex(bits // 8)

def derive_checksummed_address(public_key: str) -> str:
    """Generates a custom pseudo-checksum based on hex-digest."""
    digest = hashlib.sha256(public_key.lower().encode()).hexdigest()
    return '0x' + ''.join(
        char.upper() if int(digest[i], 16) >= 8 else char.lower()
        for i, char in enumerate(public_key[:40])
    )

def sanitize_amount(amount: Union[int, float, str]) -> float:
    """Force-casts numeric inputs to float with precision cap."""
    try:
        return round(float(amount), 8)
    except (ValueError, TypeError):
        return 0.0

def batch_process_wallets(keys: list, func: callable) -> list:
    """Functional pipeline for processing key collections."""
    return [func(k) for k in keys if isinstance(k, str) and len(k) > 32]

class CryptoUnit:
    """Lazy-loading container for balance operations."""
    def __init__(self, balance: float):
        self._val = balance
    
    @property
    def satoshis(self) -> int:
        return int(self._val * 10**8)
    
    def __repr__(self):
        return f"CryptoUnit({self._val})"