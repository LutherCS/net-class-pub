"""
Server testing

@author: Roman Yasinovskyy
@version: 2026.9
"""

import subprocess
from datetime import datetime
from http.client import HTTPConnection

import pytest
import requests

BASE_URL = "http://localhost:4380"


def setup_module(module):
    module.http_server = subprocess.Popen(["python3", "src/projects/webserver/server.py"])
    try:
        module.http_server.wait(timeout=1)
    except subprocess.TimeoutExpired:
        pass


def teardown_module(module):
    module.http_server.terminate()


@pytest.mark.parametrize(
    "resource, method, http_ver, expected_code",
    [
        ("test26.txt", "GET", "1.1", 200),
        ("test26.txt", "DELETE", "1.1", 204),
        ("test.txt", "GET", "1.1", 301),
        ("test404.txt", "GET", "1.1", 404),
        ("test26.txt", "HEAD", "1.1", 405),
        ("test26.txt", "POST", "1.1", 418),
        ("test26.txt", "PUT", "1.1", 501),
        ("test26.txt", "GET", "1.0", 505),
    ],
)
def test_response_status(resource, method, http_ver, expected_code):
    """Verify server response"""
    HTTPConnection._http_vsn_str = f"HTTP/{http_ver}"
    match method:
        case "POST":
            response = requests.post(f"{BASE_URL}/{resource}")
        case "PUT":
            response = requests.put(f"{BASE_URL}/{resource}")
        case "HEAD":
            response = requests.head(f"{BASE_URL}/{resource}")
        case "DELETE":
            response = requests.delete(f"{BASE_URL}/{resource}")
        case _:
            response = requests.get(f"{BASE_URL}/{resource}", allow_redirects=False)
    assert response.status_code == expected_code
    HTTPConnection._http_vsn_str = "HTTP/1.1"


@pytest.mark.parametrize(
    "resource, expected_server_version",
    [
        ("test.txt", "CS430/2026"),
        ("alice.txt", "CS430/2026"),
    ],
)
def test_response_server(resource, expected_server_version):
    response = requests.get(f"{BASE_URL}/{resource}")
    assert response.headers.get("Server") == expected_server_version


@pytest.mark.parametrize(
    "resource, expected_content_type",
    [
        ("test.txt", "text/plain"),
        ("alice.txt", "text/plain"),
    ],
)
def test_response_content_type(resource, expected_content_type):
    response = requests.get(f"{BASE_URL}/{resource}")
    content_type = response.headers.get("Content-Type", "")
    assert content_type.startswith(expected_content_type), content_type


@pytest.mark.parametrize(
    "resource, expected_content_length",
    [
        ("test.txt", 6),
        ("alice.txt", 148545),
    ],
)
def test_response_content_length(resource, expected_content_length):
    response = requests.get(f"{BASE_URL}/{resource}")
    assert int(response.headers.get("Content-Length", "")) == expected_content_length


@pytest.mark.parametrize(
    "resource, expected_content_date",
    [
        ("test.txt", "2024-10-02 19:11:36"),
        ("alice.txt", "2020-10-15 14:21:49"),
    ],
)
def test_response_content_date(resource, expected_content_date):
    response = requests.get(f"{BASE_URL}/{resource}")
    last_mod = datetime.fromisoformat(response.headers.get("Last-Modified", ""))
    assert last_mod.strftime("%Y-%m-%d %H:%M:%S") == expected_content_date


if __name__ == "__main__":
    pytest.main(["-v", __file__])
