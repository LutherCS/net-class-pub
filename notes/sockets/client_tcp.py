import socket
from socket import SOCK_STREAM, AF_INET

host = "127.0.0.1"
server = "127.0.0.2"
port = 4300

def main():
    print("Client here")
    with socket.socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect((server, port))
        while True:
            msg = input("Enter your name: ")
            if msg == "quit":
                break
            sock.send(msg.encode())
            response = sock.recv(2048).decode()
            print(f"Received: {response}")
    print("Client is done")


if __name__ == "__main__":
    main()
