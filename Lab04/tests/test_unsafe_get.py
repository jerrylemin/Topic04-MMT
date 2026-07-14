from database import query_one


def test_state_change_via_get_is_not_exposed(app, logged_in):
    assert logged_in.get("/vulnerable/change-email-get?email=get_attack@lab.local").status_code == 404
    assert logged_in.get("/secure/change-email?email=must_not_change@lab.local").status_code == 200
    with app.app_context():
        assert query_one("SELECT email FROM users WHERE id = 10")["email"] == "victim_old@lab.local"
