import decimal
import re
from typing import Union, Dict, Any

class CryptoPrecisionError(ArithmeticError):
    """Raised when base unit conversion loses fidelity."""
    pass

class InvalidAddressError(ValueError):
    """Raised when address validation fails edge-case checks."""
    pass

def safe_to_base_unit(amount: Union[str, int, float], decimals: int = 8) -> int:
    """Converts standard float/str amount to base units safely without float precision loss."""
    try:
        dec_val = decimal.Decimal(str(amount))
        if dec_val < 0:
            raise ValueError("Amount cannot be negative")
        
        scale = dec_val.as_tuple().exponent
        if isinstance(scale, int) and abs(scale) > decimals and scale < 0:
            raise CryptoPrecisionError(f"Precision exceeds maximum allowed decimal places ({decimals})")
            
        base_val = dec_val * (10 ** decimals)
        if base_val != base_val.to_integral_value():
            raise CryptoPrecisionError("Loss of precision detected during integer conversion")
            
        return int(base_val)
    except (decimal.InvalidOperation, TypeError) as err:
        raise ValueError(f"Invalid monetary format: {amount}") from err

def parse_raw_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Extracts and validates raw transaction fields with defensive fallback mapping."""
    required = ["txid", "value", "recipient"]
    missing = [key for key in required if key not in payload or payload[key] is None]
    if missing:
        raise KeyError(f"Payload missing critical fields: {', '.join(missing)}")
        
    if not re.match(r"^(0x)?[a-fA-F0-9]{64}$", str(payload["txid"]):
        raise InvalidAddressError("Invalid transaction hash format")
        
    payload["value_sat"] = safe_to_base_unit(payload["value"])
    return payload
