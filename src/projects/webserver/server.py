#!/usr/bin/env python3
"""Python Web server implementation"""
from socket import socket, AF_INET, SOCK_STREAM
from datetime import datetime
from time import sleep
from random import randint
import argparse
import logging
from pathlib import Path


SRVR_ADDR = "127.0.0.2"  # Local client is going to be 127.0.0.1
SRVR_PORT = 43080  # Open http://127.0.0.2:43080 in a browser
SRVR_NAME = ""


def parse_data(data: bytes) -> dict:
    """Parse the incoming request"""
    ...


def format_response(
    http_version: str, status_code: int, header: dict = {}, data: str = ""
) -> bytes:
    """Format the response"""
    ...


def server_loop(logfilename: Path):
    """Main server loop"""
    print("The server has started")
    with socket(AF_INET, SOCK_STREAM) as sock:
        ...



def main():
    """Set up arguments and start the main server loop"""
    arg_parser = argparse.ArgumentParser(description="Parse arguments")
    arg_parser.add_argument("logfile", type=str, help="Log file name")
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

    server_loop(Path(args.logfile))


if __name__ == "__main__":
    main()
