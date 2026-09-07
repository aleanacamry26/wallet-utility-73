import re
from typing import Dict, Any, Generator, List

class TransactionValidationError(Exception):
    """Raised when a raw transaction payload fails validation rules."""
    pass

def is_hex_hash(val: str) -> bool:
    return isinstance(val, str) and bool(re.match(r'^[a-fA-F0-9]{64}$', val))

def is_valid_address(addr: str) -> bool:
    return isinstance(addr, str) and bool(re.match(r'^(0x[a-fA-F0-9]{40}|(1|3|bc1)[a-zA-zA-HJ-NP-Z0-9]{25,62})$', addr))

def validate_payload(tx_data: Dict[str, Any]) -> Dict[str, Any]:
    rules = {
        "tx_hash": is_hex_hash,
        "sender": is_valid_address,
        "recipient": is_valid_address,
        "amount_sats": lambda v: isinstance(v, int) and v > 0,
    }
    for field, check in rules.items():
        if field not in tx_data:
            raise TransactionValidationError(f"Missing field: {field}")
        if not check(tx_data[field]):
            raise TransactionValidationError(f"Validation failed for field: {field}")
    return tx_data

def process_incoming_queue(raw_queue: List[Dict[str, Any]]) -> Generator[Dict[str, Any], None, None]:
    for entry in raw_queue:
        try:
            clean_tx = validate_payload(entry)
            clean_tx["processed"] = True
            yield clean_tx
        except TransactionValidationError as exc:
            yield {"raw": entry, "processed": False, "error": str(exc)}
