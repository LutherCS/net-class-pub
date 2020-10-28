#!/usr/bin/env python3
"""
Testing the pinger
"""


import mock
import pytest
from freezegun import freeze_time
from src.projects.pinger.pinger import *


@pytest.mark.skip
@pytest.mark.parametrize(
    "packet_bytes, calculated_checksum",
    [
        (b"\x08\x00\x00\x00\x00\x01\x00\x01\x91\x9b(\x19'\xe6\xd7A", 16161),
        (b"\x08\x00\x00\x00\x07E\x01\xae\x00\x00\x00\x00\x9bx\xe9\xc1", 27090),
    ],
)
def test_checksum(packet_bytes, calculated_checksum):
    """Calculate checksum"""
    assert checksum(packet_bytes) == calculated_checksum


@pytest.mark.skip
@freeze_time("1861-09-01")
@pytest.mark.parametrize(
    "req_id, seq_num, packet_bytes",
    [
        (1, 1, b"\x08\x00r\xc3\x00\x01\x00\x01\x00\x00\x00\x00\x9bx\xe9\xc1"),
        (1861, 430, b"\x08\x00i\xd2\x07E\x01\xae\x00\x00\x00\x00\x9bx\xe9\xc1"),
    ],
)
def test_format_request(req_id, seq_num, packet_bytes):
    """format request"""
    assert format_request(req_id, seq_num) == packet_bytes


# 45 00 00 24 ea 35 00 00  80 01 bb 9d 5d b8 d8 22
# c0 a8 9e 82 00 00 c6 60  ab e1 00 03 6e fc 16 96
# 30 e6 d7 41


def test_parse_reply_type_error():
    """Parse reply, check the type"""
    with mock.patch("socket.socket") as sock:
        sock.recvfrom.return_value = (
            b'E\x00\x00$\xea5\x00\x00\x80\x01\xbb\x9d]\xb8\xd8"\xc0\xa8\x9e\x82'
            + b"\x01\x00\xc6`\xab\xe1\x00\x03n\xfc\x16\x960\xe6\xd7A",
            ("127.0.0.1", 0),
        )
        sock.fileno.return_value = 430
        with pytest.raises(ValueError) as ve:
            parse_reply(sock, 44001, 1, "127.0.0.1")
        assert str(ve.value) == "Incorrect type. Expected 0, received 1"


def test_parse_reply_code_error():
    """Parse reply, check the code"""
    with mock.patch("socket.socket") as sock:
        sock.recvfrom.return_value = (
            b'E\x00\x00$\xea5\x00\x00\x80\x01\xbb\x9d]\xb8\xd8"\xc0\xa8\x9e\x82'
            + b"\x00\x01\xc6`\xab\xe1\x00\x03n\xfc\x16\x960\xe6\xd7A",
            ("127.0.0.1", 0),
        )
        sock.fileno.return_value = 430
        with pytest.raises(ValueError) as ve:
            parse_reply(sock, 44001, 1, "127.0.0.1")
        assert str(ve.value) == "Incorrect code. Expected 0, received 1"


def test_parse_reply_checksum_error():
    """Parse reply, check the checksum"""
    with mock.patch("socket.socket") as sock:
        sock.recvfrom.return_value = (
            b'E\x00\x00$\xea5\x00\x00\x80\x01\xbb\x9d]\xb8\xd8"\xc0\xa8\x9e\x82'
            + b"\x00\x00\x16`\xab\xe1\x00\x03n\xfc\x16\x960\xe6\xd7A",
            ("127.0.0.1", 0),
        )
        sock.fileno.return_value = 430
        with pytest.raises(ValueError) as ve:
            parse_reply(sock, 44001, 1, "127.0.0.1")
        assert str(ve.value) == "Incorrect checksum. Expected 50784, received 5728"


def test_parse_reply_id_error():
    """Parse reply, check the id"""
    with mock.patch("socket.socket") as sock:
        sock.recvfrom.return_value = (
            b'E\x00\x00$\xea5\x00\x00\x80\x01\xbb\x9d]\xb8\xd8"\xc0\xa8\x9e\x82'
            + b"\x00\x00\xc6`\xab\xe1\x00\x03n\xfc\x16\x960\xe6\xd7A",
            ("127.0.0.1", 0),
        )
        sock.fileno.return_value = 430
        with pytest.raises(ValueError) as ve:
            parse_reply(sock, 43000, 1, "127.0.0.1")
        assert str(ve.value) == "Incorrect id. Expected 43000, received 44001"


def test_parse_reply_sender_error():
    """Parse reply, check the id"""
    with mock.patch("socket.socket") as sock:
        sock.recvfrom.return_value = (
            b'E\x00\x00$\xea5\x00\x00\x80\x01\xbb\x9d]\xb8\xd8"\xc0\xa8\x9e\x82'
            + b"\x00\x00\xc6`\xab\xe1\x00\x03n\xfc\x16\x960\xe6\xd7A",
            ("127.0.0.2", 0),
        )
        sock.fileno.return_value = 430
        with pytest.raises(ValueError) as ve:
            parse_reply(sock, 44001, 1, "127.0.0.1")
        assert (
            str(ve.value) == "Wrong sender. Expected 127.0.0.1, received from 127.0.0.2"
        )


@freeze_time("2020-11-03")
@pytest.mark.parametrize(
    "sock_data, req_id, result",
    [
        (
            (
                b'E\x00\x00$\xea5\x00\x00\x80\x01\xbb\x9d]\xb8\xd8"\xc0\xa8\x9e\x82'
                + b"\x00\x00\xc6`\xab\xe1\x00\x03n\xfc\x16\x960\xe6\xd7A",
                ("127.0.0.1", 0),
            ),
            44001,
            (
                "127.0.0.1",
                36,
                514855640.8429146,
                128,
                3,
            ),
        ),
        (
            (
                b'E\x00\x00$\xf8K\x00\x00\x80\x01\xad\x87]\xb8\xd8"\xc0\xa8\x9e\x82'
                + b"\x00\x00C\x93\xb6:\x00\x03\xf8N\x01\xb84\xe6\xd7A",
                ("93.184.216.34", 0),
            ),
            46650,
            (
                "93.184.216.34",
                36,
                510623979.55513,
                128,
                3,
            ),
        ),
        (
            (
                b"E\x00\x00$\xfa(\x00\x00\x80\x01\x1a\xa7\xc4\xd8\x02\x06\xc0\xa8\x9e\x82"
                + b"\x00\x00\xe6\xa8\xb7G\x00\x01\xe7\xbdm(5\xe6\xd7A",
                ("196.216.2.6", 0),
            ),
            46919,
            (
                "196.216.2.6",
                36,
                510174285.2842808,
                128,
                1,
            ),
        ),
    ],
)
def test_parse_reply(sock_data, req_id, result):
    """Parse reply, check the id"""
    with mock.patch("socket.socket") as sock:
        sock.recvfrom.return_value = sock_data
        sock.fileno.return_value = 0
        assert parse_reply(sock, req_id, 1, sock_data[1][0]) == result


if __name__ == "__main__":
    pytest.main(["test_pinger.py"])
