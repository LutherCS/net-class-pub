#!/usr/bin/env python3
"""
`geo client` implementation

@authors:
@version: 2022.9
"""
import argparse
import logging
import socket

HOST = "localhost"
PORT = 4300


def format_message(message: list[str]) -> bytes:
    """Convert the message to bytes

    :param message: message to encode
    :return: message as bytes
    """
    # TODO: Implement this function
    ...


def parse_data(data: bytes) -> str:
    """Convert bytes to a string

    :param data: data received
    :return: decoded string
    """
    # TODO: Implement this function
    ...


def read_user_input() -> str:
    """Read user input from the console

    :return: country name
    """
    # TODO: Implement this function
    ...


def client_loop():
    """Main client loop"""
    print("The client has started")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # TODO: Implement this function
        ...
    print("The client has finished")


def main():
    """Main function"""
    arg_parser = argparse.ArgumentParser(description="Enable debugging")
    arg_parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable logging.DEBUG mode"
    )
    args = arg_parser.parse_args()
    logger = logging.getLogger("root")
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logger.level)
    client_loop()


if __name__ == "__main__":
    main()
