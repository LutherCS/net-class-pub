#!/usr/bin/env python3
"""
`nameserver` testing
`
@author: Roman Yasinovskyy
@version: 2022.11
"""


from random import seed
import importlib
import pathlib
import sys

import pytest

try:
    importlib.util.find_spec(".".join(pathlib.Path(__file__).parts[-3:-1]), "src")
except ModuleNotFoundError:
    sys.path.append(f"{pathlib.Path(__file__).parents[3]}/")
finally:
    from src.projects.nameserver.nameserver import (
        val_to_n_bytes,
        bytes_to_val,
        get_left_n_bits,
        get_right_n_bits,
        read_zone_file,
        parse_request,
        format_response,
    )

seed(430)


@pytest.fixture(scope="function", autouse=True, name="zone")
def zone_fixture():
    """Setting up"""
    return read_zone_file("data/projects/nameserver/zoo.zone")[1]


@pytest.mark.parametrize(
    "number, n, all_bytes", [(43043, 2, (168, 35)), (430430, 3, (6, 145, 94))]
)
def test_val_to_n_bytes(number, n, all_bytes):
    """Convert a value to n bytes"""
    assert val_to_n_bytes(number, n) == all_bytes


@pytest.mark.parametrize(
    "all_bytes, number", [([6, 145, 94], 430430), ([168, 35], 43043)]
)
def test_bytes_to_val(all_bytes, number):
    """Convert list of bytes to a value"""
    assert bytes_to_val(all_bytes) == number


@pytest.mark.parametrize(
    "all_bytes, n_bits, value", [([0xC0, 0x0C], 2, 3), ([128, 43], 2, 2)]
)
def test_get_left_n_bits(all_bytes, n_bits, value):
    """Get the first n bits from 2 bytes"""
    assert get_left_n_bits(all_bytes, n_bits) == value


@pytest.mark.parametrize(
    "all_bytes, n_bits, value", [([200, 100], 14, 2148), ([200, 100], 6, 36)]
)
def test_get_right_n_bits(all_bytes, n_bits, value):
    """Get the last n bits from 2 bytes"""
    assert get_right_n_bits(all_bytes, n_bits) == value


@pytest.mark.parametrize(
    "filename, exp_origin, records",
    [
        ("data/projects/nameserver/zoo.zone", "cs430.luther.edu", 25),
    ],
)
def test_read_zone_file(filename, exp_origin, records):
    """Read the zone file"""
    origin, zone = read_zone_file(filename)
    assert origin == exp_origin
    assert len(zone) == records


@pytest.mark.parametrize(
    "trans_id, qry_name, qry_type, qry_bytes, response",
    [
        (
            4783,
            "ant",
            1,
            b"\x03ant\x05cs430\x06luther\x03edu\x00\x00\x01\x00\x01",
            b"\x12\xaf\x81\x00\x00\x01\x00\x02\x00\x00\x00\x00\x03ant\x05cs430\x06luther\x03edu\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\x00\x0e\x10\x00\x04\xb9T\xe0Y\xc0\x0c\x00\x01\x00\x01\x00\x00\x0e\x10\x00\x04\xc7SC\x9e",
        ),
        (
            55933,
            "ant",
            28,
            b"\x03ant\x05cs430\x06luther\x03edu\x00\x00\x1c\x00\x01",
            b"\xda}\x81\x00\x00\x01\x00\x01\x00\x00\x00\x00\x03ant\x05cs430\x06luther\x03edu\x00\x00\x1c\x00\x01\xc0\x0c\x00\x1c\x00\x01\x00\x00\x0e\x10\x00\x10J\x9ap\xec:\xc0\xc6\x845\x9e\x8d7\x94\x86YY",
        ),
        (
            4321,
            "jaguar",
            1,
            b"\x06jaguar\x05cs430\x06luther\x03edu\x00\x00\x01\x00\x01",
            b"\x10\xe1\x81\x00\x00\x01\x00\x01\x00\x00\x00\x00\x06jaguar\x05cs430\x06luther\x03edu\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\x00\x00<\x00\x042\x16\x11\x8e",
        ),
    ],
)
def test_format_response(zone, trans_id, qry_name, qry_type, qry_bytes, response):
    """Format a response"""
    assert (
        format_response(
            zone,
            trans_id,
            qry_name,
            qry_type,
            qry_bytes,
        )
        == response
    )


@pytest.mark.parametrize(
    "origin, request_bytes, request_params",
    [
        (
            "cs430.luther.edu",
            b"6\xc3\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03ant\x05cs430\x06luther\x03edu\x00\x00\x01\x00\x01",
            (14019, "ant", 1, b"\x03ant\x05cs430\x06luther\x03edu\x00\x00\x01\x00\x01"),
        ),
        (
            "cs430.luther.edu",
            b"i\xce\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03ant\x05cs430\x06luther\x03edu\x00\x00\x1c\x00\x01",
            (
                27086,
                "ant",
                28,
                b"\x03ant\x05cs430\x06luther\x03edu\x00\x00\x1c\x00\x01",
            ),
        ),
        (
            "cs430.luther.edu",
            b"\x10\xe1\x81\x00\x00\x01\x00\x01\x00\x00\x00\x00\x06jaguar\x05cs430\x06luther\x03edu\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\x00\x00<\x00\x042\x16\x11\x8e",
            (
                4321,
                "jaguar",
                1,
                b"\x06jaguar\x05cs430\x06luther\x03edu\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\x00\x00<\x00\x042\x16\x11\x8e",
            ),
        ),
    ],
)
def test_parse_request(origin, request_bytes, request_params):
    """Parse the request"""
    assert (
        parse_request(
            origin,
            request_bytes,
        )
        == request_params
    )


@pytest.mark.parametrize(
    "origin, query_bytes, error_message",
    [
        (
            "cs430.luther.edu",
            b"6\xc3\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03ant\x05cs430\x06luther\x03edu\x00\x00\x03\x00\x01",
            "Unknown query type",
        ),
        (
            "cs430.luther.edu",
            b"6\xc3\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03ant\x05cs430\x06luther\x03edu\x00\x00\x01\x00\x03",
            "Unknown class",
        ),
        (
            "luther.edu",
            b"6\xc3\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03ant\x05cs430\x06luther\x03edu\x00\x00\x01\x00\x01",
            "Unknown origin",
        ),
    ],
)
def test_parse_request_query_error(origin, query_bytes, error_message):
    """Query type/class/origin is incorrect"""
    with pytest.raises(ValueError) as excinfo:
        parse_request(
            origin,
            query_bytes,
        )
    exception_msg = excinfo.value.args[0]
    assert exception_msg == error_message


if __name__ == "__main__":
    pytest.main(["-v", __file__])
