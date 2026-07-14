"""Print redacted metadata for sessions in the fixed local Lab06 database."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from database import connect_database  # noqa: E402
from security_utils import fingerprint  # noqa: E402


DATABASE = Path(os.environ.get("LAB06_DATABASE", ROOT / "data" / "lab06.sqlite3"))


def safe_session_records() -> list[dict[str, object]]:
    if not DATABASE.exists():
        return []
    connection = connect_database(DATABASE)
    try:
        rows = connection.execute(
            "SELECT id, session_token_hash, user_id, created_at, expires_at, "
            "last_seen_at, active, revoked_at, rotation_reason "
            "FROM server_sessions ORDER BY id"
        ).fetchall()
    finally:
        connection.close()
    return [
        {
            "id": int(row["id"]),
            "session_hash_fingerprint": fingerprint(str(row["session_token_hash"])),
            "user_id": int(row["user_id"]),
            "created_at": row["created_at"],
            "expires_at": row["expires_at"],
            "last_seen_at": row["last_seen_at"],
            "active": bool(row["active"]),
            "revoked_at": row["revoked_at"],
            "rotation_reason": row["rotation_reason"],
        }
        for row in rows
    ]


def main() -> int:
    print(json.dumps(safe_session_records(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
