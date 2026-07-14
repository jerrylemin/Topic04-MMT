from __future__ import annotations


def test_home_is_available(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Cookie Poisoning" in response.get_data(as_text=True)


def test_health_is_local_lab_status(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"
    assert response.get_json()["host"] == "127.0.0.1"
    assert response.get_json()["port"] == 5006


def test_default_runtime_config_supports_signed_and_encrypted_flows(tmp_path, monkeypatch):
    """Production defaults must not rely on test-only key injection."""
    from app import create_app

    monkeypatch.setenv("LAB06_DATABASE", str(tmp_path / "runtime.sqlite3"))
    application = create_app({"TESTING": True, "SERVER_NAME": "127.0.0.1:5006"})
    runtime_client = application.test_client()

    signed_login = runtime_client.post(
        "/login",
        data={"username": "admin_lab", "password": "AdminLab123!", "mode": "signed"},
    )
    encrypted_demo = runtime_client.get("/secure/encrypted-demo")

    assert signed_login.status_code == 302
    assert encrypted_demo.status_code == 200


def test_security_headers_are_present(client):
    response = client.get("/")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
    assert "default-src 'self'" in response.headers["Content-Security-Policy"]
    assert "unsafe-eval" not in response.headers["Content-Security-Policy"]
