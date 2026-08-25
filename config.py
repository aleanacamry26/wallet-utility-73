import json
import os
from typing import Any, Dict, Optional

DEFAULT_CONFIG = {
    "network": "ethereum",
    "rpc_endpoint": "https://mainnet.infura.io/v3/YOUR_KEY",
    "private_key": "",
    "gas_limit": 21000,
    "confirmations": 12,
    "timeout_seconds": 30,
    "debug_mode": False
}

class ConfigLoader:
    def __init__(self, config_path: str = "wallet_config.json"):
        self.config_path = config_path
        self._config: Dict[str, Any] = self._load_with_defaults()

    def _load_with_defaults(self) -> Dict[str, Any]:
        config = DEFAULT_CONFIG.copy()
        if os.path.isfile(self.config_path):
            try:
                with open(self.config_path, "r") as file:
                    loaded = json.load(file)
                    for key, value in loaded.items():
                        if key in config:
                            config[key] = value
            except (json.JSONDecodeError, IOError):
                pass
        for key in list(config.keys()):
            env_var = f"WALLET_UTILITY_{key.upper()}"
            if env_var in os.environ:
                env_val = os.environ[env_var]
                original = config[key]
                if isinstance(original, bool):
                    config[key] = env_val.lower() in ("true", "1", "yes")
                elif isinstance(original, int):
                    try:
                        config[key] = int(env_val)
                    except ValueError:
                        pass
                elif isinstance(original, float):
                    try:
                        config[key] = float(env_val)
                    except ValueError:
                        pass
                else:
                    config[key] = env_val
        return config

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self._config.get(key, default)

    def __getattr__(self, attr: str) -> Any:
        if attr in self._config:
            return self._config[attr]
        raise AttributeError(f"'{attr}' not in config")

    def set(self, key: str, value: Any) -> None:
        if key in self._config:
            self._config[key] = value

    def save(self) -> None:
        with open(self.config_path, "w") as file:
            json.dump(self._config, file, indent=2)

    def reload(self) -> None:
        self._config = self._load_with_defaults()