from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Mapping

from cryptography.fernet import Fernet, InvalidToken
from flask import Response

from config import LabConfig, cookie_options
from security_utils import isoformat_utc


ENCRYPTED_COOKIE = "lab06_encrypted_profile"


@dataclass(frozen=True, slots=True)
class EncryptedProfile:
    user_id: int
    display_name: str
    preference: str
    issued_at: str


@dataclass(frozen=True, slots=True)
class EncryptionResult:
    valid: bool
    profile: EncryptedProfile | None
    encryption_status: str
    confidentiality_protected: bool
    integrity_protected: bool
    reason: str


def _key(config: LabConfig | Mapping[str, Any] | Any) -> bytes:
    if isinstance(config, LabConfig):
        return config.fernet_key
    value = config["FERNET_KEY"] if isinstance(config, Mapping) else getattr(config, "FERNET_KEY")
    return value if isinstance(value, bytes) else str(value).encode("ascii")


def create_fernet(config: LabConfig | Mapping[str, Any] | Any) -> Fernet:
    return Fernet(_key(config))


def demo_encrypted_profile(now: datetime) -> EncryptedProfile:
    return EncryptedProfile(
        user_id=10,
        display_name="Sinh viên Demo",
        preference="cookie-security-lab",
        issued_at=isoformat_utc(now),
    )


def encrypt_demo_profile(
    profile: EncryptedProfile, config: LabConfig | Mapping[str, Any] | Any
) -> str:
    plaintext = json.dumps(
        asdict(profile), ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return create_fernet(config).encrypt(plaintext).decode("ascii")


# LAB06-CODE:authenticated_decryption:START
def decrypt_demo_profile(
    token: str | None, config: LabConfig | Mapping[str, Any] | Any
) -> EncryptionResult:
    if not token:
        return EncryptionResult(False, None, "missing", True, True, "missing_cookie")
    try:
        # Fernet authenticates the token before returning plaintext.
        plaintext = create_fernet(config).decrypt(token.encode("ascii"))
        data = json.loads(plaintext.decode("utf-8"))
    except (InvalidToken, UnicodeEncodeError, UnicodeDecodeError, json.JSONDecodeError):
        return EncryptionResult(False, None, "invalid", True, True, "authenticated_decryption_failed")
    if not isinstance(data, dict) or set(data) != {
        "user_id", "display_name", "preference", "issued_at"
    }:
        return EncryptionResult(False, None, "valid", True, True, "invalid_payload_shape")
    if (
        not isinstance(data["user_id"], int)
        or isinstance(data["user_id"], bool)
        or data["user_id"] <= 0
        or not isinstance(data["display_name"], str)
        or not isinstance(data["preference"], str)
        or not isinstance(data["issued_at"], str)
    ):
        return EncryptionResult(False, None, "valid", True, True, "invalid_payload_values")
    profile = EncryptedProfile(
        user_id=data["user_id"],
        display_name=data["display_name"][:100],
        preference=data["preference"][:100],
        issued_at=data["issued_at"],
    )
    return EncryptionResult(True, profile, "valid", True, True, "authenticated_decryption_succeeded")
# LAB06-CODE:authenticated_decryption:END


def tamper_encrypted_token(token: str) -> str:
    if not token:
        return token
    index = max(1, len(token) // 2)
    replacement = "A" if token[index] != "A" else "B"
    return token[:index] + replacement + token[index + 1 :]


def issue_encrypted_demo_cookie(
    response: Response,
    token: str,
    config: LabConfig | Mapping[str, Any] | Any,
) -> None:
    response.set_cookie(ENCRYPTED_COOKIE, token, **cookie_options(config, httponly=True))


def expire_encrypted_demo_cookie(
    response: Response, config: LabConfig | Mapping[str, Any] | Any
) -> None:
    response.set_cookie(
        ENCRYPTED_COOKIE,
        "",
        expires=0,
        **cookie_options(config, httponly=True, max_age=0),
    )
