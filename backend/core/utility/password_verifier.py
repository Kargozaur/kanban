import re


def verify_password(value: str) -> str:
    if not re.search(r"[A-Z]", value):
        raise ValueError("password.uppercase_required")
    if not re.search(r"\d", value):
        raise ValueError("password.number_required")
    if not re.search(r"[!@#$%^&*(),.:<>|?]", value):
        raise ValueError("password.specialsymbol_required")
    if len(value) < 8:
        raise ValueError("password.length_8_symbols_required")
    return value
