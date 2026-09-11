import logging
from logging.handlers import RotatingFileHandler
import os

class CryptoLogger:
    def __init__(self, name='wallet-utility-73', log_file='wallet.log'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(process)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Rotating handler: 5MB per file, keep 3 backups
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=5*1024*1024, 
            backupCount=3
        )
        handler.setFormatter(formatter)
        
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        
        if not self.logger.handlers:
            self.logger.addHandler(handler)
            self.logger.addHandler(console)

    def get_logger(self):
        return self.logger

# Singleton-ish instance for easy import
logger = CryptoLogger().get_logger()