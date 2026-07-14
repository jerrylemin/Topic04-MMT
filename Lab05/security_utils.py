import hashlib
from collections.abc import Mapping


SENSITIVE_FIELDS = {
    "password", "password_hash", "legacy_password_digest", "digest", "cookie",
    "session", "secret", "secret_key",
}


def fingerprint(value: str | None) -> str:
    return hashlib.sha256((value or "").encode("utf-8")).hexdigest()[:12]


def mask_secret(value: str | None, visible: int = 4) -> str:
    if not value:
        return ""
    value = str(value)
    if len(value) <= visible * 2:
        return "***"
    return f"{value[:visible]}...{value[-visible:]}"


def redact(value):
    if isinstance(value, Mapping):
        return {
            str(key): ("[REDACTED]" if str(key).lower() in SENSITIVE_FIELDS else redact(item))
            for key, item in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [redact(item) for item in value]
    return value


def legacy_digest(password: str) -> str:
    """Intentionally weak local-lab digest; secure authentication never uses it."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def mask_query(sql: str, secrets=()) -> str:
    masked = sql
    for secret in secrets:
        if secret:
            masked = masked.replace(str(secret), "[REDACTED]")
    return masked


def password_metadata(value: str, *, secure: bool) -> dict:
    algorithm = value.split("$", 1)[0] if secure else "sha256"
    return {
        "algorithm": algorithm,
        "length": len(value),
        "fingerprint": fingerprint(value),
        "salted": secure,
    }

