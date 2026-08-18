from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Mapping


LOGIN_MODES = frozenset({"plain", "base64", "signed", "session"})
_USERNAME = re.compile(r"^[A-Za-z0-9_]{1,64}$")
_TRACE_ID = re.compile(r"^trace_[a-f0-9]{24}$")


class ValidationError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class LoginInput:
    username: str
    password: str
    mode: str


def validate_username(value: object) -> str:
    username = str(value or "").strip()
    if not _USERNAME.fullmatch(username):
        raise ValidationError("Invalid username")
    return username


def validate_password(value: object) -> str:
    password = str(value or "")
    if not 1 <= len(password) <= 256 or "\x00" in password:
        raise ValidationError("Invalid password")
    return password


def validate_mode(value: object) -> str:
    mode = str(value or "").strip().lower()
    if mode not in LOGIN_MODES:
        raise ValidationError("Unsupported fixed lab mode")
    return mode


def validate_login_input(form: Mapping[str, object]) -> LoginInput:
    return LoginInput(
        username=validate_username(form.get("username")),
        password=validate_password(form.get("password")),
        mode=validate_mode(form.get("mode")),
    )


def validate_trace_id(value: object) -> str:
    trace_id = str(value or "")
    if not _TRACE_ID.fullmatch(trace_id):
        raise ValidationError("Invalid trace identifier")
    return trace_id
