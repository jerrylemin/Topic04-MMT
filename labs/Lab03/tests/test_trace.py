from database import query_one


def latest_trace_id(app):
    with app.app_context():
        return query_one("SELECT trace_id FROM trace_records ORDER BY created_at DESC, rowid DESC LIMIT 1")["trace_id"]


def test_checkout_trace_exports_required_top_level_fields(app, client, login):
    login()
    client.post("/secure/checkout", data={"product_id": 5, "quantity": 1, "price": 1})
    trace = client.get(f"/api/trace/{latest_trace_id(app)}").json
    required = {"trace_id", "current_user", "product_id", "quantity", "database_price", "submitted_price",
                "calculated_total", "stored_total", "price_mismatch", "decision", "audit_event", "steps"}
    assert required <= trace.keys()


def test_idor_trace_exports_required_top_level_fields(app, client, login):
    login()
    client.get("/secure/invoice?id=1002")
    trace = client.get(f"/api/trace/{latest_trace_id(app)}").json
    required = {"trace_id", "current_user_id", "invoice_id", "invoice_owner_id", "ownership_match",
                "authorization_policy", "decision", "http_status", "data_returned", "steps"}
    assert required <= trace.keys()


def test_profile_trace_exports_required_top_level_fields(app, client, login):
    login()
    client.post("/secure/profile/update", data={"email": "usera@lab.local", "role": "admin"})
    trace = client.get(f"/api/trace/{latest_trace_id(app)}").json
    required = {"trace_id", "current_user_id", "submitted_user_id", "submitted_role", "accepted_fields",
                "rejected_fields", "role_before", "role_after", "decision", "audit_event", "steps"}
    assert required <= trace.keys()
