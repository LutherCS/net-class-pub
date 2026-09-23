"""
Server testing

@author: Roman Yasinovskyy
@version: 2026.9
"""

import pathlib
import sys
from importlib.util import find_spec
from unittest import mock

import pytest
from freezegun import freeze_time

try:
    find_spec(".".join(pathlib.Path(__file__).parts[-3:-1]), "src")
except ModuleNotFoundError:
    sys.path.append(f"{pathlib.Path(__file__).parents[3]}/")
finally:
    from src.projects.webserver.server import format_response, parse_request


@pytest.mark.parametrize(
    "data, result",
    [
        (
            b"GET /test.txt HTTP/1.1\r\nHost: 127.0.0.1:4380\r\nUser-Agent: curl/8.5.0\r\nAccept: */*\r\n\r\n",
            {
                "Method": "GET",
                "Url": "/test.txt",
                "Version": "HTTP/1.1",
                "Host": "127.0.0.1:4380",
                "User-Agent": "curl/8.5.0",
                "Accept": "*/*",
            },
        ),
        (
            b"POST /test.txt HTTP/1.1\r\nHost: 127.0.0.1:4380\r\nUser-Agent: curl/8.5.0\r\nAccept: */*\r\nContent-Length: 5\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nn=430",
            {
                "Method": "POST",
                "Url": "/test.txt",
                "Version": "HTTP/1.1",
                "Host": "127.0.0.1:4380",
                "User-Agent": "curl/8.5.0",
                "Accept": "*/*",
                "Content-Length": "5",
                "Content-Type": "application/x-www-form-urlencoded",
                "Body": "n=430",
            },
        ),
        (
            b"HEAD /test.txt HTTP/1.1\r\nHost: 127.0.0.1:4380\r\nUser-Agent: curl/8.5.0\r\nAccept: */*\r\n\r\n",
            {
                "Method": "HEAD",
                "Url": "/test.txt",
                "Version": "HTTP/1.1",
                "Host": "127.0.0.1:4380",
                "User-Agent": "curl/8.5.0",
                "Accept": "*/*",
            },
        ),
        (
            b"PUT /test.txt HTTP/1.1\r\nHost: 127.0.0.1:4380\r\nUser-Agent: curl/8.5.0\r\nAccept: */*\r\nContent-Length: 6\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nsecret",
            {
                "Method": "PUT",
                "Url": "/test.txt",
                "Version": "HTTP/1.1",
                "Host": "127.0.0.1:4380",
                "User-Agent": "curl/8.5.0",
                "Accept": "*/*",
                "Content-Length": "6",
                "Content-Type": "application/x-www-form-urlencoded",
                "Body": "secret",
            },
        ),
        (
            b"DELETE /test.txt HTTP/1.1\r\nHost: 127.0.0.1:4380\r\nUser-Agent: curl/8.5.0\r\nAccept: */*\r\n\r\n",
            {
                "Method": "DELETE",
                "Url": "/test.txt",
                "Version": "HTTP/1.1",
                "Host": "127.0.0.1:4380",
                "User-Agent": "curl/8.5.0",
                "Accept": "*/*",
            },
        ),
    ],
)
def test_parse_request_data(data, result):
    """Parse client request"""
    assert parse_request(data) == result


@pytest.mark.parametrize(
    "http_version, status_code, header, data, result",
    [
        (
            "HTTP/1.1",
            200,
            {
                "Content-Type": "text/plain; charset=utf-8",
                "Last-Modified": "2020-10-15 14:52:20.413406",
            },
            "Hello\n",
            b"HTTP/1.1 200 OK\r\nDate: 2026-09-21 21:09:26\r\nServer: CS430/2026\r\nContent-Type: text/plain; charset=utf-8\r\nLast-Modified: 2020-10-15 14:52:20.413406\r\nContent-Length: 6\r\n\r\nHello\n",
        ),
        (
            "HTTP/1.1",
            204,
            None,
            None,
            b"HTTP/1.1 204 No Content\r\nDate: 2026-09-21 21:09:26\r\nServer: CS430/2026\r\n\r\n",
        ),
        (
            "HTTP/1.1",
            404,
            None,
            "<html><head></head><body><h1>File /test404.txt not found on our server</h1></body></html>",
            b"HTTP/1.1 404 Not Found\r\nDate: 2026-09-21 21:09:26\r\nServer: CS430/2026\r\nContent-Length: 89\r\n\r\n<html><head></head><body><h1>File /test404.txt not found on our server</h1></body></html>",
        ),
        (
            "HTTP/1.1",
            405,
            None,
            "<html><head></head><body><h1>Use GET to retrieve resources from this server</h1></body></html>",
            b"HTTP/1.1 405 Method Not Allowed\r\nDate: 2026-09-21 21:09:26\r\nServer: CS430/2026\r\nContent-Length: 94\r\n\r\n<html><head></head><body><h1>Use GET to retrieve resources from this server</h1></body></html>",
        ),
        (
            "HTTP/1.1",
            418,
            None,
            None,
            b"HTTP/1.1 418 I'm a teapot\r\nDate: 2026-09-21 21:09:26\r\nServer: CS430/2026\r\n\r\n",
        ),
        (
            "HTTP/1.1",
            501,
            None,
            None,
            b"HTTP/1.1 501 Not Implemented\r\nDate: 2026-09-21 21:09:26\r\nServer: CS430/2026\r\n\r\n",
        ),
        (
            "HTTP/1.1",
            505,
            None,
            None,
            b"HTTP/1.1 505 HTTP Version Not Supported\r\nDate: 2026-09-21 21:09:26\r\nServer: CS430/2026\r\n\r\n",
        ),
    ],
)
@freeze_time("2026-09-21 21:09:26")
def test_format_response_data(http_version, status_code, header, data, result):
    """Format server response"""
    assert format_response(http_version, status_code, header, data) == result


@pytest.mark.parametrize(
    "sock_data, result",
    [
        (
            b"GET / HTTP/1.1\r\nHost: 127.0.0.1:80\r\nUser-Agent: curl\r\nAccept: */*\r\n\r\n",
            {
                "Method": "GET",
                "Url": "/",
                "Version": "HTTP/1.1",
                "Host": "127.0.0.1:80",
                "User-Agent": "curl",
                "Accept": "*/*",
            },
        ),
        (
            b"POST / HTTP/1.1\r\nHost: 127.0.0.1:4380\r\nUser-Agent: curl\r\nAccept: */*\r\nContent-Length: 5\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nn=430",
            {
                "Method": "POST",
                "Url": "/",
                "Version": "HTTP/1.1",
                "Host": "127.0.0.1:4380",
                "User-Agent": "curl",
                "Accept": "*/*",
                "Content-Length": "5",
                "Content-Type": "application/x-www-form-urlencoded",
                "Body": "n=430",
            },
        ),
    ],
)
def test_parse_request(sock_data, result):
    """Parse client request"""
    with mock.patch("socket.socket") as sock:
        sock.recvfrom.return_value = sock_data
        sock.fileno.return_value = 0
        assert parse_request(sock_data) == result


if __name__ == "__main__":
    pytest.main(["-v", __file__])
