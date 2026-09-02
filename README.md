# wallet-utility-73

wallet-utility-73 is a Python toolkit for cryptocurrency wallet generation and management. It helps developers create secure, hierarchical deterministic wallets and perform essential operations without depending on third-party services.

## Features

- Generate BIP-39 mnemonics with customizable entropy levels
- Derive addresses for Bitcoin and Ethereum using standard derivation paths
- Encrypt and store private keys in local AES-256 encrypted vaults
- Command-line interface for batch address generation and mnemonic validation

## Installation

```bash
git clone https://github.com/developer/wallet-utility-73.git
cd wallet-utility-73
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Usage

```python
from wallet_utility_73 import Wallet

# Generate new wallet
wallet = Wallet.generate(coin="eth")
print(wallet.address)

# Load from mnemonic
wallet = Wallet.from_mnemonic("your twelve word phrase here", coin="btc")
print(wallet.get_address())
```

## License

MIT License