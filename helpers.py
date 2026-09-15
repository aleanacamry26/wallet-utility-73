import time
import hashlib
import functools
from typing import Callable, Any, Tuple, Type

def entropy_retry(
    max_attempts: int = 5,
    base_delay: float = 1.0,
    backoff_factor: float = 1.618,
    allowed_exceptions: Tuple[Type[BaseException], ...] = (Exception,)
) -> Callable:
    """
    A deterministic, entropy-seeded retry decorator designed to prevent thundering herd
    problems on blockchain RPC endpoints by using state-hash jitter.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            state_str = f"{func.__name__}:{str(args)}:{str(sorted(kwargs.items()))}"
            entropy = int(hashlib.sha256(state_str.encode()).hexdigest(), 16)
            delay = base_delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except allowed_exceptions as err:
                    if attempt == max_attempts:
                        raise err
                    jitter_factor = 0.5 + ((entropy + attempt) % 10000) / 10000.0
                    time.sleep(delay * jitter_factor)
                    delay *= backoff_factor
        return wrapper
    return decorator