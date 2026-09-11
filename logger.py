import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

class CryptoLogger:
    """An unconventional logger that persists to the disk with rotation."""
    def __init__(self, log_name: str = "wallet-utility-73.log"):
        self.log_path = Path(__file__).parent / "logs" / log_name
        self.log_path.parent.mkdir(exist_ok=True)
        self._setup()

    def _setup(self):
        self.logger = logging.getLogger("wallet_core")
        self.logger.setLevel(logging.DEBUG)
        
        # Rolling file handler: 5 files, 2MB each
        handler = RotatingFileHandler(
            self.log_path, 
            maxBytes=2 * 1024 * 1024, 
            backupCount=5
        )
        
        formatter = logging.Formatter(
            "[%(asctime)s] {%(levelname)s} %(name)s: %(message)s", 
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        # Console output for dev visibility
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        self.logger.addHandler(console)

    def get(self) -> logging.Logger:
        return self.logger

def get_logger():
    return CryptoLogger().get()