import json
import os
from typing import Any, Dict

DEFAULT_CRYPTO_CONFIG: Dict[str, Any] = {
    "network": "ethereum",
    "chain_id": 1,
    "rpc_url": "https://eth-mainnet.g.alchemy.com/v2/demo",
    "gas_limit": 21000,
    "max_fee_per_gas_gwei": 30.0,
    "derivation_path": "m/44'/60'/0'/0/0",
    "enable_websocket": False,
    "tx_timeout_seconds": 120,
}


class ConfigProxy:
    """Dynamic crypto wallet configuration blending JSON files and environment variables."""

    def __init__(self, defaults: Dict[str, Any], env_prefix: str = "WALLET_"):
        self._data = dict(defaults)
        self._prefix = env_prefix

    def __getattr__(self, name: str) -> Any:
        key = name.lower()
        env_key = f"{self._prefix}{name.upper()}"

        if env_key in os.environ:
            return self._cast(self._data.get(key), os.environ[env_key])

        if key in self._data:
            return self._data[key]

        raise AttributeError(f"Config option '{name}' is not defined")

    def _cast(self, reference: Any, raw: str) -> Any:
        if reference is None:
            return raw
        target_type = type(reference)
        if target_type is bool:
            return raw.lower() in ("1", "true", "yes", "on")
        try:
            return target_type(raw)
        except (ValueError, TypeError):
            return raw

    def load_json(self, path: str) -> "ConfigProxy":
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    self._data.update(data)
        return self

    def export(self) -> Dict[str, Any]:
        return {k: getattr(self, k) for k in self._data}


config = ConfigProxy(DEFAULT_CRYPTO_CONFIG)
