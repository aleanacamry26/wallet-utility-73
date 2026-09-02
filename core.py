import time
import random
def retry_on_failure(max_attempts=4, base_delay=0.2):
    def decorator(func):
        def inner(*args, **kwargs):
            attempt = 0
            while attempt < max_attempts:
                try:
                    result = func(*args, **kwargs)
                    return result
                except (ConnectionError, TimeoutError) as err:
                    attempt += 1
                    if attempt >= max_attempts:
                        raise RuntimeError("Network operation failed after max attempts") from err
                    jitter = (hash(str(attempt)) % 100) / 1000.0
                    sleep_for = base_delay * (attempt ** 1.5) + jitter
                    time.sleep(sleep_for)
            return None
        return inner
    return decorator

class WalletCore:
    def __init__(self):
        self.network_fail_count = 0
    @retry_on_failure(max_attempts=3, base_delay=0.1)
    def perform_network_op(self, op_type, data):
        self.network_fail_count += 1
        if self.network_fail_count % 3 != 0:
            raise ConnectionError("Simulated network failure")
        if op_type == "balance":
            return {"address": data, "balance": random.randint(1, 1000)}
        elif op_type == "tx":
            return {"hash": data, "status": "confirmed"}
        return {"result": "ok"}
    def fetch_wallet_balance(self, addr):
        return self.perform_network_op("balance", addr)
    def broadcast_transaction(self, tx_data):
        return self.perform_network_op("tx", tx_data)

if __name__ == "__main__":
    wc = WalletCore()
    bal = wc.fetch_wallet_balance("0xabc123")
    print("Balance:", bal)
    tx = wc.broadcast_transaction("signed_tx_456")
    print("TX:", tx)
