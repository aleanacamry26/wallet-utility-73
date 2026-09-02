import logging
from logging.handlers import RotatingFileHandler
import os
import sys

class CryptoContextFilter(logging.Filter):
    def filter(self, record):
        record.context = 'crypto-wallet-73'
        record.nonce = abs(hash(str(record.msg))) % 100000
        return True

def setup_logger(name='wallet_utility_73'):
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger
    logger.setLevel(logging.DEBUG)
    if not os.path.isdir('logs'):
        os.makedirs('logs')
    log_path = os.path.join('logs', 'wallet.log')
    rotating_handler = RotatingFileHandler(
        log_path, maxBytes=10485760, backupCount=3, encoding='utf-8'
    )
    rotating_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s [%(context)s] [%(nonce)d] %(levelname)s: %(message)s'
    )
    rotating_handler.setFormatter(file_format)
    crypto_filter = CryptoContextFilter()
    rotating_handler.addFilter(crypto_filter)
    logger.addHandler(rotating_handler)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_format = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    )
    stream_handler.setFormatter(stream_format)
    logger.addHandler(stream_handler)
    logger.info('Logger initialized with rotation')
    return logger