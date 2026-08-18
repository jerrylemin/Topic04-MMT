from __future__ import annotations

import hashlib
import secrets
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Mapping

from flask import Response

from config import LabConfig, cookie_options
from database import transaction
from security_utils import fingerprint, isoformat_utc


SESSION_COOKIE = "lab06_session"


@dataclass(frozen=True, slots=True)
class SessionIssue:
    user_id: int
    raw_token: str = field(repr=False)
    token_fingerprint: str = ""
    created_at: str = ""
    expires_at: str = ""
    rotation_reason: str = "login"


@dataclass(frozen=True, slots=True)
class SessionResolution:
    valid: bool
    reason: str
    session_id: int | None = None
    token_fingerprint: str | None = None
    user_id: int | None = None
    username: str | None = None
    database_role: str | None = None
    active: bool = False
    created_at: str | None = None
    expires_at: str | None = None
    last_seen_at: str | None = None


def generate_session_token() -> str:
    return secrets.token_urlsafe(32)


def hash_session_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


def fingerprint_session_token(raw_token: str) -> str:
    return fingerprint(raw_token)


def _aware(value: datetime) -> datetime:
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value.astimezone(timezone.utc)


def _parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


# LAB06-CODE:session_rotation:START
def rotate_session(
    conn: sqlite3.Connection,
    *,
    user_id: int,
    previous_raw_token: str | None,
    now: datetime,
    ttl: timedelta,
    trace_id: str,
    reason: str = "login",
) -> SessionIssue:
    current = _aware(now)
    created_at = isoformat_utc(current)
    expires_at = isoformat_utc(current + ttl)
    raw_token = generate_session_token()
    token_hash = hash_session_token(raw_token)
    new_fingerprint = fingerprint_session_token(raw_token)
    old_fingerprint = fingerprint_session_token(previous_raw_token) if previous_raw_token else None
    with transaction(conn, immediate=True):
        revoked = 0
        if previous_raw_token:
            revoked = conn.execute(
                "UPDATE server_sessions SET active = 0, revoked_at = ?, rotation_reason = ? "
                "WHERE session_token_hash = ? AND active = 1",
                (created_at, reason, hash_session_token(previous_raw_token)),
            ).rowcount
        conn.execute(
            "INSERT INTO server_sessions (session_token_hash, user_id, created_at, expires_at, "
            "last_seen_at, active, revoked_at, rotation_reason) VALUES (?, ?, ?, ?, ?, 1, NULL, ?)",
            (token_hash, user_id, created_at, expires_at, created_at, reason),
        )
        conn.execute(
            "INSERT INTO session_events (timestamp, user_id, event_type, old_session_fingerprint, "
            "new_session_fingerprint, reason, trace_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                created_at, user_id,
                "server_session_rotated" if revoked else "server_session_created",
                old_fingerprint if revoked else None, new_fingerprint, reason, trace_id,
            ),
        )
    return SessionIssue(user_id, raw_token, new_fingerprint, created_at, expires_at, reason)
# LAB06-CODE:session_rotation:END


