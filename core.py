import re
from typing import Callable, Dict, Generator, Any

def validate_address(addr: str) -> bool:
    return bool(re.match(r'^(0x[a-fA-F0-9]{40}|[13][a-km-zA-HJ-NP-Z1-9]{25,34})$', addr))

def validate_amount(val: str) -> bool:
    try:
        return float(val) > 0
    except ValueError:
        return False

VALIDATION_RULES: Dict[str, Callable[[str], bool]] = {
    "address": validate_address,
    "amount": validate_amount,
}

def transaction_feed() -> Generator[Dict[str, Any], None, None]:
    payloads = [
        {"address": "0x71C7656EC7ab88b098defB751B7401B5f6d8976F", "amount": "1.5\