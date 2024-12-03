#!/usr/bin/env python3
"""
`nameserver` implementation

@author:
@version: 2024.12
"""

import argparse
import logging
from socket import AF_INET, SOCK_DGRAM, socket

HOST = "localhost"
PORT = 43053

DNS_TYPES = {1: "A", 2: "NS", 5: "CNAME", 12: "PTR", 15: "MX", 16: "TXT", 28: "AAAA"}

TTL_SEC = {
    "1s": 1,
    "1m": 60,
    "1h": 60 * 60,
    "1d": 60 * 60 * 24,
    "1w": 60 * 60 * 24 * 7,
    "1y": 60 * 60 * 24 * 365,
}


def val_to_n_bytes(value: int, n_bytes: int) -> tuple[int, ...]:
    """
    Split a value into n bytes
    Return the result as a tuple of n integers
    """
    # TODO: Implement this function
    ...


def bytes_to_val(bytes_lst: list) -> int:
    """Merge n bytes into a value"""
    # TODO: Implement this function
    ...


def get_left_n_bits(bytes_lst: list, n_bits: int) -> int:
    """
    Extract first (leftmost) n bits of a two-byte sequence
    Return the result as a decimal value
    """
    # TODO: Implement this function
    ...


def get_right_n_bits(bytes_lst: list, n_bits: int) -> int:
    """
    Extract last (rightmost) n bits of a two-byte sequence
    Return the result as a decimal value
    """
    # TODO: Implement this function
    ...


def get_origin(filename: str) -> str:
    """
    Read the origin from the zone file
    """
    # TODO: Implement this function
    ...


def read_zone_file(filename: str) -> dict[str, list]:
    """
    Read the zone file and build a dictionary
    Use domain names as keys and list(s) of records as values
    """
    # TODO: Implement this function
    ...


def parse_request(origin: str, msg_req: bytes) -> tuple:
    """
    Parse the request
    Return query parameters as a tuple
    """
    # TODO: Implement this function
    ...


def format_response(
    zone: dict, trans_id: int, qry_name: str, qry_type: int, qry: bytearray
) -> bytearray:
    """Format the response"""
    # TODO: Implement this function
    ...


def run(filename: str) -> None:
    """Main server loop"""
    origin = get_origin(filename)
    zone = read_zone_file(filename)
    with socket(AF_INET, SOCK_DGRAM) as server_sckt:
        server_sckt.bind((HOST, PORT))
        print("Listening on %s:%d" % (HOST, PORT))

        while True:
            try:
                (request_msg, client_addr) = server_sckt.recvfrom(2048)
            except KeyboardInterrupt:
                print("Quitting")
                break
            try:
                trans_id, domain, qry_type, qry = parse_request(origin, request_msg)
                msg_resp = format_response(zone, trans_id, domain, qry_type, qry)
                server_sckt.sendto(msg_resp, client_addr)
            except ValueError as v_err:
                print(f"Ignoring the request: {v_err}")


def main():
    """Main function"""
    arg_parser = argparse.ArgumentParser(description="Parse arguments")
    arg_parser.add_argument("zone_file", type=str, help="Zone file")
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

    run(args.zone_file)


if __name__ == "__main__":
    main()
