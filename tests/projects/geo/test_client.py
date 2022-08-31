#!/usr/bin/env python3
"""Testing geo client"""

import pytest
from io import StringIO
from src.projects.project1.client import format, parse, read_user_input


@pytest.mark.parametrize(
    "message, data",
    [
        ("United States of America", b"United States of America"),
        ("Côte D'Ivoire", b"C\xc3\xb4te D'Ivoire"),
    ],
)
def test_client_format(message, data):
    assert format(message) == data


@pytest.mark.parametrize(
    "data, message",
    [
        (b"S\xc3\xa3o Tom\xc3\xa9", "São Tomé"),
        (b"Colombo, Sri Jayawardenepura Kotte", "Colombo, Sri Jayawardenepura Kotte"),
    ],
)
def test_client_parse(data, message):
    assert parse(data) == message


@pytest.mark.parametrize(
    "user_input, expected",
    [
        ("Côte D'Ivoire", "Côte D'Ivoire"),
        ("BYE", "BYE"),
    ],
)
def test_read_user_input(user_input, expected, monkeypatch):
    user_input = StringIO(f"{user_input}\n")
    monkeypatch.setattr("sys.stdin", user_input)
    assert read_user_input() == expected


if __name__ == "__main__":
    pytest.main()
