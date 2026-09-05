import collections
import json
import os
import secrets
from typing import Any, Dict


class CryptoConfig(collections.ChainMap):
    """Dynamic configuration manager with crypto-specific fallback generators."""

    DEFAULTS: Dict[str, Any] = {
        "CRYPTO_NETWORK": "mainnet",
        "DERIVATION_PATH": "m/44'/60'/0'/0/0",
        "RPC_TIMEOUT": 15,
        "GAS_MULTIPLIER": 1.15,
        "AUTO_NONCE": True,
    }

    def __init__(self, filepath: str | None = None):
        # Layer 1: Environment variables (prefixed with CW_)
        env_config = {
            k[3:]: self._parse_val(v)
            for k, v in os.environ.items()
            if k.startswith("CW_")
        }

        # Layer 2: Local JSON configuration
        file_config = {}
        if filepath and os.path.exists(filepath):
            with open(filepath, "r") as f:
                file_config = json.load(f)

        # Layer 3: Hardcoded defaults
        super().__init__(env_config, file_config, self.DEFAULTS)

    @staticmethod
    def _parse_val(val: str) -> Any:
        try:
            return json.loads(val.lower())
        except (ValueError, TypeError):
            return val

    def __getitem__(self, key: str) -> Any:
        try:
            return super().__getitem__(key)
        except KeyError:
            return self._generate_dynamic_fallback(key)

    def _generate_dynamic_fallback(self, key: str) -> Any:
        # Lazily self-populate critical, missing crypto-secrets in the session layer
        if key == "ENCRYPTION_SALT":
            generated_salt = secrets.token_hex(16)
            self.maps[0][key] = generated_salt
            return generated_salt
        if key == "WALLET_IDENTIFIER":
            generated_id = f"wallet-{secrets.token_hex(4)}"
            self.maps[0][key] = generated_id
            return generated_id
        raise KeyError(f"Configuration key '{key}' is not defined and has no default")

    def get_as_float(self, key: str) -> float:
        return float(self[key])

    def dump_active_config(self) -> str:
        merged = dict(self)
        if "ENCRYPTION_SALT" in merged:
            merged["ENCRYPTION_SALT"] = "[REDACTED]"
        return json.dumps(merged, indent=2)
