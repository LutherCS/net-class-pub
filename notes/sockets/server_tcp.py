"""
TCP socket server

@author: Roman Yasinovskyy
@version: 2026.9
"""

import socket
from random import randint
from socket import AF_INET, SOCK_STREAM
from time import sleep

host = "127.0.0.2"
port = 4300


def main():
    print("Server here")
    sock = socket.socket(AF_INET, SOCK_STREAM)

    while True:
        try:
            sock.bind((host, port))
            sock.listen()
            break
        except OSError as os_err:
            print(os_err)
            sleep(randint(1, 5))
    conn, _ = sock.accept()

    while True:
        msg = conn.recv(2048).decode()
        if not msg:
            break
        print(f"Received {msg}")
        conn.send(msg[::-1].encode())
    sock.close()
    print("Server is done")


if __name__ == "__main__":
    main()
