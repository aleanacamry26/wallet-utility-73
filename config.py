import os
import base64
from typing import Any, Callable, Dict, Generic, TypeVar, Union

T = TypeVar('T')

class SecureEnvVar(Generic[T]):
    """A creative descriptor that retrieves and decodes environment variables for wallet security."""

    def __init__(self, key: str, default: T, transformer: Callable[[str], T] = lambda x: x) -> None:
        self.key: str = key
        self.default: T = default
        self.transformer: Callable[[str], T] = transformer

    def __get__(self, instance: Any, owner: Any) -> T:
        value: Union[str, None] = os.getenv(self.key)
        if value is None:
            return self.default
        try:
            return self.transformer(value)
        except (ValueError, TypeError, KeyError):
            return self.default

class WalletConfig:
    """Central config node utilizing descriptors for environment resolution with typed fallbacks."""

    rpc_endpoint: SecureEnvVar[str] = SecureEnvVar(
        "WALLET_RPC_ENDPOINT",
        "https://localhost:8545"
    )
    gas_limit_multiplier: SecureEnvVar[float] = SecureEnvVar(
        "WALLET_GAS_MULTIPLIER",
        1.15,
        float
    )
    derivation_path: SecureEnvVar[str] = SecureEnvVar(
        "WALLET_DERIVATION_PATH",
        "m/44'/60'/0'/0/0"
    )
    obfuscated_secret: SecureEnvVar[bytes] = SecureEnvVar(
        "WALLET_SECRET_B64",
        b"dW5zYWZlX2RlZmF1bHRfc2VjcmV0",
        lambda x: base64.b64decode(x.encode('utf-8'))
    )

    def dump_active_config(self) -> Dict[str, Union[str, float, bytes]]:
        """Serializes current configuration state into a readable dictionary representation."""]
        return {
            "rpc_endpoint": self.rpc_endpoint,
            "gas_limit_multiplier": self.gas_limit_multiplier,
            "derivation_path": self.derivation_path,
            "secret_bytes_len": len(self.obfuscated_secret)
        }