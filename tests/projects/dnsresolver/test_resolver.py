#!/usr/bin/env python3
"""
`dnsresolver` testing

@authors: Roman Yasinovskyy
@version: 2022.10
"""


import importlib
import pathlib
import sys

import pytest

try:
    importlib.util.find_spec(".".join(pathlib.Path(__file__).parts[-3:-1]), "src")
except ModuleNotFoundError:
    sys.path.append(f"{pathlib.Path(__file__).parents[3]}/")
finally:
    from src.projects.dnsresolver.resolver import (PUBLIC_DNS_SERVER,
                                                   bytes_to_val, format_query,
                                                   get_2_bits,
                                                   get_domain_name_location,
                                                   parse_address_a,
                                                   parse_address_aaaa,
                                                   parse_answers,
                                                   parse_cli_query,
                                                   parse_response,
                                                   val_to_2_bytes,
                                                   val_to_n_bytes)


@pytest.mark.parametrize("number, all_bytes", [(430, (1, 174)), (43043, (168, 35))])
def test_val_to_2_bytes(number, all_bytes):
    """Convert a value to 2 bytes"""
    assert val_to_2_bytes(number) == all_bytes


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


@pytest.mark.parametrize("all_bytes, bit_value", [([0xC0, 0x0C], 3), ([128, 43], 2)])
def test_get_2_bits(all_bytes, bit_value):
    """Get the first 2 bits from 2 bytes"""
    assert get_2_bits(all_bytes) == bit_value


@pytest.mark.parametrize("all_bytes, offset", [([0xC0, 0x0C], 12), ([192, 43], 43)])
def test_get_domain_name_location(all_bytes, offset):
    """Get domain name location"""
    assert get_domain_name_location(all_bytes) == offset


@pytest.mark.parametrize(
    "query, domain_name, record_type, server_address",
    [
        (("example.com", "A"), ["example", "com"], 1, None),
        (("example.com", "A", "1.1.1.1"), ["example", "com"], 1, "1.1.1.1"),
        (("example.com", "AAAA"), ["example", "com"], 28, None),
        (("example.com", "AAAA", "1.0.0.1"), ["example", "com"], 28, "1.0.0.1"),
        (
            ("donald.knuth.luther.edu", "A"),
            ["donald", "knuth", "luther", "edu"],
            1,
            None,
        ),
        (
            ("donald.knuth.luther.edu", "AAAA", "1.0.0.1"),
            ["donald", "knuth", "luther", "edu"],
            28,
            "1.0.0.1",
        ),
    ],
)
def test_parse_cli_query(query, domain_name, record_type, server_address):
    """Parse command-line arguments"""
    cli_query = parse_cli_query(*query)
    assert cli_query[0] == domain_name
    assert cli_query[1] == record_type
    if server_address:
        assert cli_query[2] == server_address
    else:
        assert cli_query[2] in PUBLIC_DNS_SERVER


@pytest.mark.parametrize(
    "query",
    [
        ("example.com", "MX"),
        ("example.com", "AAA"),
    ],
)
def test_parse_cli_query_error(query):
    """Parse command-line arguments"""
    with pytest.raises(ValueError) as excinfo:
        parse_cli_query(*query)
    exception_msg = excinfo.value.args[0]
    assert exception_msg == "Unknown query type"


@pytest.mark.parametrize(
    "domain_name, record_type, query_data",
    [
        (
            ["example", "com"],
            28,
            b"OB\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07example\x03com\x00"
            + b"\x00\x1c\x00\x01",
        ),
        (
            ["luther", "edu"],
            1,
            b"OB\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x06luther\x03edu\x00"
            + b"\x00\x01\x00\x01",
        ),
    ],
)
def test_format_query(domain_name, record_type, query_data):
    """Format a query, ignore the first two (random) bytes"""
    assert format_query(domain_name, record_type)[2:] == query_data[2:]


