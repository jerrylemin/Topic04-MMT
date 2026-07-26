import re
from pathlib import Path

from werkzeug.security import check_password_hash

from database import query_all, query_one


ROOT = Path(__file__).parents[1]


def test_home_health_login_and_password_hash(app, client):
    assert client.get("/").status_code == 200
    assert client.get("/health").json["status"] == "ok"
    with app.app_context():
        user = query_one("SELECT password_hash FROM users WHERE id = ?", (12,))
        assert user["password_hash"] != "UserA123!"
        assert check_password_hash(user["password_hash"], "UserA123!")
    assert client.post("/login", data={"username": "user_a", "password": "wrong"}).status_code == 401


def test_protected_route_rejects_anonymous(client):
    response = client.get("/products")
    assert response.status_code == 302 and "/login" in response.location


def test_products_and_cart_are_database_backed(app, client, login):
    login()
    assert "100,000" in client.get("/products").text
    client.post("/cart/add", data={"product_id": 5, "quantity": 2})
    with app.app_context():
        item = query_one("SELECT user_id, product_id, quantity FROM cart_items")
        assert dict(item) == {"user_id": 12, "product_id": 5, "quantity": 2}


def test_vulnerable_checkout_accepts_and_stores_client_price(app, client, login):
    login()
    response = client.post("/vulnerable/checkout", data={"product_id": 5, "quantity": 1, "price": 1})
    assert response.status_code == 200
    with app.app_context():
        invoice = query_one("SELECT id, total_amount FROM invoices ORDER BY id DESC LIMIT 1")
        item = query_one("SELECT unit_price FROM invoice_items WHERE invoice_id = ?", (invoice["id"],))
        assert invoice["total_amount"] == 1 and item["unit_price"] == 1


def test_secure_checkout_ignores_client_price_and_audits_mismatch(app, client, login):
    login()
    response = client.post("/secure/checkout", data={"product_id": 5, "quantity": 1, "price": 1})
    assert response.status_code == 200
    with app.app_context():
        invoice = query_one("SELECT id, total_amount FROM invoices ORDER BY id DESC LIMIT 1")
        item = query_one("SELECT unit_price FROM invoice_items WHERE invoice_id = ?", (invoice["id"],))
        audit = query_one("SELECT * FROM audit_logs WHERE action = ?", ("checkout_price_mismatch",))
        assert invoice["total_amount"] == 100000 and item["unit_price"] == 100000
        assert audit["submitted_value"] == "1" and audit["original_value"] == "100000"


def test_secure_checkout_ignores_even_nonnumeric_client_price(app, client, login):
    login()
    assert client.post("/secure/checkout", data={"product_id": 5, "quantity": 1, "price": "FREE"}).status_code == 200
    with app.app_context():
        assert query_one("SELECT total_amount FROM invoices ORDER BY id DESC LIMIT 1")["total_amount"] == 100000


def test_checkout_rejects_bad_quantity_and_product(client, login):
    login()
    assert client.post("/secure/checkout", data={"product_id": 5, "quantity": 0, "price": 1}).status_code == 400
    assert client.post("/secure/checkout", data={"product_id": 999, "quantity": 1, "price": 1}).status_code == 400


def test_vulnerable_idor_discloses_user_b_invoice(client, login):
    login()
    response = client.get("/vulnerable/invoice?id=1002")
    assert response.status_code == 200 and "250,000" in response.text


def test_secure_idor_returns_403_without_invoice_content_and_logs(app, client, login):
    login()
    response = client.get("/secure/invoice?id=1002")
    assert response.status_code == 403
    assert "Wireless Mouse" not in response.text and "250,000" not in response.text
    with app.app_context():
        audit = query_one("SELECT * FROM audit_logs WHERE action = ?", ("invoice_access_denied",))
        assert audit and audit["decision"] == "denied"


