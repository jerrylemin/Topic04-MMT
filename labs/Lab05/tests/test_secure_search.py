import pytest

from config import QUOTE_INPUT, SEARCH_EXPANDED_INPUT


@pytest.mark.parametrize("keyword", [QUOTE_INPUT, SEARCH_EXPANDED_INPUT])
def test_fixed_sql_shaped_inputs_remain_data_in_secure_search(shared_client, keyword):
    response = shared_client.get("/secure/search", query_string={"keyword": keyword})
    assert response.status_code == 200
    assert response.headers["X-Lab-Prepared"] == "true"
    assert response.headers["X-Lab-Error-Category"] == "none"
    assert response.headers["X-Lab-Result-Count"] == "0"


def test_secure_search_uses_like_placeholder_and_bound_value(shared_client):
    response = shared_client.get("/secure/search", query_string={"keyword": "Mouse"})
    query = shared_client.get(f'/api/trace/{response.headers["X-Lab-Trace-ID"]}').get_json()["query_inspector"]
    assert "LIKE ?" in query["query_template"]
    assert query["placeholder_count"] == 1
    assert query["parameters_masked"] == ["[BOUND VALUE]"]


def test_secure_search_has_explicit_fifty_row_limit(shared_client):
    response = shared_client.get("/secure/search", query_string={"keyword": "a"})
    query = shared_client.get(f'/api/trace/{response.headers["X-Lab-Trace-ID"]}').get_json()["query_inspector"]
    assert "LIMIT 50" in query["query_template"]
    assert int(response.headers["X-Lab-Result-Count"]) <= 50


@pytest.mark.parametrize("keyword", ["", " ", "x" * 101])
def test_secure_search_validates_required_length(shared_client, keyword):
    response = shared_client.get("/secure/search", query_string={"keyword": keyword})
    assert response.status_code == 400
    assert response.headers["X-Lab-Decision"] == "validation_failed"


def test_secure_search_normalizes_repeated_spaces(shared_client):
    response = shared_client.get("/secure/search", query_string={"keyword": "  Wireless   Mouse  "})
    trace = shared_client.get(f'/api/trace/{response.headers["X-Lab-Trace-ID"]}').get_json()
    assert trace["input_inspector"]["normalized_input"] == "Wireless Mouse"

