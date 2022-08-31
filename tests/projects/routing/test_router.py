#!/usr/bin/python3
"""
Testing Router
"""


import mock
import pytest
from src.projects.routing.udp_router import *

ROUTING_TABLE = {
    "127.0.0.2": [1, "127.0.0.2"],
    "127.0.0.3": [3, "127.0.0.3"],
    "127.0.0.4": [7, "127.0.0.4"],
}


@mock.patch("src.projects.routing.udp_router.THIS_HOST", "127.0.0.1")
def test_read_config_file():
    """Read config file"""
    s, d = read_config_file("data/projects/routing/network_simple.txt")
    assert s == set(ROUTING_TABLE.keys())
    assert d == ROUTING_TABLE


def test_read_config_file_error():
    """Read config file"""
    with pytest.raises(FileNotFoundError) as fnfe:
        read_config_file("data/projects/routing/wrong_file.txt")
    assert (
        str(fnfe.value)
        == "Could not find the specified configuration file data/projects/routing/wrong_file.txt"
    )


def test_format_update():
    """Format UPDATE message"""
    assert (
        format_update(ROUTING_TABLE)
        == b"\x00\x7f\x00\x00\x02\x01\x7f\x00\x00\x03\x03\x7f\x00\x00\x04\x07"
    )


@pytest.mark.parametrize(
    "message, addr, status",
    [
        (b"\x00\x7f\x00\x00\x01\x07\x7f\x00\x00\x03\x02", "127.0.0.4", False),
        (b"\x00\x7f\x00\x00\x01\x01\x7f\x00\x00\x03\x01", "127.0.0.2", True),
    ],
)
@mock.patch("src.projects.routing.udp_router.THIS_HOST", "127.0.0.1")
def test_parse_update(message, addr, status):
    """Parse UPDATE message"""
    assert parse_update(message, addr, ROUTING_TABLE) == status


@pytest.mark.parametrize(
    "msg_txt, src, dst, msg_bytes",
    [
        (
            "Focal Fossa",
            "127.0.0.1",
            "127.0.0.2",
            b"\x01\x7f\x00\x00\x01\x7f\x00\x00\x02Focal\x20Fossa",
        ),
        (
            "Groovy Gorilla",
            "127.0.0.1",
            "127.0.0.4",
            b"\x01\x7f\x00\x00\x01\x7f\x00\x00\x04Groovy\x20Gorilla",
        ),
    ],
)
def test_format_hello(msg_txt, src, dst, msg_bytes):
    """Format HELLO message"""
    assert format_hello(msg_txt, src, dst) == msg_bytes


@pytest.mark.parametrize(
    "message, result",
    [
        (
            b"\x01\x7f\x00\x00\x03\x7f\x00\x00\x01Focal\x20Fossa",
            "Received Focal Fossa from 127.0.0.3",
        ),
        (
            b"\x01\x7f\x00\x00\x04\x7f\x00\x00\x02Groovy\x20Gorilla",
            "Forwarded Groovy Gorilla to 127.0.0.2",
        ),
    ],
)
@mock.patch("src.projects.routing.udp_router.THIS_HOST", "127.0.0.1")
def test_parse_hello(message, result):
    """Parse HELLO message"""
    assert parse_hello(message, ROUTING_TABLE) == result


if __name__ == "__main__":
    pytest.main(["test_router.py"])
