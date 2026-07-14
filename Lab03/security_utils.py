from collections.abc import Mapping


SENSITIVE_NAMES = {"password", "password_hash", "cookie", "secret", "secret_key", "session"}


def mask_cookie(value: str) -> str:
    if not value:
        return "(không có)"
    return "; ".join(f"{part.split('=', 1)[0]}=***" for part in value.split("; "))


def safe_value(name: str, value) -> str:
    lowered = name.lower()
    if any(word in lowered for word in SENSITIVE_NAMES):
        return "[REDACTED]"
    text = str(value if value is not None else "")
    return text if len(text) <= 240 else text[:240] + "…"


def safe_mapping(values: Mapping) -> dict:
    return {str(key): safe_value(str(key), value) for key, value in values.items()}

