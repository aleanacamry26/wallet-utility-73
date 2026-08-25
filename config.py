import json
from functools import lru_cache

class Config:
    def __init__(self, config_path=None):
        self._data = {}
        self._performance_cache = {}
        if config_path:
            self.load_from_file(config_path)

    def load_from_file(self, path):
        with open(path, "r") as f:
            self._data = json.load(f)
        self._optimize()

    def _optimize(self):
        flat = {}
        def flatten(d, parent_key=""):
            for k, v in d.items():
                new_key = f"{parent_key}.{k}" if parent_key else k
                if isinstance(v, dict):
                    flatten(v, new_key)
                else:
                    flat[new_key] = v
        flatten(self._data)
        self._flat_data = flat
        self._keys_set = set(flat.keys())

    def get(self, key, default=None):
        if key in self._performance_cache:
            return self._performance_cache[key]
        if key in self._keys_set:
            value = self._flat_data[key]
            self._performance_cache[key] = value
            return value
        return default

    @lru_cache(maxsize=128)
    def get_network_config(self, network):
        return self.get(f"networks.{network}", {})

    def get_wallet_setting(self, setting):
        return self.get(f"wallet.{setting}")

    def update(self, key, value):
        if "." in key:
            parts = key.split(".")
            d = self._data
            for p in parts[:-1]:
                if p not in d:
                    d[p] = {}
                d = d[p]
            d[parts[-1]] = value
        else:
            self._data[key] = value
        self._optimize()
        if key in self._performance_cache:
            del self._performance_cache[key]

    def clear_cache(self):
        self._performance_cache.clear()
        self.get_network_config.cache_clear()

DEFAULT_CONFIG = {
    "wallet": {
        "default_network": "ethereum",
        "timeout": 30
    },
    "networks": {
        "ethereum": {"rpc": "https://eth.rpc", "chain_id": 1},
        "bitcoin": {"rpc": "https://btc.rpc", "chain_id": 0}
    }
}

def get_default_config():
    c = Config()
    c._data = DEFAULT_CONFIG
    c._optimize()
    return c