@pytest.mark.parametrize(
    "response_bytes, answer",
    [
        (
            b"\xc7D\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00\x06luther\x03edu"
            + b"\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\x00\x01,\x00"
            + b"\x04\xae\x81\x19\xaa",
            [("luther.edu", "174.129.25.170", 300)],
        ),
        (
            b"\x36\xce\x81\x80\x00\x01\x00\x01\x00\x00\x00\x01\x02\x66\x62\x03"
            + b"\x63\x6f\x6d\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00"
            + b"\x00\x00\x05\x00\x04\x9d\xf0\x0e\x23\x00\x00\x29\x10\x00\x00"
            + b"\x00\x00\x05\x00\x00",
            [("fb.com", "157.240.14.35", 5)],
        ),
        (
            b"r\xd4\x81\x80\x00\x01\x00\x06\x00\x00\x00\x00\x05yahoo\x03com"
            + b"\x00\x00\x01\x00\x01\x05yahoo\x03com\x00\x00\x01\x00\x01\x00\x00"
            + b"\x00\x05\x00\x04b\x89\xf6\x07\x05yahoo\x03com\x00\x00\x01\x00\x01"
            + b"\x00\x00\x00\x05\x00\x04H\x1e#\t\x05yahoo\x03com\x00\x00\x01\x00"
            + b"\x01\x00\x00\x00\x05\x00\x04H\x1e#\n\x05yahoo\x03com\x00\x00\x01"
            + b"\x00\x01\x00\x00\x00\x05\x00\x04b\x8a\xdb\xe7\x05yahoo\x03com\x00"
            + b"\x00\x01\x00\x01\x00\x00\x00\x05\x00\x04b\x89\xf6\x08\x05yahoo\x03com"
            + b"\x00\x00\x01\x00\x01\x00\x00\x00\x05\x00\x04b\x8a\xdb\xe8",
            [
                ("yahoo.com", "98.137.246.7", 5),
                ("yahoo.com", "72.30.35.9", 5),
                ("yahoo.com", "72.30.35.10", 5),
                ("yahoo.com", "98.138.219.231", 5),
                ("yahoo.com", "98.137.246.8", 5),
                ("yahoo.com", "98.138.219.232", 5),
            ],
        ),
        (
            b"k\xfb\x81\x80\x00\x01\x00\x06\x00\x00\x00\x00\x05yahoo\x03com"
            + b"\x00\x00\x1c\x00\x01\xc0\x0c\x00\x1c\x00\x01\x00\x00\x04T\x00\x10 "
            + b"\x01I\x98\x00X\x186\x00\x00\x00\x00\x00\x00\x00\x11\xc0\x0c\x00\x1c"
            + b"\x00\x01\x00\x00\x04T\x00\x10 \x01I\x98\x00X\x186\x00\x00\x00\x00\x00"
            + b"\x00\x00\x10\xc0\x0c\x00\x1c\x00\x01\x00\x00\x04T\x00\x10 \x01I\x98"
            + b"\x00D\x04\x1d\x00\x00\x00\x00\x00\x00\x00\x04\xc0\x0c\x00\x1c\x00"
            + b"\x01\x00\x00\x04T\x00\x10 \x01I\x98\x00D\x04\x1d\x00\x00\x00\x00"
            + b"\x00\x00\x00\x03\xc0\x0c\x00\x1c\x00\x01\x00\x00\x04T\x00\x10 \x01I"
            + b"\x98\x00\x0c\x10#\x00\x00\x00\x00\x00\x00\x00\x05\xc0\x0c\x00\x1c"
            + b"\x00\x01\x00\x00\x04T\x00\x10 \x01I\x98\x00\x0c\x10#\x00\x00\x00\x00\x00\x00\x00\x04",
            [
                ("yahoo.com", "2001:4998:58:1836:0:0:0:11", 1108),
                ("yahoo.com", "2001:4998:58:1836:0:0:0:10", 1108),
                ("yahoo.com", "2001:4998:44:41d:0:0:0:4", 1108),
                ("yahoo.com", "2001:4998:44:41d:0:0:0:3", 1108),
                ("yahoo.com", "2001:4998:c:1023:0:0:0:5", 1108),
                ("yahoo.com", "2001:4998:c:1023:0:0:0:4", 1108),
            ],
        ),
    ],
)
def test_parse_response(response_bytes, answer):
    """Parse the response"""
    assert parse_response(response_bytes) == answer


