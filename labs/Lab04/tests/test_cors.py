def test_victim_does_not_enable_wildcard_cors(client):
    response = client.get("/health", headers={"Origin": "http://127.0.0.1:9004"})
    assert response.headers.get("Access-Control-Allow-Origin") != "*"
    assert response.headers.get("Access-Control-Allow-Credentials") != "true"
