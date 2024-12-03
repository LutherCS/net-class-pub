#!/usr/bin/env python3
"""
`nameserver` testing
`
@author: Roman Yasinovskyy
@version: 2024.12
"""

from random import seed
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
    from src.projects.nameserver.nameserver import (
        val_to_n_bytes,
        bytes_to_val,
        get_left_n_bits,
        get_right_n_bits,
        get_origin,
        read_zone_file,
        parse_request,
        format_response,
        run,
    )

seed(430)


@pytest.fixture(scope="function", autouse=True, name="zone")
def zone_fixture():
    """Setting up"""
    return read_zone_file("data/projects/nameserver/zoo.zone")


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
    "filename, exp_origin",
    [
        ("data/projects/nameserver/zoo.zone", "cs430.luther.edu"),
    ],
)
def test_read_origin(filename, exp_origin):
    """Read origin from the zone file"""
    origin = get_origin(filename)
    assert origin == exp_origin


@pytest.mark.parametrize(
    "filename, records",
    [
        ("data/projects/nameserver/zoo.zone", 25),
    ],
)
def test_read_zone_file(filename, records):
    """Read records from the zone file"""
    zone = read_zone_file(filename)
    assert len(zone) == records


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
            b"&\xc6\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x04gaur\x05cs430\x06luther\x03edu\x00\x00\x01\x00\x01",
            (
                9926,
                "gaur",
                1,
                b"\x04gaur\x05cs430\x06luther\x03edu\x00\x00\x01\x00\x01",
            ),
        ),
        (
            "cs430.luther.edu",
            b"\xbbt\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x05nyala\x05cs430\x06luther\x03edu\x00\x00\x1c\x00\x01",
            (
                47988,
                "nyala",
                28,
                b"\x05nyala\x05cs430\x06luther\x03edu\x00\x00\x1c\x00\x01",
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
            "mara",
            1,
            b"\x04mara\x05cs430\x06luther\x03edu\x00\x00\x01\x00\x01",
            b"\x10\xe1\x81\x00\x00\x01\x00\x01\x00\x00\x00\x00\x04mara\x05cs430\x06luther\x03edu\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\x00\x00<\x00\x04\xa0\x9f\xb9!",
        ),
        (
            2024,
            "quail",
            28,
            b"\x05quail\x05cs430\x06luther\x03edu\x00\x00\x1c\x00\x01",
            b"\x07\xe8\x81\x00\x00\x01\x00\x01\x00\x00\x00\x00\x05quail\x05cs430\x06luther\x03edu\x00\x00\x1c\x00\x01\xc0\x0c\x00\x1c\x00\x01\x00\t:\x80\x00\x10\x15\xdb\xd0\xd3\xca\x94\x14\x91\x88\xd4\x8b\xc7\xe7bA\xac",
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


@pytest.mark.parametrize(
    "mock_request, exp_response",
    [
        (
            b"\xbf\xe9\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03cat\x05cs430\x06luther\x03edu\x00\x00\x01\x00\x01",
            b'\xbf\xe9\x81\x00\x00\x01\x00\x01\x00\x00\x00\x00\x03cat\x05cs430\x06luther\x03edu\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\x01Q\x80\x00\x04"\x1c\x8cm',
        ),
        (
            b"jc\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03cat\x05cs430\x06luther\x03edu\x00\x00\x1c\x00\x01",
            b"jc\x81\x00\x00\x01\x00\x01\x00\x00\x00\x00\x03cat\x05cs430\x06luther\x03edu\x00\x00\x1c\x00\x01\xc0\x0c\x00\x1c\x00\x01\x00\x01Q\x80\x00\x10\xf7k\xc3\x94\xedEDd9\x15\x82,\x13\x90F\x82",
        ),
        (
            b"q\xc6\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x06jaguar\x05cs430\x06luther\x03edu\x00\x00\x01\x00\x01",
            b"q\xc6\x81\x00\x00\x01\x00\x01\x00\x00\x00\x00\x06jaguar\x05cs430\x06luther\x03edu\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\t:\x80\x00\x042\x16\x11\x8e",
        ),
        (
            b".\x98\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x06jaguar\x05cs430\x06luther\x03edu\x00\x00\x1c\x00\x01",
            b".\x98\x81\x00\x00\x01\x00\x01\x00\x00\x00\x00\x06jaguar\x05cs430\x06luther\x03edu\x00\x00\x1c\x00\x01\xc0\x0c\x00\x1c\x00\x01\x00\t:\x80\x00\x10\x9a\xc7870\x7f\x82\xddj\x17\xed\x194\xba\xeb\xf1",
        ),
        (
            b"\xa2\xfe\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x04lion\x05cs430\x06luther\x03edu\x00\x00\x01\x00\x01",
            b"\xa2\xfe\x81\x00\x00\x01\x00\x02\x00\x00\x00\x00\x04lion\x05cs430\x06luther\x03edu\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\x00\x00<\x00\x04\xd2\xf9DD\xc0\x0c\x00\x01\x00\x01\x00\t:\x80\x00\x04\x91\xa3\x01\x90",
        ),
        (
            b"\x1a\xae\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x04lion\x05cs430\x06luther\x03edu\x00\x00\x1c\x00\x01",
            b"\x1a\xae\x81\x00\x00\x01\x00\x01\x00\x00\x00\x00\x04lion\x05cs430\x06luther\x03edu\x00\x00\x1c\x00\x01\xc0\x0c\x00\x1c\x00\x01\x00\t:\x80\x00\x10\xe1\xb8\xc2#\x8cDS\xb0lmjV\x05\xcd\x86{",
        ),
        (
            b"*\xae\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x04puma\x05cs430\x06luther\x03edu\x00\x00\x01\x00\x01",
            b"*\xae\x81\x00\x00\x01\x00\x02\x00\x00\x00\x00\x04puma\x05cs430\x06luther\x03edu\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\t:\x80\x00\x04FT\x89D\xc0\x0c\x00\x01\x00\x01\x00\t:\x80\x00\x04<\xa8A\x02",
        ),
        (
            b"\x0b\xb7\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x04puma\x05cs430\x06luther\x03edu\x00\x00\x1c\x00\x01",
            b"\x0b\xb7\x81\x00\x00\x01\x00\x01\x00\x00\x00\x00\x04puma\x05cs430\x06luther\x03edu\x00\x00\x1c\x00\x01\xc0\x0c\x00\x1c\x00\x01\x00\t:\x80\x00\x10wL\xb9T~{\x05\xb3\x1e\x9d\xfe{|?h\xa6",
        ),
        (
            b"\xf7\xb6\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x06numbat\x05cs430\x06luther\x03edu\x00\x00\x01\x00\x01",
            b"\xf7\xb6\x81\x03\x00\x01\x00\x00\x00\x00\x00\x00\x06numbat\x05cs430\x06luther\x03edu\x00\x00\x01\x00\x01",
        ),
    ],
)
def test_run(mock_request: bytes, exp_response: bytes) -> None:
    """Test main loop with a request for a domain not in the zone"""
    origin = get_origin("data/projects/nameserver/zoo.zone")
    zone = read_zone_file("data/projects/nameserver/zoo.zone")
    trans_id, domain, qry_type, qry = parse_request(origin, mock_request)
    response = format_response(zone, trans_id, domain, qry_type, qry)
    assert response == exp_response


@pytest.mark.skip(reason="Work in progress")
def test_run_mock(mock_request, exp_response) -> None:
    """Test main loop with mock requests"""
    with mock.patch("socket.socket") as sock:
        sock.recvfrom.return_value = (mock_request, ("localhost", 0))
        run("data/projects/nameserver/zoo.zone")
        assert sock.sendto.return_value == (exp_response, ("localhost", 0))


if __name__ == "__main__":
    pytest.main(["-v", __file__])
