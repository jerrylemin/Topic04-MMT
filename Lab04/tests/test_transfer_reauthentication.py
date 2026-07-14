from database import query_all, query_one


def _token(client):
    with client.session_transaction() as sess:
        return sess["csrf_token"]


def test_secure_transfer_requires_reauthentication_and_commits_both_balances(app, logged_in):
    data = {"csrf_token": _token(logged_in), "receiver_id": "11", "amount": "100000"}
    assert logged_in.post("/secure/transfer", data=data, headers={"Origin": "http://127.0.0.1:5004"}).status_code == 403

    data["current_password"] = "Victim123!"
    response = logged_in.post("/secure/transfer", data=data, headers={"Origin": "http://127.0.0.1:5004"})
    assert response.status_code == 200
    with app.app_context():
        assert query_one("SELECT demo_balance FROM users WHERE id = 10")["demo_balance"] == 900_000
        assert query_one("SELECT demo_balance FROM users WHERE id = 11")["demo_balance"] == 600_000
        assert len(query_all("SELECT * FROM demo_transfers")) == 1


def test_transfer_rejects_non_positive_and_excessive_amounts(app, logged_in):
    for amount in ("-1", "0", "1000001"):
        response = logged_in.post(
            "/secure/transfer",
            data={"csrf_token": _token(logged_in), "receiver_id": "11", "amount": amount,
                  "current_password": "Victim123!"},
            headers={"Origin": "http://127.0.0.1:5004"},
        )
        assert response.status_code == 400
    with app.app_context():
        assert query_one("SELECT demo_balance FROM users WHERE id = 10")["demo_balance"] == 1_000_000

