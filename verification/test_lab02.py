from __future__ import annotations

import requests

from conftest import local_url, require_service


BASE = local_url(5002)
JSON = {"Accept": "application/json"}


def setup_module():
    require_service(5002)


def post(path: str, mode: str, name: str, origin: str = BASE):
    return requests.post(
        BASE + path,
        data={"mode": mode, "name": name},
        headers={**JSON, "Origin": origin},
        timeout=15,
    )


def test_loopback_origin_matrix_and_host_origin_consistency():
    assert post("/submit", "vulnerable_asan", "Le Minh").status_code == 200
    assert requests.post(
        "http://localhost:5002/submit",
        data={"mode": "vulnerable_asan", "name": "Le Minh"},
        headers={**JSON, "Origin": "http://localhost:5002"},
        timeout=15,
    ).status_code == 200
    assert post("/submit", "vulnerable_asan", "Le Minh", "http://localhost:5002").status_code == 403
    assert post("/submit", "vulnerable_asan", "Le Minh", "https://example.com").status_code == 403


def test_native_boundary_and_overflow_evidence_without_server_crash():
    for length in (31, 32):
        response = post("/submit", "vulnerable_asan", "A" * length)
        assert response.status_code == 200
    overflow = post("/submit", "vulnerable_asan", "A" * 64)
    body = overflow.json()
    assert body["native_result"]["asan"]["detected"] is True
    assert body["native_result"]["crash_detected"] is True
    assert requests.get(BASE + "/health", timeout=5).status_code == 200


def test_secure_native_variants_reject_oversized_input():
    for path, mode in (
        ("/secure/length/submit", "secure_length"),
        ("/secure/snprintf/submit", "secure_snprintf"),
    ):
        result = post(path, mode, "A" * 64).json()["native_result"]
        assert result["crash_detected"] is False
        assert result["asan"]["detected"] is False
        assert result["exit_code"] != 0

