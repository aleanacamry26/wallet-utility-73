import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

def get_wallet_logger(name: str = 'wallet-utility-73', log_dir: str = 'logs') -> logging.Logger:
    path = Path(log_dir)
    path.mkdir(exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s'
        )
        
        # console stream for immediate feedback
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        
        # rotating file handler for crypto session persistence
        file_handler = RotatingFileHandler(
            path / 'wallet.log',
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger

# global singleton instance for quick access
logger = get_wallet_logger()