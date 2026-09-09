"""
Server testing

@authors: Roman Yasinovskyy
@version: 2026.9
"""

import pathlib
import sys
from importlib.util import find_spec

import pytest

try:
    find_spec(".".join(pathlib.Path(__file__).parts[-3:-1]), "src")
except ModuleNotFoundError:
    sys.path.append(f"{pathlib.Path(__file__).parents[3]}/")
finally:
    from src.projects.geo.server import (
        find_capital,
        format_message,
        parse_data,
        read_file,
    )


@pytest.fixture(name="small_world")
def fixture_small_world():
    """Test reading the file"""
    world, count = read_file("tests/projects/geo/small_world.csv")
    return world, count


@pytest.mark.parametrize(
    "message, data",
    [
        ("São Tomé", b"S\xc3\xa3o Tom\xc3\xa9"),
        ("Colombo, Sri Jayawardenepura Kotte", b"Colombo, Sri Jayawardenepura Kotte"),
        ("Nukuʻalofa", b"Nuku\xca\xbbalofa"),
    ],
)
def test_format_message(message, data):
    """Test formatting the message"""
    assert format_message(message) == data


@pytest.mark.parametrize(
    "data, message",
    [
        (b"United States of America", "United States of America"),
        (b"C\xc3\xb4te D'Ivoire", "Côte D'Ivoire"),
    ],
)
def test_parse_data(data, message):
    """Test parsing the data"""
    assert parse_data(data) == message


@pytest.mark.parametrize(
    "input_file, countries",
    [
        ("tests/projects/geo/small_world.csv", 5),
        ("data/projects/geo/world.csv", 196),
    ],
)
def test_read_file(input_file, countries):
    _, count = read_file(input_file)
    assert count == countries


@pytest.mark.parametrize(
    "input_file, countries_with_alternative_names",
    [
        ("tests/projects/geo/small_world.csv", 7),
        ("data/projects/geo/world.csv", 201),
    ],
)
def test_read_file_2(input_file, countries_with_alternative_names):
    world, _ = read_file(input_file)
    assert len(world) == countries_with_alternative_names


@pytest.mark.parametrize(
    "country, capital",
    [
        ("Czechia", "Prague"),
        ("Czech Republic", "Prague"),
        (
            "South Africa",
            "Bloemfontein, Cape Town, Pretoria",
        ),
        ("Tonga", "Nukuʻalofa"),
        ("Ukraine", "Kyiv"),
        (
            "United States of America",
            "Washington, D.C.",
        ),
        ("USA", "Washington, D.C."),
        ("Russia", "No such country."),
    ],
)
def test_find_capital(country, capital, small_world):
    world, _ = small_world
    assert find_capital(world, country) == capital


if __name__ == "__main__":
    pytest.main(["-v", __file__])
