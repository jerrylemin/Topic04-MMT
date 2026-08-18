def test_home_health_and_anonymous_protection(client):
    assert client.get("/").status_code == 200
    assert client.get("/health").get_json()["status"] == "ok"
    assert client.get("/dashboard").status_code == 302


def test_request_size_is_limited(client):
    response = client.post("/login", data={"username": "x" * 70_000, "password": "x"})
    assert response.status_code == 413

