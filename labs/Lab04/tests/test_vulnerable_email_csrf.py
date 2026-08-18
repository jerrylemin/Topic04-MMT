from database import query_one


def test_vulnerable_email_accepts_cross_origin_post_without_token(app, logged_in):
    response = logged_in.post(
        "/vulnerable/change-email",
        data={"email": "attacker_set@lab.local"},
        headers={"Origin": "http://127.0.0.1:9004"},
    )
    assert response.status_code == 200
    with app.app_context():
        assert query_one("SELECT email FROM users WHERE id = ?", (10,))["email"] == "attacker_set@lab.local"
        log = query_one("SELECT * FROM audit_logs WHERE action = ? ORDER BY id DESC", ("vulnerable_email_changed",))
        assert log["decision"] == "allowed"
        assert log["csrf_token_status"] == "not_required"
