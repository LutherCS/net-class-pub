#!/usr/bin/env python3
"""UDP socket server"""
import socket
from socket import SOCK_DGRAM, AF_INET
from time import sleep
from random import randint

host = "127.0.0.2"
port = 4300


def main():
    print("Server here")
    sock = socket.socket(AF_INET, SOCK_DGRAM)

    while True:
        try:
            sock.bind((host, port))
            break
        except OSError as os_err:
            print(os_err)
            sleep(randint(1, 5))

    while True:
        msg, client = sock.recvfrom(2048)
        msg = msg.decode()
        if msg == "quit":
            break
        print(f"Received {msg}")
        sock.sendto(msg[::-1].encode(), client)
    sock.close()
    print("Server is done")


if __name__ == "__main__":
    main()
