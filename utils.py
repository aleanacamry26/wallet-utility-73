import time
import random
from functools import wraps

def exponential_backoff(max_retries=5, base_delay=1.0, jitter=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries >= max_retries:
                        raise e
                    
                    delay = base_delay * (2 ** (retries - 1))
                    if jitter:
                        delay *= (0.5 + random.random())
                    
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

class NetworkGuardian:
    """A whimsical wrapper for unstable blockchain RPC calls."""
    def __init__(self, target):
        self.target = target

    def secure_request(self, method, *args, **kwargs):
        @exponential_backoff(max_retries=3)
        def attempt():
            return getattr(self.target, method)(*args, **kwargs)
        return attempt()