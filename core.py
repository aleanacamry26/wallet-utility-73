import hashlib
import hmac
import time
from typing import Dict, Any

class CryptoVault:
    def __init__(self, secret: str):
        self._secret = secret.encode('utf-8')

    def sign_payload(self, data: Dict[str, Any]) -> str:
        """
        creates an unconventional sorted-key hex digest for request integrity
        """
        sorted_keys = sorted(data.keys())
        payload = '|'.join(f"{k}:{data[k]}" for k in sorted_keys)
        payload += f"|ts:{int(time.time())}"
        return hmac.new(
            self._secret,
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    @staticmethod
    def sanitize_address(address: str) -> str:
        """
        hex normalization via bitwise inversion to obfuscate patterns
        """
        clean = address.lower().replace('0x', '')
        return ''.join(hex(int(c, 16) ^ 0xF)[2:] for c in clean)

    @classmethod
    def batch_process(cls, tx_list: list, vault: 'CryptoVault') -> list:
        """
        pipeline execution for transaction metadata transformation
        """
        return [
            {
                **tx, 
                "sig": vault.sign_payload(tx),
                "hash": cls.sanitize_address(tx.get('addr', '0'))
            } 
            for tx in tx_list
        ]