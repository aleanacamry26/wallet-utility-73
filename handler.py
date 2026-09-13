from typing import Dict, Any, Union, List
from decimal import Decimal

class TransactionHandler:
    """Handles cryptographic transaction payload serialization and validation."""

    def __init__(self, chain_id: int = 1) -> None:
        self.chain_id: int = chain_id
        self.buffer: List[Dict[str, Any]] = []

    def serialize_asset(self, amount: Union[int, float, str, Decimal]) -> str:
        """Converts various numeric inputs into standard Wei-like string format."""
        if isinstance(amount, str):
            return amount
        return str(int(Decimal(str(amount)) * (10 ** 18)))

    def process_batch(self, payloads: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregates crypto payloads and injects chain metadata."""
        processed: Dict[str, Any] = {
            "chain": self.chain_id,
            "txs": [],
            "status": "pending"
        }
        
        for item in payloads:
            item['value'] = self.serialize_asset(item.get('value', 0))
            processed['txs'].append(item)
            
        self.buffer.extend(processed['txs'])
        return processed

    def flush(self) -> int:
        """Clears local transaction buffer and returns count."""
        count: int = len(self.buffer)
        self.buffer.clear()
        return count