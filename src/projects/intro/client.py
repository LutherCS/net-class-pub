#!/usr/bin/env python3
"""
`intro client` implementation

@authors:
@version: 2022.9
"""
import argparse
import logging
import socket

HOST = "localhost"
PORT = 4300


def format_message(message: list[str]) -> bytes:
    """Convert (encode) the message to bytes"""
    ...
    return f"Hello, my name is {' '.join(message)}".encode()


def parse_data(data: bytes) -> str:
    """Convert (decode) bytes to a string"""
    ...


def client_loop(name: list):
    """Client event loop"""
    print("The client has started")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        logging.info("Connecting to %s:%d", HOST, PORT)
        sock.connect((HOST, PORT))
        logging.info("Connected to %s:%d", HOST, PORT)
        logging.info("Formatting data")
        data_out = format_message(name)
        logging.info("Sending data")
        sock.sendall(data_out)
        logging.info("Receiving data")
        data_in = sock.recv(1024)
        logging.info("Parsing data")
        message = parse_data(data_in)
        print(f"Server responded: {message}")
    print("The client has finished")


def main():
    """Main function"""
    arg_parser = argparse.ArgumentParser(description="Enable debugging")
    arg_parser.add_argument(
        "-d", "--debug", action="store_true", help="enable logging.DEBUG mode"
    )
    # TODO: Add an argparse argument that gathers 1 or more command-line arguments into a list.
    # This will be the name passed to the client
    args = arg_parser.parse_args()
    logger = logging.getLogger("root")
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logger.level)
    name = args.name
    client_loop(name)


if __name__ == "__main__":
    main()
