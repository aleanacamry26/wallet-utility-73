import hashlib
import time
from typing import Any, Dict, Optional, Type


class CryptoWalletException(Exception):
    """Base exception with auto-generated error signature and RPC payload capability."""

    code: int = -32000

    def __init__(self, message: str, payload: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.payload = payload or {}
        self.timestamp = time.time()
        self.signature = self._generate_signature()

    def _generate_signature(self) -> str:
        raw = f"{self.__class__.__name__}:{self.message}:{self.timestamp}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]

    def to_rpc_error(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            "data": {
                "sig": self.signature,
                "ts": int(self.timestamp),
                **self.payload,
            },
        }

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} [{self.signature}]: {self.message}>"


class InsufficientFundsError(CryptoWalletException):
    code = -32001


class InvalidAddressChecksumError(CryptoWalletException):
    code = -32002


class NonceCollisionException(CryptoWalletException):
    code = -32003


class KeyDerivationFailure(CryptoWalletException):
    code = -32004


def get_exception_by_code(code: int) -> Type[CryptoWalletException]:
    registry = {cls.code: cls for cls in CryptoWalletException.__subclasses__()}
    return registry.get(code, CryptoWalletException)
