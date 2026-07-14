import re


EMAIL_RE = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$")


class ValidationError(ValueError):
    pass


def integer(value, name: str, minimum: int = 1, maximum: int | None = None) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{name} phải là số nguyên.") from exc
    if parsed < minimum or maximum is not None and parsed > maximum:
        upper = f" đến {maximum}" if maximum is not None else " trở lên"
        raise ValidationError(f"{name} phải trong phạm vi {minimum}{upper}.")
    return parsed


def email(value: str) -> str:
    normalized = (value or "").strip()
    if len(normalized) > 254 or not EMAIL_RE.fullmatch(normalized):
        raise ValidationError("Email không hợp lệ.")
    return normalized


def role(value: str) -> str:
    if value not in {"user", "admin"}:
        raise ValidationError("Role không hợp lệ.")
    return value