@pytest.mark.parametrize(
    "response_bytes, offset, number_of_answers, answer",
    [
        (
            b"tH\x81\x80\x00\x01\x00\x01\x00\x03\x00\x01\x06luther\x03edu\x00"
            + b"\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\x00\x01,\x00\x04"
            + b"\xae\x81\x19\xaa\xc0\x0c\x00\x02\x00\x01\x00\x01Q\x80\x00\x10"
            + b"\x05dns-2\x07iastate\xc0\x13\xc0\x0c\x00\x02\x00\x01\x00\x01Q"
            + b"\x80\x00\n\x03dns\x03uni\xc0\x13\xc0\x0c\x00\x02\x00\x01\x00"
            + b"\x01Q\x80\x00\t\x06martin\xc0\x0c\xc0j\x00\x01\x00\x01\x00\x01"
            + b"Q\x80\x00\x04\xc0\xcb\xc4\x14",
            28,
            1,
            [("luther.edu", "174.129.25.170", 300)],
        ),
        (
            b"{\xae\x81\x80\x00\x01\x00\x06\x00\x05\x00\x08\x05yahoo\x03com"
            + b"\x00\x00\x1c\x00\x01\xc0\x0c\x00\x1c\x00\x01\x00\x00\x04\xe9"
            + b"\x00\x10 \x01I\x98\x00D\x04\x1d\x00\x00\x00\x00\x00\x00\x00\x04"
            + b"\xc0\x0c\x00\x1c\x00\x01\x00\x00\x04\xe9\x00\x10 \x01I\x98\x00D"
            + b"\x04\x1d\x00\x00\x00\x00\x00\x00\x00\x03\xc0\x0c\x00\x1c\x00"
            + b"\x01\x00\x00\x04\xe9\x00\x10 \x01I\x98\x00X\x186\x00\x00\x00"
            + b"\x00\x00\x00\x00\x11\xc0\x0c\x00\x1c\x00\x01\x00\x00\x04\xe9"
            + b"\x00\x10 \x01I\x98\x00\x0c\x10#\x00\x00\x00\x00\x00\x00\x00\x04"
            + b"\xc0\x0c\x00\x1c\x00\x01\x00\x00\x04\xe9\x00\x10 \x01I\x98\x00"
            + b"\x0c\x10#\x00\x00\x00\x00\x00\x00\x00\x05\xc0\x0c\x00\x1c\x00"
            + b"\x01\x00\x00\x04\xe9\x00\x10 \x01I\x98\x00X\x186\x00\x00\x00"
            + b"\x00\x00\x00\x00\x10\xc0\x0c\x00\x02\x00\x01\x00\x00s0\x00\x06"
            + b"\x03ns1\xc0\x0c\xc0\x0c\x00\x02\x00\x01\x00\x00s0\x00\x06\x03"
            + b"ns3\xc0\x0c\xc0\x0c\x00\x02\x00\x01\x00\x00s0\x00\x06\x03ns5"
            + b"\xc0\x0c\xc0\x0c\x00\x02\x00\x01\x00\x00s0\x00\x06\x03ns2\xc0"
            + b"\x0c\xc0\x0c\x00\x02\x00\x01\x00\x00s0\x00\x06\x03ns4\xc0\x0c"
            + b"\xc0\xcf\x00\x1c\x00\x01\x00\x00CX\x00\x10 \x01I\x98\x010\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x10\x01\xc1\x05\x00\x1c\x00\x01"
            + b"\x00\x00\xda\xdb\x00\x10 \x01I\x98\x01@\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x10\x02\xc0\xe1\x00\x1c\x00\x01\x00\x00\xd9\xb0\x00"
            + b"\x10$\x06\x86\x00\x00\xb8\xfe\x03\x00\x00\x00\x00\x00\x00\x10"
            + b"\x03\xc0\xcf\x00\x01\x00\x01\x00\x11f\xdc\x00\x04D\xb4\x83\x10"
            + b"\xc1\x05\x00\x01\x00\x01\x00\x11f\xde\x00\x04D\x8e\xff\x10\xc0"
            + b"\xe1\x00\x01\x00\x01\x00\x0f\xfe\xc3\x00\x04\xcbT\xdd5\xc1\x17"
            + b"\x00\x01\x00\x01\x00\x11\x8ah\x00\x04b\x8a\x0b\x9d\xc0\xf3\x00"
            + b"\x01\x00\x01\x00\x11PF\x00\x04w\xa0\xfdS",
            27,
            6,
            [
                ("yahoo.com", "2001:4998:44:41d:0:0:0:4", 1257),
                ("yahoo.com", "2001:4998:44:41d:0:0:0:3", 1257),
                ("yahoo.com", "2001:4998:58:1836:0:0:0:11", 1257),
                ("yahoo.com", "2001:4998:c:1023:0:0:0:4", 1257),
                ("yahoo.com", "2001:4998:c:1023:0:0:0:5", 1257),
                ("yahoo.com", "2001:4998:58:1836:0:0:0:10", 1257),
            ],
        ),
    ],
)
def test_parse_answers(response_bytes, offset, number_of_answers, answer):
    """Parse answers"""
    assert parse_answers(response_bytes, offset, number_of_answers) == answer


@pytest.mark.parametrize(
    "addr_length, addr_bytes, addr_human",
    [
        (4, b"\xae\x81\x19\xaa", "174.129.25.170"),
        (4, b"\x34\x01\xe6\xdd", "52.1.230.221"),
    ],
)
def test_parse_address_a(addr_length, addr_bytes, addr_human):
    """Parse IPv4 address"""
    assert parse_address_a(addr_length, addr_bytes) == addr_human


@pytest.mark.parametrize(
    "addr_length, addr_bytes, addr_human",
    [
        (
            16,
            b" \x01I\x98\x00\x0c\x10#\x00\x00\x00\x00\x00\x00\x00\x04",
            "2001:4998:c:1023:0:0:0:4",
        ),
        (
            16,
            b"*\x03(\x80\xf1,\x01\x83\xfa\xce\xb0\x0c\x00\x00%\xde",
            "2a03:2880:f12c:183:face:b00c:0:25de",
        ),
    ],
)
def test_parse_address_aaaa(addr_length, addr_bytes, addr_human):
    """Parse IPv6 address"""
    assert parse_address_aaaa(addr_length, addr_bytes) == addr_human


if __name__ == "__main__":
    pytest.main(["-v", __file__])
