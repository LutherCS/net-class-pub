"""Simple server program"""
import argparse
import logging
import socket

HOST = "127.0.0.1"
PORT = 4300


def format(message: str) -> bytes:
    """Convert (encode) the message to bytes"""
    raise NotImplementedError


def parse(data: bytes) -> str:
    """Convert (decode) bytes to a string"""
    raise NotImplementedError


def server_loop():
    print("The server has started")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        logging.info(f"Binding to {HOST}:{PORT}")
        sock.bind((HOST, PORT))
        logging.info(f"Bound to {HOST}:{PORT}")
        sock.listen(1)
        logging.info(f"Listening on port {PORT}")
        conn, addr = sock.accept()
        with conn:
            logging.info(f"Accepted connection from {addr[0]}:{addr[1]}")
            while True:
                data_in = conn.recv(1024)
                if not data_in:
                    logging.info("Connection closed")
                    break
                message = parse(data_in)
                logging.info(f"Received: {message}")
                logging.info("Sending response...")
                data_out = format(message)
                conn.sendall(data_out)
    print("The server has finished")


def main():
    arg_parser = argparse.ArgumentParser(description="Enable debugging")
    arg_parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable logging.DEBUG mode"
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
