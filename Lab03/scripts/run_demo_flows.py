from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import create_app  # noqa: E402
from database import get_db, query_all, query_one  # noqa: E402
from seed import reset_database  # noqa: E402

TRACE_NAMES = [
    ("checkout_normal_vulnerable", "POST", "/vulnerable/checkout", {"product_id": 5, "quantity": 1, "price": 100000}),
    ("checkout_tampered_vulnerable", "POST", "/vulnerable/checkout", {"product_id": 5, "quantity": 1, "price": 1}),
    ("checkout_tampered_secure", "POST", "/secure/checkout", {"product_id": 5, "quantity": 1, "price": 1}),
    ("invoice_owner_vulnerable", "GET", "/vulnerable/invoice", {"id": 1001}),
    ("invoice_idor_vulnerable", "GET", "/vulnerable/invoice", {"id": 1002}),
    ("invoice_idor_secure", "GET", "/secure/invoice", {"id": 1002}),
    ("profile_normal_vulnerable", "POST", "/vulnerable/profile/update", {"user_id": 12, "email": "usera@lab.local", "role": "user"}),
    ("profile_role_tampered_vulnerable", "POST", "/vulnerable/profile/update", {"user_id": 12, "email": "usera@lab.local", "role": "admin"}),
    ("profile_role_tampered_secure", "POST", "/secure/profile/update", {"user_id": 12, "email": "usera@lab.local", "role": "admin"}),
]


def write(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def login(client):
    response = client.post("/login", data={"username": "user_a", "password": "UserA123!"})
    if response.status_code not in (302, 303):
        raise RuntimeError("Không đăng nhập được User A.")


def latest_trace():
    row = query_one("SELECT trace_id, payload_json FROM trace_records ORDER BY created_at DESC, rowid DESC LIMIT 1")
    return row["trace_id"], json.loads(row["payload_json"])


def reset_checkout_data():
    db = get_db()
    db.execute("DELETE FROM invoice_items WHERE invoice_id > 1003")
    db.execute("DELETE FROM invoices WHERE id > 1003")
    db.commit()


def reset_user_a():
    db = get_db()
    db.execute("UPDATE users SET email = 'usera@lab.local', role = 'user' WHERE id = 12")
    db.commit()


def main():
    app = create_app({"TESTING": True})
    client = app.test_client()
    with app.app_context():
        reset_database()
    login(client)
    results = []
    for name, method, route, data in TRACE_NAMES:
        if name == "checkout_tampered_secure":
            with app.app_context():
                reset_checkout_data()
            client.post("/logout")
            login(client)
        if name == "profile_role_tampered_secure":
            with app.app_context():
                reset_user_a()
            client.post("/logout")
            login(client)
        response = client.open(route, method=method, query_string=data if method == "GET" else None,
                               data=data if method == "POST" else None)
        with app.app_context():
            trace_id, trace = latest_trace()
        write(ROOT / "evidence" / "traces" / f"{name}.json", trace)
        public_data = {key: value for key, value in data.items() if key != "password"}
        write(ROOT / "evidence" / "requests" / f"{name}.json", {"method": method, "route": route, "parameters": public_data, "trace_id": trace_id})
        write(ROOT / "evidence" / "responses" / f"{name}.json", {"status": response.status_code, "trace_id": trace_id,
              "decision": trace.get("final_verdict", {}), "content_type": response.content_type})
        results.append({"scenario": name, "status": response.status_code, "trace_id": trace_id,
                        "decision": trace.get("final_verdict", {}).get("success")})
    with app.app_context():
        write(ROOT / "evidence" / "audit" / "audit_logs.json", [dict(row) for row in query_all("SELECT * FROM audit_logs ORDER BY id")])
        write(ROOT / "evidence" / "database" / "snapshot.json", {
            "users": [dict(row) for row in query_all("SELECT id, username, email, role FROM users ORDER BY id")],
            "products": [dict(row) for row in query_all("SELECT * FROM products ORDER BY id")],
            "invoices": [dict(row) for row in query_all("SELECT * FROM invoices ORDER BY id")],
            "invoice_items": [dict(row) for row in query_all("SELECT * FROM invoice_items ORDER BY id")],
        })
    write(ROOT / "evidence" / "logs" / "demo_flows.json", results)
    print(json.dumps(results, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
