#!/usr/bin/env python3
"""
DNS Resolver
"""

import argparse
import logging
from random import randint, choice
from socket import socket, SOCK_DGRAM, AF_INET
from typing import Tuple, List

PORT = 53

DNS_TYPES = {"A": 1, "AAAA": 28, "CNAME": 5, "MX": 15, "NS": 2, "PTR": 12, "TXT": 16}

PUBLIC_DNS_SERVER = [
    "1.0.0.1",  # Cloudflare
    "1.1.1.1",  # Cloudflare
    "8.8.4.4",  # Google
    "8.8.8.8",  # Google
    "8.26.56.26",  # Comodo
    "8.20.247.20",  # Comodo
    "9.9.9.9",  # Quad9
    "64.6.64.6",  # Verisign
    "208.67.222.222",  # OpenDNS
    "208.67.220.220",  # OpenDNS
]


def val_to_2_bytes(value: int) -> Tuple[int]:
    """
    Split a value into 2 bytes
    Return the result as a tuple of 2 integers
    """
    # TODO: Implement this function
    raise NotImplementedError


def val_to_n_bytes(value: int, n_bytes: int) -> Tuple[int]:
    """
    Split a value into n bytes
    Return the result as a tuple of n integers
    """
    # TODO: Implement this function
    raise NotImplementedError


def bytes_to_val(byte_list: list) -> int:
    """Merge n bytes into a value"""
    # TODO: Implement this function
    raise NotImplementedError


def get_2_bits(byte_list: list) -> int:
    """
    Extract first two bits of a two-byte sequence
    Return the result as a decimal value
    """
    # TODO: Implement this function
    raise NotImplementedError


def get_domain_name_location(byte_list: list) -> int:
    """
    Extract size of the offset from a two-byte sequence
    Return the result as a decimal value
    """
    # TODO: Implement this function
    raise NotImplementedError


def parse_cli_query(
    q_domain: str, q_type: str, q_server: str = None
) -> Tuple[list, int, str]:
    """
    Parse command-line query
    Return a tuple of the domain (as a list of subdomains), numeric type, and the server
    If the server is not specified, pick a random one from `PUBLIC_DNS_SERVER`
    If type is not `A` or `AAAA`, raise `ValueError`
    """
    # TODO: Implement this function
    raise NotImplementedError


def format_query(q_domain: list, q_type: int) -> bytearray:
    """
    Format DNS query
    Take the domain name (as a list) and the record type as parameters
    Return a properly formatted query
    Assumpions (defaults):
    - transaction id: random 0..65535
    - flags: recursive query set
    - questions: 1
    - class: Internet
    """
    # TODO: Implement this function
    raise NotImplementedError


def parse_response(resp_bytes: bytes) -> list:
    """
    Parse server response
    Take response bytes as a parameter
    Return a list of tuples in the format of (name, address, ttl)
    """
    # TODO: Implement this function
    raise NotImplementedError


def parse_answers(resp_bytes: bytes, answer_start: int, rr_ans: int) -> List[tuple]:
    """
    Parse DNS server answers
    Take response bytes, offset, and the number of answers as parameters
    Return a list of tuples in the format of (name, address, ttl)
    """
    # TODO: Implement this function
    raise NotImplementedError


def parse_address_a(addr_len: int, addr_bytes: bytes) -> str:
    """
    Parse IPv4 address
    Convert bytes to human-readable dotted-decimal
    """
    # TODO: Implement this function
    raise NotImplementedError


def parse_address_aaaa(addr_len: int, addr_bytes: bytes) -> str:
    """Extract IPv6 address"""
    # TODO: Implement this function
    raise NotImplementedError


def resolve(query: tuple) -> None:
    """Resolve the query"""
    try:
        q_domain, q_type, q_server = parse_cli_query(*query)
    except ValueError as ve:
        print(ve.args[0])
        exit()
    logging.info(f"Resolving type {q_type} for {q_domain} using {q_server}")
    query_bytes = format_query(q_domain, q_type)
    with socket(AF_INET, SOCK_DGRAM) as sock:
        sock.sendto(query_bytes, (q_server, PORT))
        response_data, _ = sock.recvfrom(2048)
    answers = parse_response(response_data)
    print(f"DNS server used: {q_server}")
    for a in answers:
        print()
        print(f"{'Domain:':10s}{a[0]}")
        print(f"{'Address:':10s}{a[1]}")
        print(f"{'TTL:':10s}{a[2]}")


def main():
    """Main function"""
    # TODO: Complete this function
    arg_parser = argparse.ArgumentParser(description="Parse arguments")
    args = arg_parser.parse_args()

    logger = logging.getLogger("root")
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logger.level)

    resolve((args.domain, args.type, args.server))
    raise NotImplementedError


if __name__ == "__main__":
    main()
