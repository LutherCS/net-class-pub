# Daytime

Implement client and server that would communicate using Daytime protocol as defined in [RFC 867: Daytime Protocol](https://www.rfc-editor.org/rfc/rfc867).

## Approach

You should implement the server part first and use `telnet` to verify the its functionality.
Once the server is known to be working using TCP, implement the TCP part of the client and use the same logic (formatting/parsing) to implement the UDP part of the client.
Once the client is know to be working, implement the UDP part of the server.

You can use `telnet` to send daytime request and capture the response with Wireshark.

```bash
$ telnet india.colorado.edu 13
Trying 128.138.140.44...
Connected to india.colorado.edu.
Escape character is '^]'.

60634 24-11-20 16:09:52 00 0 0 731.8 UTC(NIST) * 
Connection closed by foreign host.
```

## Requirements

1. Client and server must be implemented using **different** languages (e.g. client in Python / server in Java, client in JavaScript / server in C++ etc.)
2. Server must take protocol (TCP or UDP) and port number as command-line arguments and listen on the specified port using the specified protocol.
3. Client must take protocol (TCP or UDP), port number, and server address/name, as command-line arguments.

## Example

```bash
$ python server.py --help
usage: server.py [-h] [-t] [-u] [-p PORT] [-d]

options:
  -h, --help            show this help message and exit
  -t, --tcp             use TCP
  -u, --udp             use UDP
  -p PORT, --port PORT  port to use
```

Run the server

```bash
$ python server.py --tcp -p 43013
Starting a TCP server on port 13
```

```bash
$ python server.py --udp -p 43013
Starting a UDP server on port 43013
```

Test the server

```bash
$ telnet 127.0.1.1 43013
Trying 127.0.1.1...
Connected to 127.0.1.1.
Escape character is '^]'.
2024-11-20T10:20:59.809957
Connection closed by foreign host.
```

Use the client

```bash
$ python client.py --help               
usage: client.py [-h] [-t] [-u] [-p PORT] [-d] server

Parse arguments

positional arguments:
  server                Server to query

options:
  -h, --help            show this help message and exit
  -t, --tcp             use TCP
  -u, --udp             use UDP
  -p PORT, --port PORT  port to use
```
