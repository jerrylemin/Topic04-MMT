import pytest


@pytest.mark.parametrize("route", ["/vulnerable/search", "/secure/search"])
def test_usb_search_returns_only_matching_named_products(shared_client, route):
    response = shared_client.get(route, query_string={"keyword": "USB"})
    trace = shared_client.get(f'/api/trace/{response.headers["X-Lab-Trace-ID"]}').get_json()
    names = trace["result_set_inspector"]["result_names"]
    assert response.status_code == 200
    assert names
    assert all("usb" in name.lower() for name in names)


@pytest.mark.parametrize("route", ["/vulnerable/search", "/secure/search"])
def test_search_form_get_without_keyword_does_not_execute_query(shared_client, route):
    response = shared_client.get(route)
    assert response.status_code == 200
    assert "X-Lab-Trace-ID" not in response.headers


def test_normal_secure_and_vulnerable_search_agree_on_results(shared_client):
    vulnerable = shared_client.get("/vulnerable/search", query_string={"keyword": "USB"})
    secure = shared_client.get("/secure/search", query_string={"keyword": "USB"})
    assert vulnerable.headers["X-Lab-Result-Count"] == secure.headers["X-Lab-Result-Count"]

