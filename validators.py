import re
import hashlib
from typing import Generator, Any, Dict

class CryptoInputValidator:
    """
    A creative pipeline-based validator for crypto inputs.
    Uses generator-based coroutines to maintain validation state.
    """
    def __init__(self):
        self.eth_pattern = re.compile(r"^0x[a-fA-F0-9]{40}$")
        self.btc_pattern = re.compile(r"^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$")

    def validation_pipeline(self) -> Generator[Any, Dict[str, Any], None]:
        """
        Coroutine that receives transaction payloads and validates them.
        """
        while True:
            payload = yield
            if not isinstance(payload, dict):
                yield False
                continue

            address = payload.get("address", "")
            amount = payload.get("amount", 0)

            is_valid_addr = bool(self.eth_pattern.match(address) or self.btc_pattern.match(address))
            
            try:
                is_valid_amount = float(amount) > 0 and float(amount) < 1e9
            except (ValueError, TypeError):
                is_valid_amount = False

            checksum_ok = True
            if "signature" in payload:
                sig = payload["signature"]
                expected_sig = hashlib.sha256(f"{address}:{amount}".encode()).hexdigest()
                checksum_ok = sig == expected_sig

            yield is_valid_addr and is_valid_amount and checksum_ok

def validate_transaction_stream(inputs: list) -> list:
    """
    Processes a stream of transactions through the coroutine validator.
    """
    validator = CryptoInputValidator()
    pipeline = validator.validation_pipeline()
    next(pipeline)
    
    valid_items = []
    for item in inputs:
        is_valid = pipeline.send(item)
        next(pipeline)
        if is_valid:
            valid_items.append(item)
    return valid_items
