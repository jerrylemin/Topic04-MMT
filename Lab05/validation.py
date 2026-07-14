import re

from config import AUTH_LOGIC_INPUT, QUOTE_INPUT, SEARCH_EXPANDED_INPUT


class ValidationError(ValueError):
    pass


NORMAL_USERNAME = re.compile(r"^[A-Za-z0-9_]{1,64}$")


def normalize_spaces(value: str | None) -> str:
    return " ".join((value or "").strip().split())


def validate_username(value: str | None, *, vulnerable: bool = False) -> str:
    username = value or ""
    if vulnerable and username in {QUOTE_INPUT, AUTH_LOGIC_INPUT}:
        return username
    username = username.strip()
    if not username or len(username) > 64:
        raise ValidationError("Username length must be between 1 and 64 characters.")
    if vulnerable and not NORMAL_USERNAME.fullmatch(username):
        raise ValidationError("Username must contain only letters, numbers, or underscore (max 64).")
    return username


def validate_password(value: str | None) -> str:
    password = value or ""
    if not 1 <= len(password) <= 128:
        raise ValidationError("Password length must be between 1 and 128 characters.")
    return password


def validate_keyword(value: str | None, *, submitted: bool = True, vulnerable: bool = False) -> str:
    raw = value or ""
    if vulnerable and raw in {QUOTE_INPUT, SEARCH_EXPANDED_INPUT}:
        return raw
    keyword = normalize_spaces(raw)
    if submitted and not keyword:
        raise ValidationError("Search keyword is required.")
    if len(keyword) > 100:
        raise ValidationError("Search keyword cannot exceed 100 characters.")
    if vulnerable and any(marker in keyword for marker in ("'", '"', ";", "--", "/*", "*/")):
        raise ValidationError("Only the fixed local Lab05 scenarios may contain SQL syntax characters.")
    return keyword


def positive_int(value, field: str = "id") -> int:
    try:
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{field} must be a positive integer.") from exc
    if number <= 0:
        raise ValidationError(f"{field} must be a positive integer.")
    return number


def input_signals(value: str) -> dict:
    return {
        "length": len(value),
        "single_quote_detected": "'" in value,
        "comment_marker_detected": value in {AUTH_LOGIC_INPUT, SEARCH_EXPANDED_INPUT},
        "boolean_expression_detected": value == SEARCH_EXPANDED_INPUT,
        "trust_level": "untrusted",
    }
