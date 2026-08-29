class BaseWalletException(Exception):
    error_code = 0
    def __init__(self, message, **kwargs):
        super().__init__(message)
        self.message = message
        self.details = kwargs
    def __str__(self):
        return f"[{self.error_code}] {self.message}"
    def to_dict(self):
        return {"code": self.error_code, "message": self.message, "details": self.details}

class InvalidAddressError(BaseWalletException):
    error_code = 4001
    def __init__(self, address, **kwargs):
        super().__init__(f"Invalid address provided: {address}", address=address, **kwargs)

class InsufficientFundsError(BaseWalletException):
    error_code = 4002
    def __init__(self, required, available, **kwargs):
        super().__init__(f"Insufficient funds: need {required} have {available}", required=required, available=available, **kwargs)

class CryptoKeyError(BaseWalletException):
    error_code = 4003
    def __init__(self, key_type, issue, **kwargs):
        super().__init__(f"Key error for {key_type}: {issue}", key_type=key_type, issue=issue, **kwargs)

class TransactionFailureError(BaseWalletException):
    error_code = 4004
    def __init__(self, reason, tx_id=None, **kwargs):
        msg = f"Transaction failed: {reason}"
        if tx_id:
            msg += f" (tx: {tx_id})"
        super().__init__(msg, reason=reason, tx_id=tx_id, **kwargs)

class BlockchainConnectionError(BaseWalletException):
    error_code = 5001
    def __init__(self, chain, endpoint, **kwargs):
        super().__init__(f"Failed to connect to {chain} at {endpoint}", chain=chain, endpoint=endpoint, **kwargs)

EXCEPTION_MAP = {
    4001: InvalidAddressError,
    4002: InsufficientFundsError,
    4003: CryptoKeyError,
    4004: TransactionFailureError,
    5001: BlockchainConnectionError,
}

def create_exception(code, *args, **kwargs):
    exc_cls = EXCEPTION_MAP.get(code, BaseWalletException)
    return exc_cls(*args, **kwargs)