# Daytime

Implement client and server that would communicate using Daytime protocol as defined in [RFC 867: Daytime Protocol](https://www.rfc-editor.org/rfc/rfc867).

## Approach

You should implement the server part first and use `telnet` to verify the its functionality.
Once the server is known to be working using TCP, implement the TCP part of the client and use the same logic (formatting/parsing) to implement the UDP part of the client.
Once the client is know to be working, implement the UDP part of the server.

You can use `telnet` to send daytime request and capture the response with Wireshark.
Respect the [usage guidelines](https://tf.nist.gov/tf-cgi/servers.cgi) posted by NIST when accessing _time.nist.gov_.

```bash
$ telnet time.nist.gov 13
Trying 132.163.97.3...
Connected to time.nist.gov.
Escape character is '^]'.

61339 26-10-26 13:51:19 07 0 0 306.9 UTC(NIST) *
Connection closed by foreign host.
```

## Requirements

1. Client and server must be implemented using **different** languages (e.g. client in Kotlin / server in PHP, client in Lua / server in C++ etc.) with the following limitation:
   - Python cannot be used at all
   - Only one of Java, JavaScript, or TypeScript can be used to implement either the server or the client.
2. Server must take protocol (TCP or UDP) and port number as command-line arguments and listen on the specified port using the specified protocol.
3. Client must take protocol (TCP or UDP), port number, and server address/name, as command-line arguments.

## Example

### Using the server

```bash
$ python server.py --help
usage: server.py [-h] [-t] [-u] [-p PORT] [-d]

options:
  -h, --help            show this help message and exit
  -t, --tcp             use TCP
  -u, --udp             use UDP
  -p PORT, --port PORT  port to use
```

### Running the server

```bash
$ python server.py --tcp -p 4313
Starting a TCP server on port 13
```

### Using `telnet` to query the server

```bash
$ telnet 127.0.1.1 4313
Trying 127.0.1.1...
Connected to 127.0.1.1.
Escape character is '^]'.
2026-10-26T08:52:01.846455
Connection closed by foreign host.
```

### Using the client

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

### Using the client to query _time.nist.gov_

```bash
$ python client.py -t time.nist.gov
Starting a TCP client

61339 26-10-26 13:58:06 07 0 0 23.7 UTC(NIST) *

Client closed
```
