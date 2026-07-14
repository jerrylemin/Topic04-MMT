from __future__ import annotations

from base64_cookie_service import Base64DecodeResult, Base64Profile
from authorization_service import (
    authorize_base64_admin,
    authorize_plain_admin,
    authorize_session_admin,
    authorize_signed_admin,
)
from cookie_service import PlainCookieIdentity
from database import UserRecord
from server_session_service import SessionResolution
from signed_cookie_service import SignedProfile, SignedVerificationResult


def _user(role="user", user_id=10, username="student"):
    return UserRecord(user_id, username, "Demo", f"{username}@lab.local", "redacted", role, True, "now", "now")


def _verified(role="user", user_id=10, username="student"):
    payload = SignedProfile(user_id, username, role, "2026-01-01T00:00:00Z")
    return SignedVerificationResult(True, payload, "valid", "signature_verified", True)


def test_plain_authorization_intentionally_trusts_admin_cookie():
    decision = authorize_plain_admin(PlainCookieIdentity("student", "admin", True, True))
    assert decision.allowed and decision.submitted_role == "admin"
    assert not decision.database_role_checked


def test_plain_authorization_denies_missing_role():
    decision = authorize_plain_admin(PlainCookieIdentity("student", None, True, False))
    assert not decision.allowed and decision.decision == "deny"


def test_base64_authorization_intentionally_trusts_decoded_admin():
    decoded = Base64DecodeResult(True, Base64Profile("student", "admin"), "{}", "decoded_without_integrity_check")
    decision = authorize_base64_admin(decoded)
    assert decision.allowed and not decision.database_role_checked


def test_base64_authorization_denies_parse_failure():
    decision = authorize_base64_admin(Base64DecodeResult(False, None, None, "invalid_base64_or_json"))
    assert not decision.allowed and decision.reason == "invalid_base64_or_json"


def test_signed_student_claiming_admin_is_denied_by_database():
    decision = authorize_signed_admin(_verified(role="admin"), _user(role="user"))
    assert not decision.allowed
    assert decision.submitted_role == "admin" and decision.database_role == "user"
    assert decision.database_role_checked


def test_signed_admin_with_stale_user_claim_is_allowed_by_database():
    decision = authorize_signed_admin(_verified(role="user", user_id=1, username="admin_lab"), _user(role="admin", user_id=1, username="admin_lab"))
    assert decision.allowed and decision.database_role == "admin"


def test_signed_identity_mismatch_is_denied():
    decision = authorize_signed_admin(_verified(user_id=10), _user(role="admin", user_id=1, username="admin_lab"))
    assert not decision.allowed and decision.reason == "database_user_missing_or_identity_mismatch"


def test_invalid_signature_never_reaches_authorized_state():
    invalid = SignedVerificationResult(False, None, "invalid", "signature_rejected", False)
    decision = authorize_signed_admin(invalid, _user(role="admin", user_id=1, username="admin_lab"))
    assert not decision.allowed and decision.reason == "signature_rejected"


def test_session_authorization_uses_database_role():
    resolution = SessionResolution(True, "session_valid", user_id=1, username="admin_lab", database_role="admin", active=True)
    decision = authorize_session_admin(resolution)
    assert decision.allowed and decision.authentication_source == "server_session"
    assert decision.submitted_role is None


def test_invalid_session_is_denied_even_if_role_field_is_admin():
    resolution = SessionResolution(False, "inactive_session", user_id=1, username="admin_lab", database_role="admin", active=False)
    assert authorize_session_admin(resolution).allowed is False

