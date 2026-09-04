import time
import functools
import random

def resilient_network_call(max_retries=3, base_delay=1.0, backoff=2.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            current_delay = base_delay
            while retries <= max_retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    retries += 1
                    if retries > max_retries:
                        raise e
                    # Exponential backoff with jitter for chain stability
                    jitter = random.uniform(0, 0.1 * current_delay)
                    time.sleep(current_delay + jitter)
                    current_delay *= backoff
        return wrapper
    return decorator

class NetworkGuard:
    """Context manager for wrapping unstable RPC calls."""
    def __init__(self, retries=3):
        self.retries = retries

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type in (ConnectionError, TimeoutError):
            return True
        return False

def batch_process_with_retries(items, operation):
    results = []
    for item in items:
        @resilient_network_call(max_retries=2)
        def exec_op():
            return operation(item)
        results.append(exec_op())
    return results