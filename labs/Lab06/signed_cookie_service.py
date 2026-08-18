from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Mapping

from flask import Response
from itsdangerous import BadData, URLSafeSerializer

from config import LabConfig, cookie_options
from database import UserRecord
from security_utils import isoformat_utc


SIGNED_COOKIE = "lab06_signed_profile"
SIGNED_PURPOSE = "lab06_signed_profile_demo"
_SALT = "lab06-signed-profile-v1"


@dataclass(frozen=True, slots=True)
class SignedProfile:
    user_id: int
    username: str
    role: str
    issued_at: str
    purpose: str = SIGNED_PURPOSE


@dataclass(frozen=True, slots=True)
class SignedVerificationResult:
    valid: bool
    payload: SignedProfile | None
    signature_status: str
    reason: str
    deserialization_executed: bool


def _value(config: LabConfig | Mapping[str, Any] | Any, name: str) -> Any:
    if isinstance(config, LabConfig):
        if name == "SIGNING_KEY":
            return config.signing_secret
        raise KeyError(name)
    if isinstance(config, Mapping):
        return config[name]
    return getattr(config, name)


def create_serializer(config: LabConfig | Mapping[str, Any] | Any) -> URLSafeSerializer:
    return URLSafeSerializer(
        secret_key=str(_value(config, "SIGNING_KEY")),
        salt=_SALT,
        signer_kwargs={"digest_method": hashlib.sha256},
    )


def sign_profile(
    user: UserRecord,
    config: LabConfig | Mapping[str, Any] | Any,
    issued_at: datetime,
) -> str:
    profile = SignedProfile(
        user_id=user.id,
        username=user.username,
        role=user.role,
        issued_at=isoformat_utc(issued_at),
    )
    return create_serializer(config).dumps(asdict(profile))


# LAB06-CODE:signed_verification:START
def verify_signed_profile(
    value: str | None, config: LabConfig | Mapping[str, Any] | Any
) -> SignedVerificationResult:
    if not value:
        return SignedVerificationResult(False, None, "missing", "missing_cookie", False)
    try:
        # itsdangerous verifies the signature before returning deserialized data.
        data = create_serializer(config).loads(value)
    except BadData:
        return SignedVerificationResult(False, None, "invalid", "signature_rejected", False)
    if not isinstance(data, dict) or set(data) != {
        "user_id", "username", "role", "issued_at", "purpose"
    }:
        return SignedVerificationResult(False, None, "valid", "invalid_payload_shape", True)
    if (
        not isinstance(data["user_id"], int)
        or isinstance(data["user_id"], bool)
        or data["user_id"] <= 0
        or not isinstance(data["username"], str)
        or not 1 <= len(data["username"]) <= 64
        or data["role"] not in {"user", "admin"}
        or not isinstance(data["issued_at"], str)
        or data["purpose"] != SIGNED_PURPOSE
    ):
        return SignedVerificationResult(False, None, "valid", "invalid_payload_values", True)
    profile = SignedProfile(
        user_id=data["user_id"],
        username=data["username"],
        role=data["role"],
        issued_at=data["issued_at"],
        purpose=data["purpose"],
    )
    return SignedVerificationResult(True, profile, "valid", "signature_verified", True)
# LAB06-CODE:signed_verification:END


verify_signed_cookie = verify_signed_profile


def issue_signed_cookie(
    response: Response,
    token: str,
    config: LabConfig | Mapping[str, Any] | Any,
) -> None:
    response.set_cookie(SIGNED_COOKIE, token, **cookie_options(config, httponly=True))


def expire_signed_cookie(
    response: Response, config: LabConfig | Mapping[str, Any] | Any
) -> None:
    response.set_cookie(
        SIGNED_COOKIE,
        "",
        expires=0,
        **cookie_options(config, httponly=True, max_age=0),
    )
