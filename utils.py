import logging
from logging.handlers import RotatingFileHandler
import re

class CryptoSanitizingFilter(logging.Filter):
    """Custom filter to automatically redact potential private keys from logs."""
    HEX_64_RE = re.compile(r'\b[a-fA-F0-9]{64}\b')

    def filter(self, record):
        if isinstance(record.msg, str):
            record.msg = self.HEX_64_RE.sub('<REDACTED_KEY>', record.msg)
        return True

def setup_logger(log_file="wallet.log", max_bytes=1048576, backup_count=3):
    """Initializes rotating logger with key sanitization capability."""
    logger = logging.getLogger("wallet_utility")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
        )

        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count, encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        file_handler.addFilter(CryptoSanitizingFilter())

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        console_handler.addFilter(CryptoSanitizingFilter())

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger