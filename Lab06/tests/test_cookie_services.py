from __future__ import annotations

import base64
import json
from datetime import UTC, datetime

import pytest
from flask import Response, request

from base64_cookie_service import (
    Base64Profile,
    decode_profile,
    encode_profile,
    modified_demo_profile,
    original_demo_profile,
)
from cookie_service import (
    PLAIN_ROLE_COOKIE,
    PLAIN_USERNAME_COOKIE,
    expire_plain_demo_cookies,
    issue_plain_demo_cookies,
    read_plain_identity,
)
from database import connect_database, get_user_by_id
from encrypted_cookie_service import (
    ENCRYPTED_COOKIE,
    decrypt_demo_profile,
    expire_encrypted_demo_cookie,
)
from seed import seed_database
from signed_cookie_service import (
    SIGNED_COOKIE,
    create_serializer,
    expire_signed_cookie,
    sign_profile,
    verify_signed_profile,
)


def _b64_json(value):
    raw = json.dumps(value, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii")


def test_plain_service_issues_only_fixed_demo_values(app):
    response = Response()
    issue_plain_demo_cookies(response, app.config)
    cookies = response.headers.getlist("Set-Cookie")
    assert any(item.startswith(f"{PLAIN_USERNAME_COOKIE}=student") for item in cookies)
    assert any(item.startswith(f"{PLAIN_ROLE_COOKIE}=user") for item in cookies)


def test_plain_service_reads_cookie_presence_from_request(app):
    with app.test_request_context(headers={"Cookie": "lab06_username=student; lab06_role=user"}):
        identity = read_plain_identity(request)
    assert identity.username == "student" and identity.role == "user"
    assert identity.username_present and identity.role_present


def test_plain_service_reports_missing_cookie_without_defaults(app):
    with app.test_request_context():
        identity = read_plain_identity(request)
    assert identity.username is None and identity.role is None
    assert not identity.username_present and not identity.role_present


def test_plain_expiry_clears_both_fixed_cookies(app):
    response = Response()
    expire_plain_demo_cookies(response, app.config)
    cookies = response.headers.getlist("Set-Cookie")
    assert len(cookies) == 2
    assert all("Max-Age=0" in item for item in cookies)


def test_base64_demo_profiles_are_fixed():
    assert original_demo_profile() == Base64Profile("student", "user")
    assert modified_demo_profile() == Base64Profile("student", "admin")


def test_base64_round_trip_preserves_profile():
    profile = Base64Profile("student", "user")
    result = decode_profile(encode_profile(profile))
    assert result.valid and result.profile == profile
    assert result.reason == "decoded_without_integrity_check"


@pytest.mark.parametrize(
    ("value", "reason"),
    [
        (None, "missing_cookie"),
        ("", "missing_cookie"),
        ("%%%", "invalid_base64_or_json"),
        ("A" * 2049, "cookie_too_large"),
        (_b64_json(["student", "user"]), "invalid_payload_shape"),
        (_b64_json({"username": "student", "role": "user", "extra": True}), "invalid_payload_shape"),
        (_b64_json({"username": 10, "role": "user"}), "invalid_payload_types"),
        (_b64_json({"username": "student", "role": "owner"}), "invalid_payload_values"),
    ],
)
def test_base64_decoder_rejects_invalid_inputs(value, reason):
    result = decode_profile(value)
    assert result.valid is False
    assert result.profile is None
    assert result.reason == reason


def test_signed_service_round_trip_preserves_verified_claim(app, tmp_path):
    path = seed_database(tmp_path / "signed.sqlite3")
    connection = connect_database(path)
    user = get_user_by_id(connection, 10)
    connection.close()
    result = verify_signed_profile(sign_profile(user, app.config, datetime.now(UTC)), app.config)
    assert result.valid and result.payload.user_id == 10
    assert result.signature_status == "valid" and result.deserialization_executed


def test_signed_service_does_not_deserialize_bad_signature(app):
    result = verify_signed_profile("not.a.valid.signature", app.config)
    assert result.valid is False
    assert result.deserialization_executed is False
    assert result.signature_status == "invalid"


def test_signed_service_rejects_validly_signed_wrong_shape(app):
    token = create_serializer(app.config).dumps({"user_id": 10})
    result = verify_signed_profile(token, app.config)
    assert result.valid is False
    assert result.deserialization_executed is True
    assert result.reason == "invalid_payload_shape"


def test_signed_expiry_uses_only_fixed_cookie_name(app):
    response = Response()
    expire_signed_cookie(response, app.config)
    header = response.headers["Set-Cookie"]
    assert header.startswith(f"{SIGNED_COOKIE}=") and "Max-Age=0" in header


def test_encrypted_missing_cookie_is_handled_without_exception(app):
    result = decrypt_demo_profile(None, app.config)
    assert result.valid is False and result.reason == "missing_cookie"
    assert result.confidentiality_protected and result.integrity_protected


def test_encrypted_expiry_uses_fixed_cookie_name(app):
    response = Response()
    expire_encrypted_demo_cookie(response, app.config)
    header = response.headers["Set-Cookie"]
    assert header.startswith(f"{ENCRYPTED_COOKIE}=") and "Max-Age=0" in header

