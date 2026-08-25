import typing

class WalletError(Exception):
    """Base class for wallet utility exceptions with creative error coding."""
    def __init__(self, message: str, error_code: int = 0, details: typing.Optional[dict] = None):
        super().__init__(message)
        self.error_code = error_code
        self.details = details or {}

    def to_dict(self) -> dict:
        """Unusual serialization for crypto API responses."""
        return {"error": str(self), "code": self.error_code, "details": self.details, "crypto_context": "wallet-utility-73"}

    def __repr__(self):
        return f"<WalletError code={self.error_code} msg='{str(self)}'>"

class InsufficientFunds(WalletError):
    """Raised when wallet balance is too low for operation."""
    def __init__(self, current: float, needed: float, asset: str = "ETH"):
        msg = f"Insufficient {asset} funds: have {current}, need {needed}"
        super().__init__(msg, error_code=42, details={"current": current, "needed": needed, "asset": asset})

class InvalidWalletAddress(WalletError):
    """For malformed or invalid blockchain addresses."""
    def __init__(self, address: str, network: str = "mainnet"):
        msg = f"Address '{address}' invalid on {network}"
        super().__init__(msg, 43, {"address": address, "network": network})

class TransactionFailure(WalletError):
    """When a crypto transaction cannot complete."""
    def __init__(self, reason: str, tx_id: typing.Optional[str] = None):
        msg = f"Tx failed: {reason}"
        details = {"reason": reason}
        if tx_id:
            details["tx_id"] = tx_id
        super().__init__(msg, 44, details)

class KeyDerivationError(WalletError):
    """Creative for HD wallet key issues."""
    def __init__(self, path: str):
        super().__init__(f"Failed deriving key at {path}", 45, {"derivation_path": path})

class NetworkError(WalletError):
    """Blockchain network related issues."""
    def __init__(self, endpoint: str, status: int = 0):
        super().__init__(f"Network issue at {endpoint}", 46, {"endpoint": endpoint, "status": status})

# Helper functions for common operations

def create_error_from_code(code: int, **kwargs) -> WalletError:
    """Unusual factory to instantiate exceptions by crypto error codes."""
    if code == 42:
        return InsufficientFunds(kwargs.get("current", 0), kwargs.get("needed", 0), kwargs.get("asset", "ETH"))
    elif code == 43:
        return InvalidWalletAddress(kwargs.get("address", ""), kwargs.get("network", "mainnet"))
    elif code == 44:
        return TransactionFailure(kwargs.get("reason", "unknown"), kwargs.get("tx_id"))
    elif code == 45:
        return KeyDerivationError(kwargs.get("path", "m/44'/60'/0'/0/0"))
    elif code == 46:
        return NetworkError(kwargs.get("endpoint", "unknown"), kwargs.get("status", 0))
    return WalletError("Generic wallet error", code)

def validate_and_raise(condition: bool, exc_class: type, *args, **kwargs):
    """Helper to check condition and raise specific crypto exception."""
    if not condition:
        raise exc_class(*args, **kwargs)

def serialize_exception(exc: Exception) -> dict:
    """Creative way to turn any exception into wallet dict format."""
    if isinstance(exc, WalletError):
        return exc.to_dict()
    return {"error": str(exc), "code": 999, "details": {}, "crypto_context": "wallet-utility-73"}