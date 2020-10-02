import pytest
from src.projects.project0.client import format, parse


@pytest.mark.parametrize(
    "message, data",
    [
        (["Toph"], b"Hello, my name is Toph"),
        (["The", "Child"], b"Hello, my name is The Child"),
        (
            ["フンベルト・フォン・ジッキンゲン"],
            b"Hello, my name is \xe3\x83\x95\xe3\x83\xb3\xe3\x83\x99\xe3\x83\xab\xe3\x83\x88\xe3\x83\xbb\xe3\x83\x95\xe3\x82\xa9\xe3\x83\xb3\xe3\x83\xbb\xe3\x82\xb8\xe3\x83\x83\xe3\x82\xad\xe3\x83\xb3\xe3\x82\xb2\xe3\x83\xb3",
        ),
        (
            ["Чорна", "вдова"],
            b"Hello, my name is \xd0\xa7\xd0\xbe\xd1\x80\xd0\xbd\xd0\xb0 \xd0\xb2\xd0\xb4\xd0\xbe\xd0\xb2\xd0\xb0",
        ),
    ],
)
def test_client_format(message, data):
    assert format(message) == data


@pytest.mark.parametrize(
    "data, message",
    [
        (b"Toph", "Toph"),
        (b"The Child", "The Child"),
        (
            b"\xe3\x83\x95\xe3\x83\xb3\xe3\x83\x99\xe3\x83\xab\xe3\x83\x88\xe3\x83\xbb\xe3\x83\x95\xe3\x82\xa9\xe3\x83\xb3\xe3\x83\xbb\xe3\x82\xb8\xe3\x83\x83\xe3\x82\xad\xe3\x83\xb3\xe3\x82\xb2\xe3\x83\xb3",
            "フンベルト・フォン・ジッキンゲン",
        ),
        (
            b"\xd0\xa7\xd0\xbe\xd1\x80\xd0\xbd\xd0\xb0 \xd0\xb2\xd0\xb4\xd0\xbe\xd0\xb2\xd0\xb0",
            "Чорна вдова",
        ),
    ],
)
def test_client_parse(data, message):
    assert parse(data) == message


if __name__ == "__main__":
    pytest.main()
