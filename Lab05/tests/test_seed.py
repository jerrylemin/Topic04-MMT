from database import query_all, query_one
from seed import PRODUCTS, USERS


def test_seed_contains_exact_demo_usernames(shared_app):
    with shared_app.app_context():
        usernames = [row["username"] for row in query_all("SELECT username FROM users ORDER BY id")]
    assert usernames == ["admin_lab", "student_a", "student_b"]


def test_seed_contains_required_product_names(shared_app):
    expected = {product[1] for product in PRODUCTS}
    with shared_app.app_context():
        actual = {row["name"] for row in query_all("SELECT name FROM products")}
    assert actual == expected


def test_seed_has_three_users_and_at_least_eight_products(shared_app):
    with shared_app.app_context():
        users = query_one("SELECT COUNT(*) AS count FROM users")["count"]
        products = query_one("SELECT COUNT(*) AS count FROM products")["count"]
    assert users == len(USERS) == 3
    assert products >= 8


def test_seed_uses_only_lab_local_email_addresses(shared_app):
    with shared_app.app_context():
        emails = [row["email"] for row in query_all("SELECT email FROM users")]
    assert all(email.endswith("@lab.local") for email in emails)


def test_database_has_no_plaintext_password_column(shared_app):
    with shared_app.app_context():
        columns = {row["name"] for row in query_all("PRAGMA table_info(users)")}
    assert "password" not in columns


def test_seed_passwords_are_not_stored_verbatim(shared_app):
    with shared_app.app_context():
        serialized = " ".join(str(tuple(row)) for row in query_all("SELECT * FROM users"))
    for password in ("AdminLab123!", "StudentA123!", "StudentB123!"):
        assert password not in serialized

