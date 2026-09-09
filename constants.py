from dataclasses import dataclass
from typing import Final, Dict

@dataclass(frozen=True)
class ChainConfig:
    name: str
    symbol: str
    decimals: int
    rpc_url: str

CHAINS: Final[Dict[str, ChainConfig]] = {
    'ETH': ChainConfig('Ethereum', 'ETH', 18, 'https://eth.llamarpc.com'),
    'BSC': ChainConfig('BNB Chain', 'BNB', 18, 'https://bsc-dataseed.binance.org'),
    'MATIC': ChainConfig('Polygon', 'MATIC', 18, 'https://polygon-rpc.com'),
    'ARB': ChainConfig('Arbitrum', 'ETH', 18, 'https://arb1.arbitrum.io/rpc')
}

PRECISION_LIMIT: Final[int] = 8
WEI_CONVERSION: Final[int] = 10**18

def get_chain(symbol: str) -> ChainConfig:
    try:
        return CHAINS[symbol.upper()]
    except KeyError:
        raise ValueError(f'Unsupported network identifier: {symbol}')

def format_wei(value: int, decimals: int = 18) -> float:
    return float(value) / (10**decimals)

class HexConverter:
    @staticmethod
    def to_int(hex_val: str) -> int:
        return int(hex_val, 16)
    
    @staticmethod
    def from_int(val: int) -> str:
        return hex(val)

CRYPTO_MAPPING = {
    '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee': 'NATIVE',
    '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c': 'WBNB'
}