from config import QUOTE_INPUT, SEARCH_EXPANDED_INPUT


def test_quote_search_records_handled_syntax_error(shared_client):
    response = shared_client.get("/vulnerable/search", query_string={"keyword": QUOTE_INPUT})
    assert response.status_code == 200
    assert response.headers["X-Lab-Decision"] == "query_error"
    assert response.headers["X-Lab-Error-Category"] == "sql_syntax_error"


def test_fixed_expanded_search_returns_more_rows_than_expected(shared_client):
    response = shared_client.get("/vulnerable/search", query_string={"keyword": SEARCH_EXPANDED_INPUT})
    trace = shared_client.get(f'/api/trace/{response.headers["X-Lab-Trace-ID"]}').get_json()
    result = trace["result_set_inspector"]
    assert response.headers["X-Lab-Decision"] == "unexpected_results"
    assert result["rows_returned"] > result["rows_expected"]
    assert result["unexpected_data"] is True


def test_expanded_search_stays_inside_products_and_is_read_only(shared_client):
    response = shared_client.get("/vulnerable/search", query_string={"keyword": SEARCH_EXPANDED_INPUT})
    trace = shared_client.get(f'/api/trace/{response.headers["X-Lab-Trace-ID"]}').get_json()
    assert trace["database_inspector"]["table"] == "products"
    assert trace["result_set_inspector"]["other_table_accessed"] is False
    assert trace["result_set_inspector"]["database_modified"] is False
    assert trace["execution_inspector"]["rows_changed"] == 0


def test_unapproved_sql_shaped_search_is_rejected(shared_client):
    response = shared_client.get(
        "/vulnerable/search", query_string={"keyword": "mouse' OR 'x'='x"}
    )
    assert response.status_code == 400
    assert response.headers["X-Lab-Decision"] == "validation_failed"


def test_vulnerable_search_trace_marks_input_as_syntax_capable(shared_client):
    response = shared_client.get("/vulnerable/search", query_string={"keyword": "Mouse"})
    query = shared_client.get(f'/api/trace/{response.headers["X-Lab-Trace-ID"]}').get_json()["query_inspector"]
    assert query["construction_method"] == "string_concatenation"
    assert query["input_interpreted_as"] == "syntax-capable text"

