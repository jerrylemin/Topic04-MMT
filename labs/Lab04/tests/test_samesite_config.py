def test_cookie_security_configuration_and_set_cookie_header(app, client):
    assert app.config["SESSION_COOKIE_NAME"] == "lab04_session"
    assert app.config["SESSION_COOKIE_HTTPONLY"] is True
    assert app.config["SESSION_COOKIE_SAMESITE"] in {"Lax", "Strict"}
    response = client.post("/login", data={"username": "victim", "password": "Victim123!"})
    cookie = response.headers.get("Set-Cookie", "")
    assert "HttpOnly" in cookie
    assert f"SameSite={app.config['SESSION_COOKIE_SAMESITE']}" in cookie

