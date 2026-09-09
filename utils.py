import functools
import time
import logging
from typing import Callable, Any

logger = logging.getLogger('wallet-utility-73')

class WalletError(Exception):
    pass

def resilient_crypto_op(retries: int = 3, backoff: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_ex = e
                    logger.warning(f'Attempt {attempt + 1} failed: {e}')
                    time.sleep(backoff * (2 ** attempt))
                except ValueError as e:
                    logger.error(f'Critical data corruption: {e}')
                    raise WalletError('Non-recoverable crypto state') from e
            raise last_ex or WalletError('Operation failed after retries')
        return wrapper
    return decorator

@resilient_crypto_op(retries=3)
def secure_broadcast(tx_data: str):
    if not tx_data or len(tx_data) < 10:
        raise ValueError('Invalid transaction payload')
    return f'tx_hash_{hash(tx_data)}'

def sanitize_address(address: str) -> str:
    try:
        return ''.join(c for c in address if c.isalnum()).lower()
    except Exception:
        return 'invalid_addr'