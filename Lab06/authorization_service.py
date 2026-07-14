from __future__ import annotations

from dataclasses import dataclass

from base64_cookie_service import Base64DecodeResult
from cookie_service import PlainCookieIdentity
from database import UserRecord
from server_session_service import SessionResolution
from signed_cookie_service import SignedVerificationResult


@dataclass(frozen=True, slots=True)
class AuthorizationDecision:
    allowed: bool
    subject: str | None
    action: str
    resource: str
    authentication_source: str
    submitted_role: str | None
    database_role: str | None
    policy: str
    reason: str
    database_role_checked: bool

    @property
    def decision(self) -> str:
        return "allow" if self.allowed else "deny"


# LAB06-CODE:plain_authorization:START
def authorize_plain_admin(identity: PlainCookieIdentity) -> AuthorizationDecision:
    allowed = identity.username_present and identity.role_present and identity.role == "admin"
    return AuthorizationDecision(
        allowed=allowed, subject=identity.username, action="view_admin",
        resource="plain_admin_page", authentication_source="client_cookie",
        submitted_role=identity.role, database_role=None,
        policy="trust client-controlled lab06_role cookie",
        reason="client_cookie_role_admin" if allowed else "client_cookie_role_not_admin",
        database_role_checked=False,
    )
# LAB06-CODE:plain_authorization:END


# LAB06-CODE:base64_authorization_service:START
def authorize_base64_admin(result: Base64DecodeResult) -> AuthorizationDecision:
    profile = result.profile if result.valid else None
    allowed = bool(profile and profile.role == "admin")
    return AuthorizationDecision(
        allowed=allowed, subject=None if profile is None else profile.username,
        action="view_admin", resource="base64_admin_page",
        authentication_source="client_base64_cookie",
        submitted_role=None if profile is None else profile.role, database_role=None,
        policy="decode Base64 JSON and trust client-controlled role",
        reason="decoded_role_admin" if allowed else result.reason,
        database_role_checked=False,
    )
# LAB06-CODE:base64_authorization_service:END


# LAB06-CODE:signed_database_authorization:START
def authorize_signed_admin(
    verified: SignedVerificationResult, database_user: UserRecord | None
) -> AuthorizationDecision:
    payload = verified.payload if verified.valid else None
    user_matches_claim = bool(
        payload and database_user and database_user.active and database_user.id == payload.user_id
    )
    allowed = bool(user_matches_claim and database_user and database_user.role == "admin")
    if not verified.valid:
        reason = verified.reason
    elif not user_matches_claim:
        reason = "database_user_missing_or_identity_mismatch"
    elif allowed:
        reason = "current_database_role_admin"
    else:
        reason = "current_database_role_not_admin"
    return AuthorizationDecision(
        allowed=allowed,
        subject=None if database_user is None else database_user.username,
        action="view_admin", resource="signed_admin_page",
        authentication_source="verified_signed_cookie",
        submitted_role=None if payload is None else payload.role,
        database_role=None if database_user is None else database_user.role,
        policy="valid signature plus current database role must equal admin",
        reason=reason, database_role_checked=True,
    )
# LAB06-CODE:signed_database_authorization:END


# LAB06-CODE:session_database_authorization:START
def authorize_session_admin(resolution: SessionResolution) -> AuthorizationDecision:
    allowed = resolution.valid and resolution.database_role == "admin"
    return AuthorizationDecision(
        allowed=allowed, subject=resolution.username, action="view_admin",
        resource="server_session_admin_page", authentication_source="server_session",
        submitted_role=None, database_role=resolution.database_role,
        policy="active server session plus current database role must equal admin",
        reason="current_database_role_admin" if allowed else resolution.reason,
        database_role_checked=resolution.user_id is not None,
    )
# LAB06-CODE:session_database_authorization:END
