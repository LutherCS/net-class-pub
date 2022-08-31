"""Python Web server implementation"""
from socket import socket, AF_INET, SOCK_STREAM


ADDRESS = "127.0.0.2"  # Local client is going to be 127.0.0.1
PORT = 4300  # Open http://127.0.0.2:4300 in a browser
LOGFILE = "webserver.log"


def main():
    """Main loop"""
    with socket(AF_INET, SOCK_STREAM) as server_sock:
        pass


if __name__ == "__main__":
    main()
