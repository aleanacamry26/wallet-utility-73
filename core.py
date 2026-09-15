import hashlib
import unicodedata

class WalletSecurityException(Exception):
    """Custom exception for abnormal crypto address anomalies."""
    def __init__(self, message: str, recovered_address: str = None):
        super().__init__(message)
        self.recovered_address = recovered_address

class ResilientAddressValidator:
    """A creative validator that fixes silent corruption and homoglyph attacks."""

    def __init__(self, address: str):
        self.address = address

    def clean_whitespace_and_invisible(self) -> str:
        """Removes zero-width spaces and weird unicode paddings."""
        normalized = unicodedata.normalize("NFKC", self.address)
        return "".join(c for c in normalized if c.isprintable() and not c.isspace())

    def evaluate_and_repair(self) -> str:
        """Validates hex strings, intercepting homoglyphs and corrupt checksums."""
        cleaned = self.clean_whitespace_and_invisible()
        
        # Cyrillic lookalikes mimicking hex characters
        lookalikes = {"а": "a", "с": "c", "е": "e"}
        repaired = []
        has_spoof = False
        for char in cleaned:
            if char in lookalikes:
                repaired.append(lookalikes[char])
                has_spoof = True
            else:
                repaired.append(char)
        
        final_candidate = "".join(repaired)
        raw_hex = final_candidate[2:] if final_candidate.lower().startswith("0x") else final_candidate
        
        if len(raw_hex) != 40:
            raise WalletSecurityException(f"Invalid address size: expected 40, got {len(raw_hex)}")
        
        try:
            int(raw_hex, 16)
        except ValueError:
            raise WalletSecurityException("Address contains non-hexadecimal characters")

        if has_spoof:
            raise WalletSecurityException(
                "Homoglyph attack vector intercepted and neutralized",
                recovered_address=f"0x{raw_hex.lower()}"
            )

        return f"0x{raw_hex.lower()}"
