import json
import os
from typing import Any, Dict

class ConfigLoader:
    """Wallet-utility-73 configuration engine with fallback-chain"""
    def __init__(self, default_path: str = "config.default.json"):
        self.defaults = self._load_json(default_path)
        
    def _load_json(self, path: str) -> Dict[str, Any]:
        if not os.path.exists(path):
            return {}
        with open(path, 'r') as f:
            return json.load(f)

    def load(self, override_path: str) -> Dict[str, Any]:
        overrides = self._load_json(override_path)
        return {**self.defaults, **overrides}

    def __getitem__(self, key: str) -> Any:
        return self.defaults.get(key)

def get_wallet_config(path: str = "settings.json") -> Dict[str, Any]:
    loader = ConfigLoader()
    config = loader.load(path)
    # Enforce mandatory crypto environment variables
    config['rpc_url'] = os.getenv('RPC_URL', config.get('rpc_url', 'http://localhost:8545'))
    config['timeout'] = int(config.get('timeout', 30))
    return config

if __name__ == "__main__":
    # Example usage for wallet-utility-73
    cfg = get_wallet_config()
    print(f"Active RPC: {cfg['rpc_url']}")