# LAB06-CODE:session_resolution:START
def resolve_session(
    conn: sqlite3.Connection, raw_token: str | None, now: datetime
) -> SessionResolution:
    if not raw_token:
        return SessionResolution(False, "missing_session_cookie")
    token_hash = hash_session_token(raw_token)
    token_fingerprint = fingerprint_session_token(raw_token)
    row = conn.execute(
        "SELECT s.id, s.user_id, s.created_at, s.expires_at, s.last_seen_at, s.active, "
        "u.username, u.role, u.active AS user_active FROM server_sessions AS s "
        "JOIN users AS u ON u.id = s.user_id WHERE s.session_token_hash = ?",
        (token_hash,),
    ).fetchone()
    if row is None:
        return SessionResolution(False, "unknown_session", token_fingerprint=token_fingerprint)
    common = dict(
        session_id=int(row["id"]), token_fingerprint=token_fingerprint,
        user_id=int(row["user_id"]), username=str(row["username"]),
        database_role=str(row["role"]), active=bool(row["active"]),
        created_at=str(row["created_at"]), expires_at=str(row["expires_at"]),
        last_seen_at=str(row["last_seen_at"]),
    )
    if not bool(row["active"]):
        return SessionResolution(False, "inactive_session", **common)
    current = _aware(now)
    if _parse_time(str(row["expires_at"])) <= current:
        with transaction(conn, immediate=True):
            conn.execute(
                "UPDATE server_sessions SET active = 0, revoked_at = ?, rotation_reason = ? WHERE id = ?",
                (isoformat_utc(current), "expired", int(row["id"])),
            )
        common["active"] = False
        return SessionResolution(False, "expired_session", **common)
    if not bool(row["user_active"]):
        return SessionResolution(False, "inactive_user", **common)
    seen = isoformat_utc(current)
    with transaction(conn, immediate=True):
        conn.execute("UPDATE server_sessions SET last_seen_at = ? WHERE id = ?", (seen, int(row["id"])))
    common["last_seen_at"] = seen
    return SessionResolution(True, "session_valid", **common)
# LAB06-CODE:session_resolution:END


# LAB06-CODE:logout_invalidation:START
def revoke_session(
    conn: sqlite3.Connection,
    *,
    raw_token: str | None,
    now: datetime,
    reason: str,
    trace_id: str,
) -> bool:
    if not raw_token:
        return False
    timestamp = isoformat_utc(_aware(now))
    token_hash = hash_session_token(raw_token)
    token_fingerprint = fingerprint_session_token(raw_token)
    with transaction(conn, immediate=True):
        row = conn.execute(
            "SELECT id, user_id FROM server_sessions WHERE session_token_hash = ? AND active = 1",
            (token_hash,),
        ).fetchone()
        if row is None:
            return False
        conn.execute(
            "UPDATE server_sessions SET active = 0, revoked_at = ?, rotation_reason = ? WHERE id = ?",
            (timestamp, reason, int(row["id"])),
        )
        conn.execute(
            "INSERT INTO session_events (timestamp, user_id, event_type, old_session_fingerprint, "
            "new_session_fingerprint, reason, trace_id) VALUES (?, ?, ?, ?, NULL, ?, ?)",
            (timestamp, int(row["user_id"]), "logout_invalidated_session", token_fingerprint, reason, trace_id),
        )
    return True
# LAB06-CODE:logout_invalidation:END


def revoke_all_demo_sessions(
    conn: sqlite3.Connection, *, now: datetime, trace_id: str, reason: str = "lab_reset"
) -> int:
    timestamp = isoformat_utc(_aware(now))
    with transaction(conn, immediate=True):
        count = conn.execute(
            "UPDATE server_sessions SET active = 0, revoked_at = ?, rotation_reason = ? WHERE active = 1",
            (timestamp, reason),
        ).rowcount
        conn.execute(
            "INSERT INTO session_events (timestamp, user_id, event_type, old_session_fingerprint, "
            "new_session_fingerprint, reason, trace_id) VALUES (?, NULL, ?, NULL, NULL, ?, ?)",
            (timestamp, "all_demo_sessions_revoked", reason, trace_id),
        )
    return int(count)


def set_session_cookie(
    response: Response,
    issue: SessionIssue,
    config: LabConfig | Mapping[str, Any] | Any,
) -> None:
    if isinstance(config, LabConfig):
        max_age = config.session_ttl_seconds
    elif isinstance(config, Mapping):
        max_age = int(config["SESSION_TTL_SECONDS"])
    else:
        max_age = int(getattr(config, "SESSION_TTL_SECONDS"))
    response.set_cookie(
        SESSION_COOKIE,
        issue.raw_token,
        **cookie_options(config, httponly=True, max_age=max_age),
    )


def expire_session_cookie(
    response: Response, config: LabConfig | Mapping[str, Any] | Any
) -> None:
    response.set_cookie(
        SESSION_COOKIE,
        "",
        expires=0,
        **cookie_options(config, httponly=True, max_age=0),
    )
