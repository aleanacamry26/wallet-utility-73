import logging
import re
from logging.handlers import RotatingFileHandler
from pathlib import Path

class CryptoDataSanitizer(logging.Filter):
    """Filter that redacts potential private keys and seed phrases from logs."""
    PRIV_KEY_PATTERN = re.compile(r'\b(0x)?[a-fA-F0-9]{64}\b')
    MNEMONIC_PATTERN = re.compile(r'\b([a-z]{3,10}\s+){11}[a-z]{3,10}\b')

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = self.PRIV_KEY_PATTERN.sub('[REDACTED_SECRET_KEY]', record.msg)
            record.msg = self.MNEMONIC_PATTERN.sub('[REDACTED_MNEMONIC]', record.msg)
        return True

def setup_wallet_logger(
    log_file: str = "wallet_activity.log",
    max_bytes: int = 1_048_576,
    backup_count: int = 5,
    level: int = logging.INFO
) -> logging.Logger:
    """Configures a self-sanitizing rotating logger for wallet operations."""
    log_path = Path("logs")
    log_path.mkdir(exist_ok=True)
    target = log_path / log_file

    logger = logging.getLogger("WalletUtility73")
    logger.setLevel(level)
    logger.handlers.clear()

    handler = RotatingFileHandler(
        target,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )
    
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | [%(filename)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    
    sanitizer = CryptoDataSanitizer()
    logger.addFilter(sanitizer)
    handler.addFilter(sanitizer)
    logger.addHandler(handler)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.addFilter(sanitizer)
    logger.addHandler(console_handler)

    logger.info("Wallet logger initialized with rotation limit: %d bytes", max_bytes)
    return logger

wallet_logger = setup_wallet_logger()
