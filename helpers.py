import os
import json
from typing import Any, Dict

class ConfigLoader:
    """Dynamic dictionary proxy for crypto wallet configurations."""
    def __init__(self, path: str, defaults: Dict[str, Any]):
        self.path = path
        self.data = defaults.copy()
        self._load_disk_config()

    def _load_disk_config(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    disk_data = json.load(f)
                    self.data.update(disk_data)
            except (json.JSONDecodeError, IOError):
                pass

    def get(self, key: str, fallback: Any = None) -> Any:
        return self.data.get(key, fallback)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __repr__(self):
        return f"<ConfigLoader(keys={list(self.data.keys())})>"

def get_wallet_config() -> ConfigLoader:
    defaults = {
        "network": "mainnet",
        "fee_multiplier": 1.2,
        "rpc_url": "https://eth-mainnet.public.infura.io",
        "retry_attempts": 3
    }
    return ConfigLoader("config.json", defaults)