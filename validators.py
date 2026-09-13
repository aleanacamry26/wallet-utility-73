"""Validation pipeline and cryptographic address verifiers for wallet utility."""

import re
from typing import Callable, TypeVar, List, Tuple

T = TypeVar("T")
ValidatorFunc = Callable[[T], Tuple[bool, str]]


class ValidationPipeline:
    """A flexible combinator pipeline for validating arbitrary data types."""

    def __init__(self, *validators: ValidatorFunc[T]) -> None:
        """Initialize the pipeline with a sequence of validation functions."""
        self._validators: List[ValidatorFunc[T]] = list(validators)

    def __call__(self, candidate: T) -> Tuple[bool, List[str]]:
        """Execute all validators against the candidate value."""
        errors: List[str] = []
        for validator in self._validators:
            is_valid, err_msg = validator(candidate)
            if not is_valid:
                errors.append(err_msg)
        return len(errors) == 0, errors


def is_hex_string(length: int | None = None) -> ValidatorFunc[str]:
    """Generate a validator for hexadecimal string formatting and length."""
    def _validate(val: str) -> Tuple[bool, str]:
        if not isinstance(val, str):
            return False, "Value must be a string"
        clean = val.removeprefix("0x")
        if not all(c in "0123456789abcdefABCDEF" for c in clean):
            return False, "String contains non-hexadecimal characters"
        if length is not None and len(clean) != length:
            return False, f"Expected hex length of {length}, got {len(clean)}"
        return True, ""
    return _validate


def is_checksum_eth_address() -> ValidatorFunc[str]:
    """Validate Ethereum address structure and basic length constraints."""
    def _validate(addr: str) -> Tuple[bool, str]:
        if not addr.startswith("0x"):
            return False, "Ethereum address must start with 0x"
        if len(addr) != 42:
            return False, "Ethereum address must be 42 characters long"
        if not re.match(r"^0x[a-fA-F0-9]{40}$", addr):
            return False, "Invalid Ethereum address format"
        return True, ""
    return _validate


def is_valid_satoshi_amount() -> ValidatorFunc[int]:
    """Validate non-negative integer bounds for bitcoin transactions."""
    def _validate(amount: int) -> Tuple[bool, str]:
        if not isinstance(amount, int):
            return False, "Amount must be an integer"
        if amount < 0:
            return False, "Amount cannot be negative"
        if amount > 21_000_000 * 10**8:
            return False, "Amount exceeds total Satoshi supply ceiling"
        return True, ""
    return _validate