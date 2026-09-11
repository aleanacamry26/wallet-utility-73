import hashlib

def generate_wallet_identicon(address: str) -> str:
    """Generates a deterministic ASCII art identicon for visual wallet verification.
    
    Helps users avoid clipboard-jacking attacks by recognizing their wallet's signature.
    """
    addr_bytes = address.lower().replace("0x", "").encode("utf-8")
    digest = hashlib.sha256(addr_bytes).digest()

    # 9x5 grid coordinates
    width, height = 9, 5
    x, y = width // 2, height // 2
    grid = [[0 for _ in range(width)] for _ in range(height)]

    # Walk the grid using entropy bits from the hash
    for byte in digest:
        for shift in range(0, 8, 2):
            direction = (byte >> shift) & 0x03
            # 0: Up-Left, 1: Up-Right, 2: Down-Left, 3: Down-Right
            dx = -1 if direction in (0, 2) else 1
            dy = -1 if direction in (0, 1) else 1

            x = max(0, min(width - 1, x + dx))
            y = max(0, min(height - 1, y + dy))
            grid[y][x] += 1

    symbols = " .:+*#@%$"
    num_symbols = len(symbols)
    
    border = "+" + "-" * width + "+"
    rows = [border]
    for r in grid:
        row_str = "".join(symbols[min(val, num_symbols - 1)] for val in r)
        rows.append(f"|{row_str}|")
    rows.append(border)

    return "\n".join(rows)

def format_crypto_amount(amount: float, decimals: int = 8) -> str:
    """Formats a crypto value safely without falling back to scientific notation."""
    formatted = f"{amount:.{decimals}f}"
    if "." in formatted:
        formatted = formatted.rstrip("0").rstrip(".")
    return formatted or "0"

def compare_addresses(addr1: str, addr2: str) -> bool:
    """Performs a case-insensitive, sanitized wallet address comparison."""
    return addr1.lower().strip() == addr2.lower().strip()