"""
UDP socket server

@author: Roman Yasinovskyy
@version: 2026.9
"""

import socket
from random import randint
from socket import AF_INET, SOCK_DGRAM
from time import sleep

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
