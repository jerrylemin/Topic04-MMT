from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from werkzeug.security import generate_password_hash

from config import Config
from database import connect_database, initialize_database, transaction
from security_utils import isoformat_utc


PASSWORD_METHOD = "pbkdf2:sha256:600000"


@dataclass(frozen=True, slots=True)
class DemoAccount:
    id: int
    username: str
    display_name: str
    email: str
    role: str
    password: str


DEMO_ACCOUNTS = (
    DemoAccount(10, "student", "Sinh viên Demo", "student@lab.local", "user", "Student123!"),
    DemoAccount(1, "admin_lab", "Quản trị Lab", "admin@lab.local", "admin", "AdminLab123!"),
)


def seed_database(database_path: str | Path | None = None) -> Path:
    path = Path(database_path or Config.DATABASE)
    conn = connect_database(path)
    try:
        initialize_database(conn)
        now = isoformat_utc()
        with transaction(conn, immediate=True):
            for account in DEMO_ACCOUNTS:
                password_hash = generate_password_hash(account.password, method=PASSWORD_METHOD)
                conn.execute(
                    "INSERT INTO users (id, username, display_name, email, password_hash, role, active, "
                    "created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?) "
                    "ON CONFLICT(id) DO UPDATE SET username = excluded.username, "
                    "display_name = excluded.display_name, email = excluded.email, "
                    "password_hash = excluded.password_hash, role = excluded.role, active = 1, "
                    "updated_at = excluded.updated_at",
                    (
                        account.id, account.username, account.display_name, account.email,
                        password_hash, account.role, now, now,
                    ),
                )
    finally:
        conn.close()
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed the fixed local Lab06 demo accounts")
    parser.add_argument("--database", type=Path, default=Path(Config.DATABASE))
    args = parser.parse_args()
    seeded = seed_database(args.database)
    print(f"Seeded Lab06 database: {seeded}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
