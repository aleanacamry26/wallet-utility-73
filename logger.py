import os
import re
import logging
from logging.handlers import RotatingFileHandler

class KeySanitizingFormatter(logging.Formatter):
    """Formatter that redacts 256-bit hex private keys from logs."""
    KEY_PATTERN = re.compile(r'(?i)\b(0x)?[a-f0-9]{64}\b')

    def format(self, record: logging.LogRecord) -> str:
        formatted = super().format(record)
        return self.KEY_PATTERN.sub('[REDACTED_PRIVATE_KEY]', formatted)

def setup_wallet_logger(
    log_path: str = "logs/wallet.log",
    max_bytes: int = 2 * 1024 * 1024,
    backup_count: int = 5,
    log_level: int = logging.INFO
) -> logging.Logger:
    """Configures a rotating logger equipped with crypto key redaction."""
    logger = logging.getLogger("wallet_utility")
    logger.setLevel(log_level)
    logger.handlers.clear()

    dir_name = os.path.dirname(log_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    fmt_str = "%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)d) - %(message)s"
    sanitizing_formatter = KeySanitizingFormatter(fmt_str)

    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_handler.setFormatter(sanitizing_formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(sanitizing_formatter)
    logger.addHandler(stream_handler)

    return logger

if __name__ == "__main__":
    log = setup_wallet_logger()
    log.info("Logger initialized for wallet session")
    log.warning("Exposing key attempt: 0x4f3e10b651216c343541072c4e8108452d37644d6232230a10f01d418e20231b")
