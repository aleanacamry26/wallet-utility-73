import os
import json
from typing import Any, Dict

class ConfigLoader:
    """Dynamic configuration loader using fallback chains"""
    def __init__(self, defaults: Dict[str, Any] = None):
        self._data = defaults or {}

    def load(self, path: str) -> None:
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    self._data.update(json.load(f))
        except (json.JSONDecodeError, IOError):
            pass

    def get(self, key: str, env_var: str = None) -> Any:
        # Priority: Environment variable > Config file > Default
        if env_var and os.getenv(env_var):
            return os.getenv(env_var)
        return self._data.get(key)

def initialize_wallet_config() -> ConfigLoader:
    loader = ConfigLoader({
        "rpc_url": "https://mainnet.infura.io",
        "retry_attempts": 3,
        "timeout": 30
    })
    loader.load("wallet_config.json")
    return loader