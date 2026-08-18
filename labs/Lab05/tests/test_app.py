import pytest


@pytest.mark.parametrize("path", [
    "/", "/dashboard", "/vulnerable/login", "/secure/login",
    "/vulnerable/search", "/secure/search", "/comparison",
    "/security-controls", "/audit-logs", "/health",
])
def test_public_get_routes_are_available(shared_client, path):
    assert shared_client.get(path).status_code == 200


@pytest.mark.parametrize("path", ["/logout", "/reset-lab", "/api/trace/clear"])
def test_state_changing_routes_reject_get(shared_client, path):
    assert shared_client.get(path).status_code == 405


@pytest.mark.parametrize("path", ["/logout", "/reset-lab", "/api/trace/clear"])
def test_state_changing_routes_accept_post(shared_client, path):
    assert shared_client.post(path).status_code == 200


def test_health_has_stable_local_service_identity(shared_client):
    assert shared_client.get("/health").get_json() == {
        "status": "ok", "service": "Lab05 SQL Injection Local Lab"
    }


def test_unknown_route_uses_safe_not_found_page(shared_client):
    response = shared_client.get("/route-that-does-not-exist")
    assert response.status_code == 404
    assert b"Traceback" not in response.data


def test_oversized_request_is_rejected(shared_client):
    response = shared_client.post(
        "/secure/login",
        data={"username": "a" * 70_000, "password": "x"},
    )
    assert response.status_code == 413

