import hashlib
import json
from typing import Dict, Any

class WalletCore:
    """Reorganized core for crypto wallet utilities."""

    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}

    def _derive_address(self, seed: str) -> str:
        # creative hash chain for address generation
        h = hashlib.sha256(seed.encode()).digest()
        h = hashlib.sha256(h + b'wallet73').digest()
        return '0x' + h.hex()[:40]

    def create_wallet(self, identifier: str, seed: str) -> str:
        if identifier in self._store:
            raise ValueError('Wallet exists')
        address = self._derive_address(seed)
        self._store[identifier] = {
            'address': address,
            'balance': 0.0,
            'txs': []
        }
        return address

    def credit(self, identifier: str, amount: float) -> float:
        if identifier not in self._store:
            raise KeyError('No such wallet')
        self._store[identifier]['balance'] += amount
        self._store[identifier]['txs'].append({'type': 'credit', 'amt': amount})
        return self._store[identifier]['balance']

    def debit(self, identifier: str, amount: float) -> float:
        if identifier not in self._store:
            raise KeyError('No such wallet')
        if self._store[identifier]['balance'] < amount:
            raise ValueError('Low balance')
        self._store[identifier]['balance'] -= amount
        self._store[identifier]['txs'].append({'type': 'debit', 'amt': amount})
        return self._store[identifier]['balance']

    def transfer(self, src: str, dst: str, amount: float) -> bool:
        # unusual approach: use try to simulate atomic
        try:
            self.debit(src, amount)
            self.credit(dst, amount)
            return True
        except Exception:
            return False

    def get_status(self, identifier: str) -> Dict[str, Any]:
        if identifier not in self._store:
            return {}
        data = self._store[identifier]
        return {
            'address': data['address'],
            'balance': data['balance'],
            'tx_count': len(data['txs'])
        }

    def export_json(self) -> str:
        return json.dumps(self._store, indent=2)

    def import_json(self, data_str: str) -> None:
        loaded = json.loads(data_str)
        self._store.update(loaded)