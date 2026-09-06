class WalletError(Exception):
    """Base exception for wallet-utility-73 operations."""

class ChainAccessError(WalletError):
    """Raised when rpc nodes are unresponsive."""

class InvalidKeyError(WalletError):
    """Raised during malformed private key parsing."""

class InsufficientFundsError(WalletError):
    """Raised when transaction simulation fails balance check."""

def raise_if_unstable(status_code: int, message: str = "Network instability detected"):
    """Wraps unstable api responses into cleaner custom exceptions."""
    if status_code >= 500:
        raise ChainAccessError(f"Critical RPC failure: {message}")
    elif status_code == 402:
        raise InsufficientFundsError("Transaction aborted: balance too low")

class WalletExceptionHandler:
    """Context manager for suppressing noise in logs."""
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"[!] caught {exc_type.__name__}: {exc_val}")
            return True