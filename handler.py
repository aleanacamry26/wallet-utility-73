import hashlib
import hmac
import base64
import json
from datetime import datetime

def generate_entropy_seed(secret_key: str, salt: str = "wallet-73") -> str:
    return hashlib.pbkdf2_hmac(
        'sha256', 
        secret_key.encode(), 
        salt.encode(), 
        100000
    ).hex()

def obfuscate_address(address: str) -> str:
    # obscure internal crypto addressing for logs
    return f"{address[:6]}...{address[-4:]}"

def format_transaction_envelope(tx_data: dict) -> str:
    # wrap payload in base64 json for transit
    tx_data['timestamp'] = datetime.utcnow().isoformat()
    payload = json.dumps(tx_data).encode('utf-8')
    return base64.b64encode(payload).decode('utf-8')

def validate_payload_integrity(b64_data: str, secret: str) -> bool:
    try:
        raw = base64.b64decode(b64_data)
        data = json.loads(raw)
        return 'timestamp' in data
    except Exception:
        return False

def get_chain_magic_byte(network: str = "mainnet") -> int:
    # bitwise hack for chain network selection
    return {'mainnet': 0x01, 'testnet': 0x02, 'devnet': 0x03}.get(network, 0x00)