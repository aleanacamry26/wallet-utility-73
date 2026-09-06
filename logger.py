import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

def get_wallet_logger(name: str = 'wallet-utility-73') -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if logger.handlers:
        return logger

    log_path = Path('logs')
    log_path.mkdir(exist_ok=True)
    
    # rotating handler with 5mb limit, keeping 3 backups
    handler = RotatingFileHandler(
        filename=log_path / f'{name}.log',
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding='utf-8'
    )
    
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s'
    )
    handler.setFormatter(formatter)
    
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    
    logger.addHandler(handler)
    logger.addHandler(console)
    
    # prevent log propagation to root logger
    logger.propagate = False
    
    return logger