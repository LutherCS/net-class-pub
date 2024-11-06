#!/usr/bin/env python3
"""
Testing the traceroute

@author: Roman Yasinovskyy
@version: 2024.11
"""

import importlib
import pathlib
import sys

import mock
import pytest
from freezegun import freeze_time

try:
    importlib.util.find_spec(".".join(pathlib.Path(__file__).parts[-3:-1]), "src")
except ModuleNotFoundError:
    sys.path.append(f"{pathlib.Path(__file__).parents[3]}/")
finally:
    from src.projects.traceroute.traceroute import (
        checksum,
        format_request,
        parse_reply,
        receive_reply,
        send_request,
    )


def test_checksum():
    """Calculate checksum"""
    assert checksum(b"\x08\x00,i\x00\x01\x00\x01VOTE!") == 0
    assert (
        checksum(
            b"\x0b\x00\xf4\xff\x00\x00\x00\x00"
            + b'E\x00\x00!\xda%\x00\x00\x01\x01\xe7\xc3\xc0\xa8\x01p]\xb8\xd8"'
            + b"\x08\x00\xd6\xa5U\xc4\x00\x01VOTE!"
        )
        == 0
    )


def test_format_request():
    """Format request"""
    assert format_request(1, 1) == b"\x08\x00,i\x00\x01\x00\x01VOTE!"


@freeze_time("2024-11-5")
def test_send_request():
    """Send request"""
    with mock.patch("socket.socket") as sock:
        assert (
            send_request(sock, b"\x08\x00,i\x00\x01\x00\x01VOTE!", "127.0.0.1", 128)
            == 1730764800.0
        )


@freeze_time("2024-11-5")
def test_receive_reply():
    """Receive reply"""
    with mock.patch("socket.socket") as sock:
        sock.recvfrom.return_value = (
            b"\x08\x00,i\x00\x01\x00\x01VOTE!",
            ("127.0.0.1", 0),
        )
        assert receive_reply(sock) == (
            b"\x08\x00,i\x00\x01\x00\x01VOTE!",
            ("127.0.0.1", 0),
            1730764800.0,
        )


def test_parse_reply_type_error():
    """Parse reply, check the type"""
    with pytest.raises(ValueError) as val_err:
        parse_reply(b"\x00" * 20 + b"\x01\x00,i\x00\x01\x00\x01VOTE!")
    assert str(val_err.value) == "Incorrect type 1 received instead of 0, 3, 8, 11"


def test_parse_reply_code_error():
    """Parse reply, check the code"""
    with pytest.raises(ValueError) as ve:
        parse_reply(b"\x00" * 20 + b"\x00\x01,i\x00\x01\x00\x01VOTE!")
    assert str(ve.value) == "Incorrect code 1 received with type 0"


def test_parse_reply_checksum_error():
    """Parse reply, check the checksum"""
    with pytest.raises(ValueError) as ve:
        parse_reply(b"\x00" * 20 + b"\x00\x00i,\x00\x01\x00\x01VOTE!")
    assert str(ve.value) == "Incorrect checksum 692c received instead of cb3c"


if __name__ == "__main__":
    pytest.main(["-v", __file__])
