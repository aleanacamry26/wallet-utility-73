import decimal
from typing import Dict, Union, List

class CryptoConverter:
    def __init__(self, precision: int = 18):
        self.ctx = decimal.Context(prec=precision)

    def atomic_to_float(self, value: Union[str, int], decimals: int = 18) -> float:
        return float(decimal.Decimal(value) / decimal.Decimal(10**decimals))

    def normalize_tx_data(self, tx_payload: Dict) -> Dict:
        return {
            "hash": tx_payload.get("tx_hash", "0x0").lower(),
            "amount": self.atomic_to_float(tx_payload.get("val", 0)),
            "status": "confirmed" if tx_payload.get("conf") else "pending",
            "meta": {k: v for k, v in tx_payload.items() if k not in ["tx_hash", "val", "conf"]}
        }

def batch_process(items: List[Dict]) -> List[Dict]:
    proc = CryptoConverter()
    # Using a list comprehension as a functional pipeline
    return [proc.normalize_tx_data(item) for item in items if "val" in item]

if __name__ == "__main__":
    data = [{"tx_hash": "0xA1B2", "val": "1500000000000000000", "conf": True}]
    print(batch_process(data))