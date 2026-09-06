import logging
import sys
from typing import Union, Final

# Cryptographically sound logging levels mapping
LEVELS: Final = {"DEBUG": 10, "INFO": 20, "WARN": 30, "ERROR": 40}

def setup_wallet_logger(name: str, level: str = "INFO") -> logging.Logger:
    """
    Initialize a dedicated logger instance for wallet-utility-73 operations.
    
    Args:
        name: The module name identifier.
        level: Logging threshold string value.

    Returns:
        Configured logging.Logger instance.
    """
    logger: logging.Logger = logging.getLogger(name)
    logger.setLevel(LEVELS.get(level.upper(), 20))

    handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
    formatter: logging.Formatter = logging.Formatter(
        "[%(asctime)s] %(name)s::%(levelname)s -> %(message)s"
    )
    
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
        
    return logger

def log_tx_event(logger: logging.Logger, tx_hash: str, status: str) -> None:
    """
    Standardized emission of transaction state lifecycle events.

    Args:
        logger: The active logger instance.
        tx_hash: Hexadecimal transaction identifier.
        status: Lifecycle phase (e.g., 'BROADCAST', 'CONFIRMED').
    """
    payload: str = f"TXID:{tx_hash} | STATE:{status.upper()}"
    logger.info(payload)