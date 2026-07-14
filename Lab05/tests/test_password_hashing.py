from werkzeug.security import check_password_hash, generate_password_hash

from database import query_all, query_one
from security_utils import legacy_digest, password_metadata


def test_all_secure_hashes_use_required_pbkdf2_work_factor(shared_app):
    with shared_app.app_context():
        hashes = [row["password_hash"] for row in query_all("SELECT password_hash FROM users")]
    assert all(value.startswith("pbkdf2:sha256:600000$") for value in hashes)


def test_secure_hash_verifies_with_werkzeug(shared_app):
    with shared_app.app_context():
        value = query_one("SELECT password_hash FROM users WHERE username = ?", ("student_a",))["password_hash"]
    assert check_password_hash(value, "StudentA123!") is True
    assert check_password_hash(value, "wrong") is False


def test_equal_passwords_receive_unique_salts():
    first = generate_password_hash("SamePassword123!", method="pbkdf2:sha256:600000")
    second = generate_password_hash("SamePassword123!", method="pbkdf2:sha256:600000")
    assert first != second
    assert check_password_hash(first, "SamePassword123!")
    assert check_password_hash(second, "SamePassword123!")


def test_legacy_digest_is_deterministic_unsalted_sha256():
    assert legacy_digest("demo") == legacy_digest("demo")
    metadata = password_metadata(legacy_digest("demo"), secure=False)
    assert metadata["algorithm"] == "sha256"
    assert metadata["salted"] is False
    assert metadata["length"] == 64


def test_database_password_metadata_never_needs_full_hash(shared_app):
    with shared_app.app_context():
        value = query_one("SELECT password_hash FROM users WHERE id = 1")["password_hash"]
    metadata = password_metadata(value, secure=True)
    assert set(metadata) == {"algorithm", "length", "fingerprint", "salted"}
    assert value not in metadata.values()