def test_owner_and_admin_invoice_policy(client, login):
    login()
    assert client.get("/secure/invoice?id=1001").status_code == 200
    client.post("/logout")
    login("admin", "Admin123!")
    assert client.get("/secure/invoice?id=1002").status_code == 200


def test_vulnerable_profile_accepts_role_admin(app, client, login):
    login()
    response = client.post("/vulnerable/profile/update", data={
        "user_id": 12, "email": "usera@lab.local", "role": "admin",
    })
    assert response.status_code == 200
    with app.app_context():
        assert query_one("SELECT role FROM users WHERE id = ?", (12,))["role"] == "admin"
    with client.session_transaction() as session:
        assert session["role"] == "admin"


def test_secure_profile_rejects_sensitive_fields_and_uses_session_user(app, client, login):
    login()
    response = client.post("/secure/profile/update", data={
        "user_id": 13, "email": "usera.changed@lab.local", "role": "admin",
    })
    assert response.status_code == 200
    with app.app_context():
        user_a = query_one("SELECT email, role FROM users WHERE id = ?", (12,))
        user_b = query_one("SELECT email, role FROM users WHERE id = ?", (13,))
        actions = {row["action"] for row in query_all("SELECT action FROM audit_logs")}
        assert dict(user_a) == {"email": "usera.changed@lab.local", "role": "user"}
        assert dict(user_b) == {"email": "userb@lab.local", "role": "user"}
        assert {"target_user_mismatch", "sensitive_field_submitted"} <= actions


def test_secure_profile_rejects_invalid_email(app, client, login):
    login()
    assert client.post("/secure/profile/update", data={"email": "not-an-email"}).status_code == 400
    with app.app_context():
        assert query_one("SELECT email FROM users WHERE id = ?", (12,))["email"] == "usera@lab.local"


def test_trace_masks_cookie_and_contains_required_inspectors(app, client, login):
    login()
    client.set_cookie("demo", "secret-cookie-value")
    client.post("/secure/checkout", data={"product_id": 5, "quantity": 1, "price": 1})
    with app.app_context():
        trace_id = query_one("SELECT trace_id FROM trace_records ORDER BY created_at DESC LIMIT 1")["trace_id"]
    trace = client.get(f"/api/trace/{trace_id}").json
    assert "secret-cookie-value" not in trace["request_inspector"]["cookie"]
    assert "***" in trace["request_inspector"]["cookie"]
    assert {"database_price", "submitted_price"} <= trace["database_inspector"].keys()
    assert trace["steps"] and trace["final_verdict"]["success"] is False


def test_audit_does_not_store_password_or_full_cookie(app, client, login):
    login()
    client.post("/secure/profile/update", data={"email": "new@lab.local", "password": "NeverStoreThis"})
    with app.app_context():
        payload = "\n".join(str(tuple(row)) for row in query_all("SELECT * FROM audit_logs"))
        assert "NeverStoreThis" not in payload and "session=" not in payload


def test_security_headers_request_limit_reset_and_local_bind(app, client, login):
    response = client.get("/")
    for name in ["Content-Security-Policy", "X-Content-Type-Options", "X-Frame-Options", "Referrer-Policy", "Permissions-Policy"]:
        assert name in response.headers
    assert client.post("/login", data=b"x" * (65 * 1024), content_type="application/x-www-form-urlencoded").status_code == 413
    login()
    client.post("/vulnerable/profile/update", data={"user_id": 12, "email": "usera@lab.local", "role": "admin"})
    assert client.post("/reset-lab").status_code == 302
    with app.app_context():
        assert query_one("SELECT role FROM users WHERE id = ?", (12,))["role"] == "user"
    assert app.config["BIND_HOST"] == "127.0.0.1"


def test_sql_calls_do_not_interpolate_request_data():
    source = "\n".join((ROOT / name).read_text(encoding="utf-8") for name in ["auth.py", "services.py", "audit_service.py"])
    assert not re.search(r"execute\s*\(\s*f[\"']", source)
    assert not re.search(r"execute\s*\(\s*[\"'][^\n]*\+", source)
