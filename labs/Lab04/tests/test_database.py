from werkzeug.security import check_password_hash

from database import query_one


def test_seed_uses_required_accounts_and_hashed_passwords(app):
    with app.app_context():
        victim = query_one("SELECT * FROM users WHERE id = ?", (10,))
        receiver = query_one("SELECT * FROM users WHERE id = ?", (11,))

    assert victim["email"] == "victim_old@lab.local"
    assert victim["demo_balance"] == 1_000_000
    assert victim["password_hash"] != "Victim123!"
    assert check_password_hash(victim["password_hash"], "Victim123!")
    assert receiver["demo_balance"] == 500_000
