from __future__ import annotations

import sqlite3

import pytest
from werkzeug.security import check_password_hash

from seed import DEMO_ACCOUNTS, PASSWORD_METHOD, seed_database


@pytest.fixture()
def seeded_path(tmp_path):
    return seed_database(tmp_path / "seed.sqlite3")


def test_seed_creates_exact_demo_identities(seeded_path):
    with sqlite3.connect(seeded_path) as connection:
        rows = connection.execute("SELECT id, username, role FROM users ORDER BY id").fetchall()
    assert rows == [(1, "admin_lab", "admin"), (10, "student", "user")]


@pytest.mark.parametrize(
    ("username", "password"),
    [("student", "Student123!"), ("admin_lab", "AdminLab123!")],
)
def test_seeded_passwords_verify(seeded_path, username, password):
    with sqlite3.connect(seeded_path) as connection:
        stored = connection.execute("SELECT password_hash FROM users WHERE username = ?", (username,)).fetchone()[0]
    assert stored != password
    assert check_password_hash(stored, password)


def test_seed_uses_required_pbkdf2_iterations(seeded_path):
    with sqlite3.connect(seeded_path) as connection:
        hashes = [row[0] for row in connection.execute("SELECT password_hash FROM users")]
    assert PASSWORD_METHOD == "pbkdf2:sha256:600000"
    assert all(value.startswith("pbkdf2:sha256:600000$") for value in hashes)


def test_seed_is_idempotent(seeded_path):
    seed_database(seeded_path)
    with sqlite3.connect(seeded_path) as connection:
        assert connection.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 2


def test_seed_source_accounts_are_fixed_and_non_real():
    assert {(account.id, account.username) for account in DEMO_ACCOUNTS} == {(10, "student"), (1, "admin_lab")}
    assert all(account.email.endswith("@lab.local") for account in DEMO_ACCOUNTS)

