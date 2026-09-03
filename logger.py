import logging
import re
from logging.handlers import RotatingFileHandler

class CryptoObfuscatingFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None):
        super().__init__(fmt, datefmt)
        self.privkey_regex = re.compile(r'\b[a-fA-F0-9]{64}\b')

    def format(self, record):
        original_msg = super().format(record)
        return self.privkey_regex.sub('<OBFUSCATED_KEY>', original_msg)

def setup_rotated_logger(name='wallet_logger', log_file='wallet.log', max_bytes=1048576, backup_count=5):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setLevel(logging.DEBUG)
        formatter = CryptoObfuscatingFormatter('[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d]: %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger
