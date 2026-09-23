"""
Server implementation

@author:
@version: 2026.9
"""

import argparse
import datetime
import logging
from pathlib import Path
from socket import AF_INET, SO_REUSEADDR, SOCK_STREAM, SOL_SOCKET, socket

SRVR_ADDR = "127.0.0.1"
SRVR_PORT = 4380  # Open http://127.0.0.1:4380 in a browser
SRVR_NAME = ""
# A request for the key should redirect to the mapped value
REDIRECT = {"alice.txt": "alice30.txt", "test.txt": "test26.txt"}


def parse_request(data: bytes) -> dict[str, str]:
    """Parse the incoming request

    :return: a dictionary of key-value mappings based on the request header
    """
    # TODO: Implement this function


def format_response(
    http_version: str, status_code: int, header: dict | None = None, data: str = ""
) -> bytes:
    """Format the response

    :return: encoded message that includes header and data
    """
    # TODO: Implement this function


def server_loop(logfilename: Path):
    """Main server loop"""
    # TODO: Implement this function using TCP socket
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.bind((SRVR_ADDR, SRVR_PORT))
        sock.listen()
        print("The server has started")


def main():
    """Set up arguments and start the main server loop"""
    arg_parser = argparse.ArgumentParser(description="Parse arguments")
    arg_parser.add_argument(
        "-l",
        "--logfile",
        type=str,
        help="Log file name",
        default="src/projects/webserver/webserver.log",
    )
    arg_parser.add_argument("-d", "--debug", action="store_true", help="Enable logging.DEBUG mode")
    args = arg_parser.parse_args()

    logger = logging.getLogger("root")
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logger.level)

    try:
        server_loop(Path(args.logfile))
    except KeyboardInterrupt:
        print("\nThe server has stopped")


if __name__ == "__main__":
    main()
