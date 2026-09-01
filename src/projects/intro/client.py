"""
`intro client` implementation

@authors: Roman Yasinovskyy
@version: 2026.9
"""

import argparse
import logging
import socket

HOST = "localhost"
PORT = 4300


def format_message(message: list[str]) -> bytes:
    """Convert (encode) the message to bytes"""
    # TODO: Implement this function


def parse_data(data: bytes) -> str:
    """Convert (decode) bytes to a string"""
    # TODO: Implement this function


def client_loop(name: list):
    """Client event loop"""
    print("The client has started")
    logger = logging.getLogger()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        logger.info("Connecting to %s:%d", HOST, PORT)
        sock.connect((HOST, PORT))
        logger.info("Connected to %s:%d", HOST, PORT)
        logger.info("Formatting data")
        data_out = format_message(name)
        logger.info("Sending data")
        sock.sendall(data_out)
        logger.info("Receiving data")
        data_in = sock.recv(1024)
        logger.info("Parsing data")
        message = parse_data(data_in)
        print(f"Server responded: {message}")
    print("The client has finished")


def main():
    """Main function"""
    arg_parser = argparse.ArgumentParser(description="Enable debugging")
    arg_parser.add_argument("-d", "--debug", action="store_true", help="enable logging.DEBUG mode")
    arg_parser.add_argument("name", type=str, nargs="+", help="Name")
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
