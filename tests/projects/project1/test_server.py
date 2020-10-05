#!/usr/bin/env python3
"""Testing geo server"""

import pytest
from src.projects.project1.server import format, parse, read_file, find_capital


@pytest.fixture
def small_world():
    world, count = read_file("tests/projects/project1/small_world.csv")
    return world, count


@pytest.mark.parametrize(
    "message, data",
    [
        ("São Tomé", b"S\xc3\xa3o Tom\xc3\xa9"),
        ("Colombo, Sri Jayawardenepura Kotte", b"Colombo, Sri Jayawardenepura Kotte"),
    ],
)
def test_server_format(message, data):
    assert format(message) == data


@pytest.mark.parametrize(
    "data, message",
    [
        (b"United States of America", "United States of America"),
        (b"C\xc3\xb4te D'Ivoire", "Côte D'Ivoire"),
    ],
)
def test_server_parse(data, message):
    assert parse(data) == message


@pytest.mark.parametrize(
    "input_file, countries",
    [
        ("tests/projects/project1/small_world.csv", 4),
        ("src/projects/project1/world.csv", 196),
    ],
)
def test_read_file(input_file, countries):
    _, count = read_file(input_file)
    assert count == countries


@pytest.mark.parametrize(
    "input_file, countries_with_alternative_names",
    [
        ("tests/projects/project1/small_world.csv", 6),
        ("src/projects/project1/world.csv", 201),
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
    pytest.main()
