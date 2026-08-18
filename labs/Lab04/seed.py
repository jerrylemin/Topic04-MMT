from flask import Flask, has_app_context
from werkzeug.security import generate_password_hash

from config import Config
from database import get_db, init_db


USERS = (
    (10, "victim", "victim_old@lab.local", "Victim123!", "user", 1_000_000),
    (11, "receiver", "receiver@lab.local", "Receiver123!", "user", 500_000),
)


def reset_database(*, preserve_evidence: bool = False) -> None:
    db = get_db()
    db.execute("DELETE FROM demo_transfers")
    if not preserve_evidence:
        db.executescript("""
            DELETE FROM audit_logs;
            DELETE FROM state_history;
            DELETE FROM trace_records;
        """)
        db.execute("DELETE FROM users")
    db.executemany(
        """INSERT INTO users
           (id, username, email, password_hash, role, demo_balance)
           VALUES (?, ?, ?, ?, ?, ?)
           ON CONFLICT(id) DO UPDATE SET
             username = excluded.username,
             email = excluded.email,
             password_hash = excluded.password_hash,
             role = excluded.role,
             demo_balance = excluded.demo_balance,
             updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now')""",
        [(user_id, username, email, generate_password_hash(password), role, balance)
         for user_id, username, email, password, role, balance in USERS],
    )
    db.commit()


def main() -> None:
    app = Flask(__name__)
    app.config.from_object(Config)
    with app.app_context():
        init_db()
        reset_database()
    print("Lab04 database reset with local demo accounts.")


if __name__ == "__main__":
    main()
