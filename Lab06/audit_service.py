from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from security_utils import bounded_text, isoformat_utc, redact


@dataclass(frozen=True, slots=True)
class AuditEvent:
    action: str
    route: str
    mode: str
    reason: str
    trace_id: str
    timestamp: str | None = None
    user_id: int | None = None
    username: str | None = None
    cookie_name: str | None = None
    cookie_status: str | None = None
    submitted_role: str | None = None
    database_role: str | None = None
    authorization_decision: str | None = None


@dataclass(frozen=True, slots=True)
class AuditRecord:
    id: int
    timestamp: str
    user_id: int | None
    username: str | None
    action: str
    route: str
    mode: str
    cookie_name: str | None
    cookie_status: str | None
    submitted_role: str | None
    database_role: str | None
    authorization_decision: str | None
    reason: str
    trace_id: str

    def to_dict(self) -> dict[str, object]:
        return redact(asdict(self))


def record_audit(conn: sqlite3.Connection, event: AuditEvent) -> int:
    cursor = conn.execute(
        "INSERT INTO audit_logs (timestamp, user_id, username, action, route, mode, "
        "cookie_name, cookie_status, submitted_role, database_role, "
        "authorization_decision, reason, trace_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            event.timestamp or isoformat_utc(), event.user_id,
            bounded_text(event.username, limit=64), bounded_text(event.action, limit=80),
            bounded_text(event.route, limit=160), bounded_text(event.mode, limit=32),
            bounded_text(event.cookie_name, limit=80), bounded_text(event.cookie_status, limit=80),
            bounded_text(event.submitted_role, limit=32), bounded_text(event.database_role, limit=32),
            bounded_text(event.authorization_decision, limit=32), bounded_text(event.reason, limit=500),
            bounded_text(event.trace_id, limit=80),
        ),
    )
    return int(cursor.lastrowid)


def _record(row: sqlite3.Row) -> AuditRecord:
    return AuditRecord(
        id=int(row["id"]), timestamp=str(row["timestamp"]), user_id=row["user_id"],
        username=row["username"], action=str(row["action"]), route=str(row["route"]),
        mode=str(row["mode"]), cookie_name=row["cookie_name"],
        cookie_status=row["cookie_status"], submitted_role=row["submitted_role"],
        database_role=row["database_role"],
        authorization_decision=row["authorization_decision"],
        reason=str(row["reason"]), trace_id=str(row["trace_id"]),
    )


def list_audit_events(conn: sqlite3.Connection, *, limit: int = 200) -> list[AuditRecord]:
    safe_limit = max(1, min(int(limit), 1000))
    rows = conn.execute(
        "SELECT id, timestamp, user_id, username, action, route, mode, cookie_name, "
        "cookie_status, submitted_role, database_role, authorization_decision, reason, trace_id "
        "FROM audit_logs ORDER BY id DESC LIMIT ?",
        (safe_limit,),
    ).fetchall()
    return [_record(row) for row in rows]


def export_audit_events(records: Sequence[AuditRecord], destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = [record.to_dict() for record in records]
    destination.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return destination
