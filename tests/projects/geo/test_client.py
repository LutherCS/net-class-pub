"""
Client testing

@authors: Roman Yasinovskyy
@version: 2026.9
"""

import pathlib
import sys
from importlib.util import find_spec
from io import StringIO

import pytest

try:
    find_spec(".".join(pathlib.Path(__file__).parts[-3:-1]), "src")
except ModuleNotFoundError:
    sys.path.append(f"{pathlib.Path(__file__).parents[3]}/")
finally:
    from src.projects.geo.client import format_message, parse_data, read_user_input


@pytest.mark.parametrize(
    "message, data",
    [
        ("United States of America", b"United States of America"),
        ("Côte D'Ivoire", b"C\xc3\xb4te D'Ivoire"),
    ],
)
def test_format_message(message, data):
    """ "Test formatting the message"""
    assert format_message(message) == data


@pytest.mark.parametrize(
    "data, message",
    [
        (b"S\xc3\xa3o Tom\xc3\xa9", "São Tomé"),
        (b"Colombo, Sri Jayawardenepura Kotte", "Colombo, Sri Jayawardenepura Kotte"),
        (b"Nuku\xca\xbbalofa", "Nukuʻalofa"),
    ],
)
def test_parse_data(data, message):
    """Test parsing the data"""
    assert parse_data(data) == message


@pytest.mark.parametrize(
    "user_input, expected",
    [
        ("Côte D'Ivoire", "Côte D'Ivoire"),
        ("São Tomé & Príncipe", "São Tomé & Príncipe"),
        ("BYE", "BYE"),
    ],
)
def test_read_user_input(user_input, expected, monkeypatch):
    """Test reading user input"""
    user_input = StringIO(f"{user_input}\n")
    monkeypatch.setattr("sys.stdin", user_input)
    assert read_user_input() == expected


if __name__ == "__main__":
    pytest.main(["-v", __file__])
