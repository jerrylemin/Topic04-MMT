import hashlib
import re
from collections.abc import Mapping


SENSITIVE_FIELDS = {"password", "current_password", "new_password", "cookie", "csrf_token", "secret", "secret_key"}
SENSITIVE_DROP_FIELDS = {"password_hash"}
EMAIL_RE = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$")


class ValidationError(ValueError):
    pass


def mask_secret(value: str | None, visible: int = 4) -> str:
    if not value:
        return ""
    value = str(value)
    if len(value) <= visible * 2:
        return "***"
    return f"{value[:visible]}...{value[-visible:]}"


def fingerprint(value: str | None) -> str:
    return hashlib.sha256((value or "").encode()).hexdigest()[:12]


def redact(value):
    if isinstance(value, Mapping):
        return {
            str(key): ("[REDACTED]" if str(key).lower() in SENSITIVE_FIELDS else redact(item))
            for key, item in value.items()
            if str(key).lower() not in SENSITIVE_DROP_FIELDS
        }
    if isinstance(value, (list, tuple)):
        return [redact(item) for item in value]
    return value


def validate_email(value: str | None) -> str:
    email = (value or "").strip()
    if not email or len(email) > 254 or not EMAIL_RE.fullmatch(email):
        raise ValidationError("Email không hợp lệ.")
    return email


def validate_new_password(value: str | None) -> str:
    password = value or ""
    if len(password) < 10 or len(password) > 128:
        raise ValidationError("Mật khẩu phải dài từ 10 đến 128 ký tự.")
    if not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password) or not re.search(r"\d", password):
        raise ValidationError("Mật khẩu phải có chữ hoa, chữ thường và chữ số.")
    return password


def positive_int(value, field: str, maximum: int = 1_000_000_000) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{field} phải là số nguyên.") from exc
    if number <= 0 or number > maximum:
        raise ValidationError(f"{field} nằm ngoài giới hạn cho phép.")
    return number
