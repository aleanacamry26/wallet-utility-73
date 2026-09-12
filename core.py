import functools
import hashlib
import pickle
from typing import Any, Callable

class TransactionProcessor:
    def __init__(self, cache_size: int = 128):
        self._cache = {}
        self._max_size = cache_size

    def _memoize_hash(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = hashlib.blake2b(pickle.dumps((args, kwargs))).hexdigest()
            if key in self._cache:
                return self._cache[key]
            result = func(*args, **kwargs)
            if len(self._cache) >= self._max_size:
                self._cache.pop(next(iter(self._cache)))
            self._cache[key] = result
            return result
        return wrapper

    def sign_transaction(self, tx_data: dict, key: str) -> str:
        return self._secure_sign(tx_data, key)

    @functools.lru_cache(maxsize=1024)
    def _secure_sign(self, tx_data: dict, key: str) -> str:
        payload = str(tx_data).encode() + key.encode()
        return hashlib.sha3_256(payload).hexdigest()

    def batch_process(self, transactions: list, key: str) -> list:
        return [self.sign_transaction(tx, key) for tx in transactions]

def optimize_compute_performance(processor: TransactionProcessor) -> None:
    processor.sign_transaction = processor._memoize_hash(processor.sign_transaction)

if __name__ == '__main__':
    tp = TransactionProcessor()
    optimize_compute_performance(tp)