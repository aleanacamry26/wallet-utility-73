import hashlib

class EdgeCaseHandler:
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    def handle(self, exc: Exception, context: dict) -> dict:
        if self.next_handler:
            return self.next_handler.handle(exc, context)
        return {"status": "unhandled", "message": str(exc)}

class NegativeAmountHandler(EdgeCaseHandler):
    def handle(self, exc: Exception, context: dict) -> dict:
        if isinstance(exc, ValueError) and context.get("amount", 0) < 0:
            return {"status": "error", "message": "negative amounts not permitted for wallet transfers"}
        return super().handle(exc, context)

class InsufficientBalanceHandler(EdgeCaseHandler):
    def handle(self, exc: Exception, context: dict) -> dict:
        if context.get("balance", 0) < context.get("amount", 0):
            return {"status": "error", "message": "insufficient balance for crypto transaction"}
        if "insufficient" in str(exc).lower():
            return {"status": "error", "message": "insufficient balance for crypto transaction"}
        return super().handle(exc, context)

class InvalidAddressHandler(EdgeCaseHandler):
    def handle(self, exc: Exception, context: dict) -> dict:
        addr = context.get("address", "")
        if not addr or len(addr) < 10 or not addr.startswith("0x"):
            return {"status": "error", "message": "invalid wallet address edge case"}
        return super().handle(exc, context)

def create_error_chain() -> EdgeCaseHandler:
    return NegativeAmountHandler(
        InsufficientBalanceHandler(
            InvalidAddressHandler()
        )
    )

def process_wallet_transfer(wallet: dict, amount: float, to_address: str) -> dict:
    context = {
        "amount": amount,
        "balance": wallet.get("balance", 0),
        "address": to_address
    }
    try:
        if amount <= 0:
            raise ValueError("amount must be positive")
        if wallet.get("balance", 0) < amount:
            raise RuntimeError("insufficient funds detected")
        if not to_address.startswith("0x"):
            raise ValueError("bad address")
        tx_hash = hashlib.sha256(f"{wallet}{amount}{to_address}".encode()).hexdigest()
        wallet["balance"] -= amount
        return {"status": "success", "tx_hash": tx_hash, "remaining": wallet["balance"]}
    except Exception as e:
        handler = create_error_chain()
        return handler.handle(e, context)

def main():
    my_wallet = {"balance": 250.5, "id": "user73"}
    result1 = process_wallet_transfer(my_wallet, 100, "0x742d35Cc6634C0532925a3b844Bc454e4438f44e")
    print(result1)
    result2 = process_wallet_transfer(my_wallet, -5, "0x742d35Cc6634C0532925a3b844Bc454e4438f44e")
    print(result2)
    result3 = process_wallet_transfer(my_wallet, 200, "shortaddr")
    print(result3)
    result4 = process_wallet_transfer(my_wallet, 300, "0x742d35Cc6634C0532925a3b844Bc454e4438f44e")
    print(result4)

if __name__ == "__main__":
    main()