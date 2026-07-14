import hmac
import secrets
import time

from flask import session

from security_utils import mask_secret


TOKEN_MIN_LENGTH = 32
TOKEN_MAX_LENGTH = 256
TOKEN_MAX_AGE_SECONDS = 3600


def generate_csrf_token() -> str:
    return secrets.token_urlsafe(32)


def issue_csrf_token() -> str:
    token = generate_csrf_token()
    session["csrf_token"] = token
    session["csrf_token_issued_at"] = time.time()
    return token


def ensure_csrf_token() -> str:
    return session.get("csrf_token") or issue_csrf_token()


def rotate_csrf_token() -> str:
    return issue_csrf_token()


def validate_csrf_token(expected: str | None, submitted: str | None, issued_at: float | None = None) -> dict:
    if not submitted:
        return {"present": False, "valid": False, "status": "missing", "reason": "token_missing"}
    if not expected or not isinstance(submitted, str) or not TOKEN_MIN_LENGTH <= len(submitted) <= TOKEN_MAX_LENGTH:
        return {"present": True, "valid": False, "status": "invalid", "reason": "token_invalid"}
    if issued_at is not None and time.time() - float(issued_at) > TOKEN_MAX_AGE_SECONDS:
        return {"present": True, "valid": False, "status": "invalid", "reason": "token_expired"}
    valid = hmac.compare_digest(expected, submitted)
    return {
        "present": True,
        "valid": valid,
        "status": "valid" if valid else "invalid",
        "reason": "token_matches_session" if valid else "token_mismatch",
    }


def validate_session_csrf(submitted: str | None) -> dict:
    return validate_csrf_token(session.get("csrf_token"), submitted, session.get("csrf_token_issued_at"))


def mask_csrf_token(token: str | None) -> str:
    return mask_secret(token)
