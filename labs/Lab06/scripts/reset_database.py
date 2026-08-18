"""Reset only the fixed Lab06 SQLite database and reseed demo accounts."""

from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from database import connect_database, initialize_database, transaction  # noqa: E402
from seed import seed_database  # noqa: E402


DATABASE = Path(os.environ.get("LAB06_DATABASE", ROOT / "data" / "lab06.sqlite3"))
EVENT_DELETES = (
    "DELETE FROM session_events",
    "DELETE FROM cookie_events",
    "DELETE FROM audit_logs",
    "DELETE FROM server_sessions",
)


def reset_database() -> Path:
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    connection = connect_database(DATABASE)
    try:
        initialize_database(connection)
        with transaction(connection, immediate=True):
            for statement in EVENT_DELETES:
                connection.execute(statement)
    finally:
        connection.close()
    seed_database(DATABASE)
    return DATABASE


def main() -> int:
    path = reset_database()
    print(f"Reset fixed Lab06 database: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
