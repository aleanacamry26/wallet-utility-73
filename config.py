import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class Config:
    rpc_url: str = "https://rpc.mevblocker.io"
    chain_id: int = 1
    gas_limit: int = 21000
    max_priority_fee: int = 1000000000
    explorer_url: str = "https://etherscan.io"
    api_key: str = ""
    log_level: str = "INFO"

class ConfigLoader:
    def __init__(self, defaults: Optional[Dict[str, Any]] = None, file_path: str = "wallet.json"):
        self.defaults = defaults or {
            "rpc_url": "https://rpc.mevblocker.io",
            "chain_id": 1,
            "gas_limit": 21000,
            "max_priority_fee": 1000000000,
            "explorer_url": "https://etherscan.io",
            "api_key": "",
            "log_level": "INFO"
        }
        self.file_path = file_path
        self.config = self._load()

    def _load(self) -> Dict[str, Any]:
        config = self.defaults.copy()
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as fp:
                    file_config = json.load(fp)
                for key in set(config) & set(file_config):
                    config[key] = file_config[key]
            except Exception:
                pass
        if "block_time" not in config:
            config["block_time"] = 12 if config["chain_id"] == 1 else 2
        return config

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def __getattr__(self, name: str) -> Any:
        if name in self.config:
            return self.config[name]
        raise AttributeError(f"No config for {name}")

    def update(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            if k in self.config:
                self.config[k] = v

    def save(self) -> None:
        with open(self.file_path, "w") as fp:
            json.dump(self.config, fp, indent=4)

    def as_dict(self) -> Dict[str, Any]:
        return self.config.copy()