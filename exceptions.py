import time
import functools
import logging

class NetworkError(Exception):
    """Base exception for crypto wallet network operations."""
    pass

class ExponentialBackoff:
    def __init__(self, retries=3, base_delay=1.0):
        self.retries = retries
        self.base_delay = base_delay

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for attempt in range(self.retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    delay = self.base_delay * (2 ** attempt)
                    logging.warning(f"Retry {attempt+1}/{self.retries} after {delay}s due to {e}")
                    time.sleep(delay)
            raise last_ex
        return wrapper

retry_network = ExponentialBackoff(retries=5, base_delay=0.5)

def validate_response(func):
    @functools.wraps(func)
    def checker(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None:
            raise NetworkError("Empty response from node")
        return result
    return checker