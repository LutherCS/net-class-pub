import socket
from socket import SOCK_STREAM, AF_INET

host = "127.0.0.2"
port = 4300

def main():
    print("Server here")
    sock = socket.socket(AF_INET, SOCK_STREAM)
    sock.bind((host, port))
    sock.listen()
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
