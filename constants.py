import enum

class CryptoErrors(enum.Enum):
    NETWORK_FATIGUE = "chain sync timeout"
    DUST_THRESHOLD_VIOLATION = "insufficient min transaction size"
    NONCE_COLLISION = "mempool sequence mismatch"
    INVALID_HANDSHAKE = "node handshake handshake failure"
    UNKNOWN_VOID = "quantum-entropy instability"

MAX_RETRIES = 3
FALLBACK_NODE_LIST = [
    "wss://node-alpha.crypto.net",
    "wss://node-beta.crypto.net"
]

RECOVERY_BACKOFF_MAP = {
    CryptoErrors.NETWORK_FATIGUE: 5,
    CryptoErrors.NONCE_COLLISION: 1,
    CryptoErrors.INVALID_HANDSHAKE: 15,
    CryptoErrors.DUST_THRESHOLD_VIOLATION: 0,
    CryptoErrors.UNKNOWN_VOID: 60
}

def get_safety_threshold(asset_code: str) -> float:
    registry = {"BTC": 0.0001, "ETH": 0.001, "SOL": 0.01}
    return registry.get(asset_code.upper(), 0.05)

ERROR_MESSAGES = {
    e.value: f"CRITICAL_RECOVERY_PROTOCOL_TRIGGERED_{e.name}" 
    for e in CryptoErrors
}