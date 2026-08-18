def test_victim_sends_required_security_headers(logged_in):
    response = logged_in.get("/secure/change-email")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
    assert "Permissions-Policy" in response.headers
    assert "Content-Security-Policy" in response.headers
    assert "unsafe-eval" not in response.headers["Content-Security-Policy"]
    assert response.headers["Cache-Control"] == "no-store"

