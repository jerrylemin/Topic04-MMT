import pytest


@pytest.mark.parametrize("route,request_kwargs", [
    ("/secure/login", {"method": "post", "data": {"username": "student_a", "password": "StudentA123!"}}),
    ("/secure/search", {"method": "get", "query_string": {"keyword": "USB"}}),
    ("/secure/user", {"method": "get", "query_string": {"id": "1"}}),
])
def test_secure_database_flows_report_real_parameter_binding(shared_client, route, request_kwargs):
    method = request_kwargs.pop("method")
    response = getattr(shared_client, method)(route, **request_kwargs)
    trace = shared_client.get(f'/api/trace/{response.headers["X-Lab-Trace-ID"]}').get_json()
    assert trace["query_inspector"]["prepared"] is True
    assert trace["execution_inspector"]["prepared_statement"] is True
    assert trace["execution_inspector"]["parameters_bound"] >= 1
    assert trace["query_inspector"]["final_query_masked"] == trace["query_inspector"]["query_template"]


@pytest.mark.parametrize("route,request_kwargs", [
    ("/vulnerable/login", {"method": "post", "data": {"username": "student_a", "password": "StudentA123!"}}),
    ("/vulnerable/search", {"method": "get", "query_string": {"keyword": "USB"}}),
    ("/vulnerable/user", {"method": "get", "query_string": {"id": "1"}}),
])
def test_vulnerable_flows_are_honestly_labeled_as_concatenation(shared_client, route, request_kwargs):
    method = request_kwargs.pop("method")
    response = getattr(shared_client, method)(route, **request_kwargs)
    trace = shared_client.get(f'/api/trace/{response.headers["X-Lab-Trace-ID"]}').get_json()
    assert trace["query_inspector"]["construction_method"] == "string_concatenation"
    assert trace["execution_inspector"]["prepared_statement"] is False
    assert trace["execution_inspector"]["rows_changed"] == 0

