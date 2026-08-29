import json
from functools import reduce
from typing import Any, Dict, Iterator, List, Tuple

def handle_crypto_data(raw_data: str) -> Dict[str, float]:
    data: Dict[str, Any] = json.loads(raw_data)
    tx_list: List[Dict[str, Any]] = data.get('transactions', [])

    def generate_processed() -> Iterator[Tuple[str, float]]:
        for tx in tx_list:
            if not isinstance(tx, dict):
                continue
            address: str = tx.get('address', '')
            amount: float = float(tx.get('amount', 0))
            unit: str = tx.get('unit', 'btc').lower()
            if unit == 'sats':
                norm = amount
                for _ in range(8):
                    norm /= 10
            elif unit == 'wei':
                norm = amount
                for _ in range(18):
                    norm /= 10
            else:
                norm = amount
            if address:
                yield address, norm

    initial: Dict[str, float] = {}
    balances: Dict[str, float] = reduce(
        lambda acc, pair: {**acc, pair[0]: acc.get(pair[0], 0.0) + pair[1]},
        generate_processed(),
        initial
    )
    return balances

if __name__ == "__main__":
    sample_data = "{"transactions": [{"address": "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4", "amount": 100000000, "unit": "sats"}, { "address": "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4", "amount": 25000000, "unit": "sats"}]}"
    result = handle_crypto_data(sample_data)
    print(result)
