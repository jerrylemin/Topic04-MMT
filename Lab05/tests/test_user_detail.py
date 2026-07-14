import pytest

from database import query_all


@pytest.mark.parametrize("route,prepared", [
    ("/vulnerable/user", "false"),
    ("/secure/user", "true"),
])
def test_existing_user_detail_returns_only_public_record(shared_app, shared_client, route, prepared):
    response = shared_client.get(route, query_string={"id": "1"})
    trace = shared_client.get(f'/api/trace/{response.headers["X-Lab-Trace-ID"]}').get_json()
    assert response.status_code == 200
    assert response.headers["X-Lab-Prepared"] == prepared
    assert trace["database_inspector"]["result_ids"] == [1]
    body = response.get_data(as_text=True)
    with shared_app.app_context():
        sensitive_values = [
            value
            for row in query_all("SELECT password_hash, legacy_password_digest FROM users")
            for value in tuple(row)
        ]
    assert "pbkdf2:sha256:600000$" not in body
    assert all(value not in body for value in sensitive_values)


@pytest.mark.parametrize("value", ["0", "-1", "abc", "1.5", ""])
def test_secure_user_detail_requires_positive_integer(shared_client, value):
    response = shared_client.get("/secure/user", query_string={"id": value})
    assert response.status_code == 400
    assert response.headers["X-Lab-Decision"] == "validation_failed"


def test_secure_user_detail_uses_placeholder_and_limit_one(shared_client):
    response = shared_client.get("/secure/user", query_string={"id": "2"})
    query = shared_client.get(f'/api/trace/{response.headers["X-Lab-Trace-ID"]}').get_json()["query_inspector"]
    assert "id = ?" in query["query_template"]
    assert "LIMIT 1" in query["query_template"]


def test_missing_secure_user_returns_generic_404(shared_client):
    response = shared_client.get("/secure/user", query_string={"id": "999"})
    assert response.status_code == 404
    assert response.headers["X-Lab-Decision"] == "not_found"
