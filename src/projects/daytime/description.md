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

59890 22-11-07 14:05:58 00 0 0  54.9 UTC(NIST) * 
Connection closed by foreign host.
```

## Requirements

1. Client and server must me implemented using **different** languages (e.g. client in Python / server in Java, client in Java / server in C++ etc.)
2. Server must take protocol (TCP or UDP) as command-line argument and listen on port 13 using the specified protocol.
3. Client must take server name and protocol (TCP or UDP) as command-line arguments.

## Example

```bash
telnet localhost 13
Sunday, November 6, 2022 18:21:37-CST
```
