"""Print a redacted snapshot of the fixed local Lab05 database."""

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import create_app  # noqa: E402
from database import query_all, query_one  # noqa: E402
from security_utils import password_metadata  # noqa: E402


def snapshot() -> dict:
    app = create_app({"TESTING": True})
    with app.app_context():
        counts = {
            table: query_one(f"SELECT COUNT(*) AS count FROM {table}")["count"]
            for table in ("users", "products", "audit_logs", "login_attempts", "query_events")
        }
        users = []
        for row in query_all("SELECT id, username, legacy_password_digest, password_hash FROM users ORDER BY id"):
            users.append({
                "id": row["id"],
                "username": row["username"],
                "legacy": password_metadata(row["legacy_password_digest"], secure=False),
                "secure": password_metadata(row["password_hash"], secure=True),
            })
    return {"database": "Lab05 local SQLite", "counts": counts, "password_storage": users}


def main() -> int:
    print(json.dumps(snapshot(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
