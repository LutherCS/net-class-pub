#!/usr/bin/python3
"""
Router testing using UDP sockets

@author: Roman Yasinovskyy
@version: 2022.12
"""


import importlib
import pathlib
import sys

import mock
import pytest

try:
    importlib.util.find_spec(".".join(pathlib.Path(__file__).parts[-3:-1]), "src")
except ModuleNotFoundError:
    sys.path.append(f"{pathlib.Path(__file__).parents[3]}/")
finally:
    from src.projects.routing.udp_router import (
        format_hello,
        format_update,
        parse_hello,
        parse_update,
        read_config_file,
    )


@pytest.fixture(name="routing_table")
def fixture_routing_table():
    return {
        "127.0.0.2": [1, "127.0.0.2"],
        "127.0.0.3": [3, "127.0.0.3"],
        "127.0.0.4": [7, "127.0.0.4"],
    }


@mock.patch("src.projects.routing.udp_router.THIS_HOST", "127.0.0.1")
def test_read_config_file(routing_table):
    """Read config file"""
    s, d = read_config_file("data/projects/routing/network_simple.txt")
    assert s == set(routing_table.keys())
    assert d == routing_table


def test_read_config_file_error():
    """Read config file"""
    with pytest.raises(FileNotFoundError) as fnf_err:
        read_config_file("data/projects/routing/wrong_file.txt")
    assert (
        str(fnf_err.value)
        == "Could not find the specified configuration file data/projects/routing/wrong_file.txt"
    )


def test_format_update(routing_table):
    """Format UPDATE message"""
    assert (
        format_update(routing_table)
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
def test_parse_update(routing_table, message, addr, status):
    """Parse UPDATE message"""
    assert parse_update(message, addr, routing_table) == status


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
def test_parse_hello(routing_table, message, result):
    """Parse HELLO message"""
    assert parse_hello(message, routing_table) == result


if __name__ == "__main__":
    pytest.main(["-v", __file__])
