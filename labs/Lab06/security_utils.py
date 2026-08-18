from __future__ import annotations

import hashlib
import json
import secrets
from datetime import datetime, timezone
from typing import Any, Mapping


_SENSITIVE_EXACT = {
    "password", "password_hash", "secret", "secret_key", "signing_key",
    "fernet_key", "raw_token", "session_id", "session_token_hash",
    "cookie_value", "full_cookie", "full_signature",
}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def isoformat_utc(value: datetime | None = None) -> str:
    current = utc_now() if value is None else value
    if current.tzinfo is None:
        current = current.replace(tzinfo=timezone.utc)
    return current.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def generate_trace_id() -> str:
    return f"trace_{secrets.token_hex(12)}"


def fingerprint(value: str | bytes, *, length: int = 12) -> str:
    raw = value.encode("utf-8") if isinstance(value, str) else value
    return hashlib.sha256(raw).hexdigest()[:length]


def mask_value(value: str | None, *, visible: int = 4) -> str | None:
    if value is None:
        return None
    if len(value) <= visible * 2:
        return "*" * len(value)
    return f"{value[:visible]}…{value[-visible:]}"


def is_sensitive_field(name: str) -> bool:
    lowered = name.strip().lower()
    return lowered in _SENSITIVE_EXACT or lowered.endswith("_password") or lowered.endswith("_raw_token")


def redact(value: Any, *, field_name: str = "") -> Any:
    if is_sensitive_field(field_name):
        return "[REDACTED]"
    if isinstance(value, Mapping):
        return {str(key): redact(item, field_name=str(key)) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [redact(item) for item in value]
    if isinstance(value, datetime):
        return isoformat_utc(value)
    return value


def safe_json_dumps(value: Any, *, indent: int | None = 2) -> str:
    return json.dumps(redact(value), ensure_ascii=False, indent=indent, sort_keys=True)


def bounded_text(value: object | None, *, limit: int = 500) -> str | None:
    if value is None:
        return None
    text = str(value).replace("\x00", "")
    return text[:limit]
