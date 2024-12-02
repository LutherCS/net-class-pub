#!/usr/bin/env python3
"""
Router implementation using UDP sockets

@author:
@version: 2024.12
"""

import argparse
import logging
import pathlib
import random
import select
import socket
import struct
import time

THIS_HOST = "localhost"
BASE_PORT = 4300


def read_config_file(filename: str) -> tuple[set, dict]:
    """
    Read config file

    :param filename: name of the configuration file
    :return tuple of the (neighbors, routing table)
    """
    ...


def format_update(routing_table: dict) -> bytes:
    """
    Format update message

    :param routing_table: routing table of this router
    :returns the formatted message
    """
    ...


def parse_update(msg: bytes, neigh_addr: str, routing_table: dict) -> bool:
    """
    Update routing table

    :param msg: message from a neighbor
    :param neigh_addr: neighbor's address
    :param routing_table: this router's routing table
    :returns True is the table has been updated, False otherwise
    """
    ...


def send_update(node: str) -> None:
    """
    Send update

    :param node: recipient of the update message
    """
    ...


def format_hello(msg_txt: str, src_node: str, dst_node: str) -> bytes:
    """
    Format hello message

    :param msg_txt: message text
    :param src_node: message originator
    :param dst_node: message recipient
    """
    ...


def parse_hello(msg: bytes, routing_table: dict) -> str:
    """
    Parse the HELLO message

    :param msg: message
    :param routing_table: this router's routing table
    :returns the action taken as a string
    """
    ...


def send_hello(msg_txt: str, src_node: str, dst_node: str, routing_table: dict) -> None:
    """
    Send a message

    :param mst_txt: message to send
    :param src_node: message originator
    :param dst_node: message recipient
    :param routing_table: this router's routing table
    """
    ...


def print_status(routing_table: dict) -> None:
    """
    Print status

    :param routing_table: this router's routing table
    """
    ...


def route(neighbors: set, routing_table: dict, timeout: int = 5):
    """
    Router's main loop

    :param neighbors: this router's neighbors
    :param routing_table: this router's routing table
    :param timeout: default 5
    """
    ubuntu_release = [
        "Plucky Puffin",
        "Oracular Oriole",
        "Noble Numbat",
        "Mantic Minotaur",
        "Lunar Lobster",
        "Kinetic Kudu",
        "Jammy Jellyfish",
        "Impish Indri",
        "Hirsute Hippo",
        "Groovy Gorilla",
        "Focal Fossa",
        "Eoam Ermine",
        "Disco Dingo",
        "Cosmic Cuttlefish",
        "Bionic Beaver",
        "Artful Aardvark",
    ]
    ...


def main():
    """Main function"""
    ...


if __name__ == "__main__":
    main()
