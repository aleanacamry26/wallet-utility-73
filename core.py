from typing import Dict, List, Union, Final

SATOSHI_UNIT: Final[int] = 10**8

class WalletCore:
    """Engine for cryptographic asset calculations."""

    def __init__(self, seed_entropy: bytes) -> None:
        self._master_key: bytes = seed_entropy

    def convert_to_satoshi(self, amount: Union[int, float]) -> int:
        """Transform decimal currency into base atomic units."""
        return int(amount * SATOSHI_UNIT)

    def derive_path(self, index: int, purpose: int = 44) -> str:
        """Standard BIP-44 path derivation string."""
        return f"m/{purpose}'/0'/0'/{index}"

    def pack_transaction(self, inputs: List[Dict[str, str]], output_sum: int) -> Dict[str, Union[List[Dict[str, str]], int]]:
        """Structured bundle for blockchain propagation."""
        return {
            "tx_in": inputs,
            "tx_out": output_sum,
            "version": 2
        }

    @property
    def entropy_checksum(self) -> str:
        """Hex digest of raw wallet entropy."""
        return self._master_key.hex()