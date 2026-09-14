import sys
import datetime
from typing import Any

class WalletLogger:
    """Colorful terminal output for crypto operations."""
    COLORS = {
        "info": "\033[94m",
        "success": "\033[92m",
        "warning": "\033[93m",
        "error": "\033[91m",
        "reset": "\033[0m"
    }

    @staticmethod
    def _log(level: str, message: str) -> None:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        color = WalletLogger.COLORS.get(level, "")
        reset = WalletLogger.COLORS["reset"]
        print(f"{timestamp} [{color}{level.upper()}{reset}] {message}", file=sys.stderr)

    @classmethod
    def info(cls, msg: Any) -> None:
        cls._log("info", str(msg))

    @classmethod
    def success(cls, msg: Any) -> None:
        cls._log("success", str(msg))

    @classmethod
    def warn(cls, msg: Any) -> None:
        cls._log("warning", str(msg))

    @classmethod
    def fail(cls, msg: Any) -> None:
        cls._log("error", str(msg))

def log_execution(func):
    """Decorator for tracking function lifecycle events."""
    def wrapper(*args, **kwargs):
        WalletLogger.info(f"executing {func.__name__}...")
        try:
            result = func(*args, **kwargs)
            WalletLogger.success(f"{func.__name__} completed successfully")
            return result
        except Exception as e:
            WalletLogger.fail(f"{func.__name__} failed: {str(e)}")
            raise
    return wrapper