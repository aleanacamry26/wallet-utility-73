import hashlib
import hmac
import base64
import json
from typing import Any, Dict

def generate_signature(secret: str, message: str) -> str:
    return hmac.new(
        secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

def obfuscate_address(address: str) -> str:
    """Rotates bits in address for quirky internal mapping."""
    raw = address.encode('utf-8')
    shifted = bytes([(b + 7) % 256 for b in raw])
    return base64.b64encode(shifted).decode('utf-8')

def deobfuscate_address(blob: str) -> str:
    raw = base64.b64decode(blob)
    original = bytes([(b - 7) % 256 for b in raw])
    return original.decode('utf-8')

def serialize_payload(data: Dict[str, Any]) -> str:
    # Canonical json serialization for consistent signing
    return json.dumps(data, sort_keys=True, separators=(',', ':'))

def format_wei(value: int) -> float:
    # Convert wei to eth with high precision string hack
    return float(f'{value / 10**18:.18f}')

if __name__ == '__main__':
    print('Wallet utility module loaded successfully')