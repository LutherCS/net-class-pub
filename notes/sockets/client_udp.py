import socket
from socket import SOCK_DGRAM, AF_INET

host = "127.0.0.1"
server = "127.0.0.2"
port = 4300

def main():
    print("Client here")
    with socket.socket(AF_INET, SOCK_DGRAM) as sock:
        while True:
            msg = input("Enter your name: ")
            sock.sendto(msg.encode(), (server, port))
            if msg == "quit":
                break
            response, _ = sock.recvfrom(2048)
            print(f"Received: {response.decode()}")
    print("Client is done")

if __name__ == "__main__":
    main()
