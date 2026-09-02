"""
`intro server` testing

@authors: Roman Yasinovskyy
@version: 2026.9
"""

import importlib.util
import pathlib
import sys
from unittest import mock

import pytest

try:
    importlib.util.find_spec(".".join(pathlib.Path(__file__).parts[-3:-1]), "src")
except ModuleNotFoundError:
    sys.path.append(f"{pathlib.Path(__file__).parents[3]}/")
finally:
    from src.projects.hello.server import format_message, parse_data


@pytest.mark.parametrize(
    "message, data",
    [
        ("Toph", b"Hello, Toph"),
        ("The Child", b"Hello, The Child"),
        (
            "フンベルト・フォン・ジッキンゲン",
            b"Hello, \xe3\x83\x95\xe3\x83\xb3\xe3\x83\x99\xe3\x83\xab\xe3\x83\x88\xe3\x83\xbb\xe3\x83\x95\xe3\x82\xa9\xe3\x83\xb3\xe3\x83\xbb\xe3\x82\xb8\xe3\x83\x83\xe3\x82\xad\xe3\x83\xb3\xe3\x82\xb2\xe3\x83\xb3",
        ),
        (
            "Чорна вдова",
            b"Hello, \xd0\xa7\xd0\xbe\xd1\x80\xd0\xbd\xd0\xb0 \xd0\xb2\xd0\xb4\xd0\xbe\xd0\xb2\xd0\xb0",
        ),
    ],
)
def test_format_message(message, data):
    assert format_message(message) == data


@pytest.mark.parametrize(
    "data, message",
    [
        (b"Hello, my name is Toph", "Toph"),
        (b"Hello, my name is The Child", "The Child"),
        (
            b"Hello, my name is \xe3\x83\x95\xe3\x83\xb3\xe3\x83\x99\xe3\x83\xab\xe3\x83\x88\xe3\x83\xbb\xe3\x83\x95\xe3\x82\xa9\xe3\x83\xb3\xe3\x83\xbb\xe3\x82\xb8\xe3\x83\x83\xe3\x82\xad\xe3\x83\xb3\xe3\x82\xb2\xe3\x83\xb3",
            "フンベルト・フォン・ジッキンゲン",
        ),
        (
            b"Hello, my name is \xd0\xa7\xd0\xbe\xd1\x80\xd0\xbd\xd0\xb0 \xd0\xb2\xd0\xb4\xd0\xbe\xd0\xb2\xd0\xb0",
            "Чорна вдова",
        ),
    ],
)
def test_parse_data(data, message):
    assert parse_data(data) == message


@pytest.mark.parametrize(
    "sock_data, result",
    [
        (b"Hello, my name is Toph", "Toph"),
        (b"Hello, my name is The Child", "The Child"),
        (
            b"Hello, my name is \xe3\x83\x95\xe3\x83\xb3\xe3\x83\x99\xe3\x83\xab\xe3\x83\x88\xe3\x83\xbb\xe3\x83\x95\xe3\x82\xa9\xe3\x83\xb3\xe3\x83\xbb\xe3\x82\xb8\xe3\x83\x83\xe3\x82\xad\xe3\x83\xb3\xe3\x82\xb2\xe3\x83\xb3",
            "フンベルト・フォン・ジッキンゲン",
        ),
        (
            b"Hello, my name is \xd0\xa7\xd0\xbe\xd1\x80\xd0\xbd\xd0\xb0 \xd0\xb2\xd0\xb4\xd0\xbe\xd0\xb2\xd0\xb0",
            "Чорна вдова",
        ),
    ],
)
def test_parse_request(sock_data, result):
    """Parse client request"""
    with mock.patch("socket.socket") as sock:
        sock.recvfrom.return_value = sock_data
        sock.fileno.return_value = 0
        assert parse_data(sock_data) == result


if __name__ == "__main__":
    pytest.main(["-v", __file__])
