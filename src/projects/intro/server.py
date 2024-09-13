#!/usr/bin/env python3
"""
`intro server` implementation

@authors:
@version: 2024.9
"""
import argparse
import logging
import socket

HOST = "127.0.0.1"
PORT = 4300


def format_message(message: str) -> bytes:
    """Convert (encode) the message to bytes"""
    ...


def parse_data(data: bytes) -> str:
    """Convert (decode) bytes to a string"""
    ...


def server_loop():
    """Server event loop"""
    print("The server has started")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        logging.info("Binding to %s:%d", HOST, PORT)
        sock.bind((HOST, PORT))
        logging.info("Bound to %s:%d", HOST, PORT)
        sock.listen(1)
        logging.info("Listening on port %d", PORT)
        conn, addr = sock.accept()
        with conn:
            logging.info("Accepted connections from %s:%d", addr[0], addr[1])
            while True:
                data_in = conn.recv(1024)
                if not data_in:
                    logging.info("Connection closed")
                    break
                message = parse_data(data_in)
                logging.info("Received: %s", message)
                logging.info("Sending response...")
                data_out = format_message(message)
                conn.sendall(data_out)
    print("The server has finished")


def main():
    """Main function"""
    arg_parser = argparse.ArgumentParser(description="Enable debugging")
    arg_parser.add_argument(
        "-d", "--debug", action="store_true", help="enable logging.DEBUG mode"
    )
    args = arg_parser.parse_args()

    # TODO: Get the *root* logger
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logger.level)
    server_loop()


if __name__ == "__main__":
    main()
