from __future__ import annotations

import sqlite3
from dataclasses import dataclass

from werkzeug.security import check_password_hash

from database import UserRecord, get_user_by_id, get_user_by_username


@dataclass(frozen=True, slots=True)
class AuthResult:
    authenticated: bool
    user: UserRecord | None
    reason: str


# LAB06-CODE:password_verification:START
def authenticate(conn: sqlite3.Connection, username: str, password: str) -> AuthResult:
    user = get_user_by_username(conn, username)
    if user is None or not user.active:
        return AuthResult(False, None, "invalid_credentials")
    if not check_password_hash(user.password_hash, password):
        return AuthResult(False, None, "invalid_credentials")
    return AuthResult(True, user, "password_verified")
# LAB06-CODE:password_verification:END


def require_active_user(conn: sqlite3.Connection, user_id: int) -> UserRecord | None:
    user = get_user_by_id(conn, user_id)
    return user if user is not None and user.active else None
