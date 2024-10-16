#!/usr/bin/env python3
"""
`dnsresolver` testing

@authors: Roman Yasinovskyy
@version: 2024.10
"""

import importlib
import pathlib
import sys
import tomllib
from typing import Generator

import pytest

try:
    importlib.util.find_spec(".".join(pathlib.Path(__file__).parts[-3:-1]), "src")
except ModuleNotFoundError:
    sys.path.append(f"{pathlib.Path(__file__).parents[3]}/")
finally:
    from src.projects.dnsresolver.resolver import (
        PUBLIC_DNS_SERVER,
        bytes_to_val,
        format_query,
        get_2_bits,
        get_domain_name_location,
        parse_address_a,
        parse_address_aaaa,
        parse_answers,
        parse_cli_query,
        parse_response,
        val_to_2_bytes,
        val_to_n_bytes,
    )

TIME_LIMIT = 1


def get_cases(category: str, *attribs: str) -> Generator:
    """Get test cases from the TOML file"""
    with open(pathlib.Path(__file__).with_suffix(".toml"), "rb") as file:
        all_cases = tomllib.load(file)
        for case in all_cases[category]:
            yield tuple(case.get(a) for a in attribs)


@pytest.mark.parametrize(
    "number, all_bytes", get_cases("test_case_bytes", "number", "all_bytes")
)
def test_val_to_2_bytes(number: int, all_bytes: list[int]):
    """Convert a value to 2 bytes"""
    assert val_to_2_bytes(number) == tuple(all_bytes[-2:])


@pytest.mark.parametrize(
    "number, n_bytes, all_bytes",
    get_cases("test_case_bytes", "number", "n_bytes", "all_bytes"),
)
def test_val_to_n_bytes(number: int, n_bytes: int, all_bytes: list[int]):
    """Convert a value to n bytes"""
    assert val_to_n_bytes(number, n_bytes) == tuple(all_bytes)


@pytest.mark.parametrize(
    "all_bytes, number",
    get_cases("test_case_bytes", "all_bytes", "number"),
)
def test_bytes_to_val(all_bytes: list[int], number: int):
    """Convert list of bytes to a value"""
    assert bytes_to_val(all_bytes) == number


@pytest.mark.parametrize(
    "all_bytes, bit_value",
    get_cases("test_case_bits", "all_bytes", "bit_value"),
)
def test_get_2_bits(all_bytes: list[int], bit_value: int):
    """Get the first 2 bits from 2 bytes"""
    assert get_2_bits(all_bytes) == bit_value


@pytest.mark.parametrize(
    "all_bytes, offset",
    get_cases("test_case_bits", "all_bytes", "offset"),
)
def test_get_domain_name_location(all_bytes: list[int], offset: int):
    """Get domain name location"""
    assert get_domain_name_location(all_bytes) == offset


@pytest.mark.parametrize(
    "query, domain_name, record_type, server_address",
    get_cases("test_case_cli", "query", "domain_name", "record_type", "server_address"),
)
def test_parse_cli_query(
    query: list[str], domain_name: list[str], record_type: int, server_address: str
):
    """Parse command-line arguments"""
    cli_query = parse_cli_query(*query)
    assert cli_query[0] == domain_name
    assert cli_query[1] == record_type
    if server_address:
        assert cli_query[2] == server_address
    else:
        assert cli_query[2] in PUBLIC_DNS_SERVER


@pytest.mark.parametrize(
    "query, error_msg",
    get_cases("test_case_cli_error", "query", "error_msg"),
)
def test_parse_cli_query_error(query: list[str], error_msg: str):
    """Parse command-line arguments"""
    with pytest.raises(ValueError) as excinfo:
        parse_cli_query(*query)
    exception_msg = excinfo.value.args[0]
    assert exception_msg == error_msg


@pytest.mark.parametrize(
    "domain_name, record_type, query_data_file",
    get_cases(
        "test_case_format_query", "domain_name", "record_type", "query_data_file"
    ),
)
def test_format_query(domain_name: list[str], record_type: int, query_data_file: str):
    """Format a query, ignore the first two (random) bytes"""
    with open(pathlib.Path(__file__).parent / query_data_file, "rb") as f:
        query_data = f.read()
    assert format_query(domain_name, record_type)[2:] == query_data[2:]


@pytest.mark.parametrize(
    "addr_length, addr_bytes, addr_human",
    get_cases(
        "test_case_parse_address_a",
        "addr_length",
        "addr_bytes",
        "addr_human",
    ),
)
def test_parse_address_a(addr_length: int, addr_bytes: list[int], addr_human: str):
    """Parse IPv4 address"""
    assert parse_address_a(addr_length, bytes(addr_bytes)) == addr_human


@pytest.mark.parametrize(
    "addr_length, addr_bytes, addr_human",
    get_cases(
        "test_case_parse_address_aaaa",
        "addr_length",
        "addr_bytes",
        "addr_human",
    ),
)
def test_parse_address_aaaa(addr_length: int, addr_bytes: bytes, addr_human: str):
    """Parse IPv6 address"""
    assert parse_address_aaaa(addr_length, bytes(addr_bytes)) == addr_human


@pytest.mark.parametrize(
    "response_data_file, offset, number_of_answers, answer",
    get_cases(
        "test_case_parse_answers",
        "response_data_file",
        "offset",
        "number_of_answers",
        "answer",
    ),
)
def test_parse_answers(
    response_data_file: str, offset: int, number_of_answers: int, answer: list
):
    """Parse answers"""
    with open(pathlib.Path(__file__).parent / response_data_file, "rb") as f:
        response_data = f.read()
    assert parse_answers(response_data, offset, number_of_answers) == [
        tuple(a) for a in answer
    ]


@pytest.mark.parametrize(
    "response_data_file, answer",
    get_cases("test_case_parse_response", "response_data_file", "answer"),
)
def test_parse_response(response_data_file: str, answer: list):
    """Parse the response"""
    with open(pathlib.Path(__file__).parent / response_data_file, "rb") as f:
        response_data = f.read()
    assert parse_response(response_data) == [tuple(a) for a in answer]


if __name__ == "__main__":
    pytest.main(["-v", __file__])
