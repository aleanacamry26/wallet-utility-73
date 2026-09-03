import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any] = None, env_prefix: str = "W73_"):
        self._data = defaults or {}
        self._prefix = env_prefix
        self._load_from_env()

    def _load_from_env(self) -> None:
        for key, value in os.environ.items():
            if key.startswith(self._prefix):
                config_key = key[len(self._prefix):].lower()
                self._data[config_key] = self._cast_value(value)

    def _cast_value(self, val: str) -> Any:
        if val.lower() in ('true', 'yes'): return True
        if val.lower() in ('false', 'no'): return False
        try: return int(val)
        except ValueError:
            try: return float(val)
            except ValueError: return val

    def get(self, key: str, fallback: Any = None) -> Any:
        return self._data.get(key, fallback)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __repr__(self) -> str:
        return f"ConfigStore(keys={list(self._data.keys())})"

# Quick singleton injection
settings = ConfigLoader({
    "rpc_url": "https://mainnet.infura.io/v3/",
    "timeout": 30,
    "debug_mode": False
})