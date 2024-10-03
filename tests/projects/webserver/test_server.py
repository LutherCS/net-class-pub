#!/usr/bin/env python3
"""
`web server` testing

@authors: Roman Yasinovskyy
@version: 2024.10
"""

import importlib
import pathlib
import sys

import pytest
from freezegun import freeze_time

try:
    importlib.util.find_spec(".".join(pathlib.Path(__file__).parts[-3:-1]), "src")
except ModuleNotFoundError:
    sys.path.append(f"{pathlib.Path(__file__).parents[3]}/")
finally:
    from src.projects.webserver.server import format_response, parse_request


@pytest.mark.parametrize(
    "data, result",
    [
        (
            b"GET /test.txt HTTP/1.1\r\nHost: 127.0.0.2:43080\r\nUser-Agent: curl/8.5.0\r\nAccept: */*\r\n\r\n",
            {
                "method": "GET",
                "url": "/test.txt",
                "version": "HTTP/1.1",
                "Host": "127.0.0.2:43080",
                "User-Agent": "curl/8.5.0",
                "Accept": "*/*",
            },
        ),
        (
            b"GET /test404.txt HTTP/1.1\r\nHost: 127.0.0.2:43080\r\nUser-Agent: curl/8.5.0\r\nAccept: */*\r\n\r\n",
            {
                "method": "GET",
                "url": "/test404.txt",
                "version": "HTTP/1.1",
                "Host": "127.0.0.2:43080",
                "User-Agent": "curl/8.5.0",
                "Accept": "*/*",
            },
        ),
        (
            b"POST /test405.txt HTTP/1.1\r\nHost: 127.0.0.2:43080\r\nUser-Agent: curl/8.5.0\r\nAccept: */*\r\n\r\n",
            {
                "method": "POST",
                "url": "/test405.txt",
                "version": "HTTP/1.1",
                "Host": "127.0.0.2:43080",
                "User-Agent": "curl/8.5.0",
                "Accept": "*/*",
            },
        ),
        (
            b"HEAD /test501.txt HTTP/1.1\r\nHost: 127.0.0.2:43080\r\nUser-Agent: curl/8.5.0\r\nAccept: */*\r\n\r\n",
            {
                "method": "HEAD",
                "url": "/test501.txt",
                "version": "HTTP/1.1",
                "Host": "127.0.0.2:43080",
                "User-Agent": "curl/8.5.0",
                "Accept": "*/*",
            },
        ),
    ],
)
def test_parse_request(data, result):
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
            b"HTTP/1.1 200 OK\r\nDate: 2024-10-02 02:10:24\r\nServer: CS430/2024\r\nContent-Type: text/plain; charset=utf-8\r\nLast-Modified: 2020-10-15 14:52:20.413406\r\nContent-Length: 6\r\n\r\nHello\n",
        ),
        (
            "HTTP/1.1",
            404,
            None,
            "<html><head></head><body><h1>File /test404.txt not found on our server</h1></body></html>",
            b"HTTP/1.1 404 Not Found\r\nDate: 2024-10-02 02:10:24\r\nServer: CS430/2024\r\nContent-Length: 89\r\n\r\n<html><head></head><body><h1>File /test404.txt not found on our server</h1></body></html>",
        ),
        (
            "HTTP/1.1",
            405,
            None,
            "<html><head></head><body><h1>Use GET to retrieve resources from this server</h1></body></html>",
            b"HTTP/1.1 405 Method Not Allowed\r\nDate: 2024-10-02 02:10:24\r\nServer: CS430/2024\r\nContent-Length: 94\r\n\r\n<html><head></head><body><h1>Use GET to retrieve resources from this server</h1></body></html>",
        ),
        (
            "HTTP/1.1",
            501,
            None,
            "",
            b"HTTP/1.1 501 Not Implemented\r\nDate: 2024-10-02 02:10:24\r\nServer: CS430/2024\r\n\r\n",
        ),
    ],
)
@freeze_time("2024-10-02 02:10:24")
def test_format_response(http_version, status_code, header, data, result):
    """Format server response"""
    assert format_response(http_version, status_code, header, data) == result


if __name__ == "__main__":
    pytest.main(["-v", __file__])
