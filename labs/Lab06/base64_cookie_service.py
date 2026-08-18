from __future__ import annotations

import base64
import binascii
import json
from dataclasses import asdict, dataclass
from typing import Any, Mapping

from flask import Response

from config import cookie_options


BASE64_COOKIE = "lab06_profile_b64"
MAX_COOKIE_LENGTH = 2048


@dataclass(frozen=True, slots=True)
class Base64Profile:
    username: str
    role: str


@dataclass(frozen=True, slots=True)
class Base64DecodeResult:
    valid: bool
    profile: Base64Profile | None
    decoded_json: str | None
    reason: str


def original_demo_profile() -> Base64Profile:
    return Base64Profile(username="student", role="user")


def modified_demo_profile() -> Base64Profile:
    return Base64Profile(username="student", role="admin")


def encode_profile(profile: Base64Profile) -> str:
    payload = json.dumps(
        asdict(profile), ensure_ascii=False, separators=(",", ":"), sort_keys=False
    ).encode("utf-8")
    return base64.urlsafe_b64encode(payload).decode("ascii")


def decode_profile(value: str | None) -> Base64DecodeResult:
    if not value:
        return Base64DecodeResult(False, None, None, "missing_cookie")
    if len(value) > MAX_COOKIE_LENGTH:
        return Base64DecodeResult(False, None, None, "cookie_too_large")
    try:
        decoded_bytes = base64.b64decode(
            value.encode("ascii"), altchars=b"-_", validate=True
        )
        decoded = decoded_bytes.decode("utf-8")
        data = json.loads(decoded)
    except (UnicodeEncodeError, UnicodeDecodeError, binascii.Error, json.JSONDecodeError):
        return Base64DecodeResult(False, None, None, "invalid_base64_or_json")
    if not isinstance(data, dict) or set(data) != {"username", "role"}:
        return Base64DecodeResult(False, None, decoded, "invalid_payload_shape")
    if not isinstance(data["username"], str) or not isinstance(data["role"], str):
        return Base64DecodeResult(False, None, decoded, "invalid_payload_types")
    if len(data["username"]) > 64 or data["role"] not in {"user", "admin"}:
        return Base64DecodeResult(False, None, decoded, "invalid_payload_values")
    return Base64DecodeResult(
        True,
        Base64Profile(username=data["username"], role=data["role"]),
        decoded,
        "decoded_without_integrity_check",
    )


def issue_base64_demo_cookie(
    response: Response,
    config: Mapping[str, Any] | Any,
    profile: Base64Profile,
) -> None:
    response.set_cookie(
        BASE64_COOKIE,
        encode_profile(profile),
        **cookie_options(config, httponly=False),
    )


def expire_base64_cookie(response: Response, config: Mapping[str, Any] | Any) -> None:
    response.delete_cookie(
        BASE64_COOKIE,
        path="/",
        secure=bool(config["COOKIE_SECURE"]),
        httponly=False,
        samesite="Lax",
    )


# LAB06-CODE:base64_authorization:START
def authorize_decoded_role(result: Base64DecodeResult) -> bool:
    return bool(result.valid and result.profile and result.profile.role == "admin")
# LAB06-CODE:base64_authorization:END

