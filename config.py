import functools
import sys
from typing import Any, Callable

class HotCache:
    """A micro-optimization cache for static config lookups."""
    def __init__(self, limit: int = 128):
        self.limit = limit
        self.cache = {}
        self.keys = []

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any) -> Any:
            if args not in self.cache:
                if len(self.cache) >= self.limit:
                    self.cache.pop(self.keys.pop(0))
                self.cache[args] = func(*args)
                self.keys.append(args)
            return self.cache[args]
        return wrapper

config_store = {
    "provider_url": "https://mainnet.infura.io/v3/",
    "timeout": 30,
    "gas_buffer": 1.2
}

@HotCache(limit=32)
def get_chain_config(key: str) -> Any:
    """Fetches and memoizes config values with hot caching."""
    return config_store.get(key)

def get_system_load() -> float:
    """Aggressive syscall for environment awareness."""
    try:
        return float(open('/proc/loadavg').read().split()[0])
    except Exception:
        return 0.0

ACTIVE_REGIME = "aggressive" if get_system_load() < 2.0 else "conservative"