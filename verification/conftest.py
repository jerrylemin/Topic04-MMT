from __future__ import annotations

from urllib.parse import urlsplit

import pytest
import requests


LOCAL_HOSTS = {"127.0.0.1", "localhost"}


def local_url(port: int, path: str = "") -> str:
    url = f"http://127.0.0.1:{port}{path}"
    assert urlsplit(url).hostname in LOCAL_HOSTS
    return url


def require_service(port: int, path: str = "/health") -> None:
    try:
        response = requests.get(local_url(port, path), timeout=5)
    except requests.RequestException as exc:
        pytest.fail(f"Local service on port {port} is unavailable: {exc}")
    assert response.status_code == 200, (port, response.status_code, response.text[:200])

