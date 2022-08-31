# The Story about Ping

Implement a *ping* application using ICMP request and reply messages. You have to use Python's *RAW* sockets to properly send ICMP messages. You should complete the provided ping application so that it sends 5 Echo requests to each RIR (ARIN, RIPE, LACNIC, AFRINIC, APNIC), 1 request every second. Each message contains a payload of data that includes a timestamp. After sending each packet, the application waits up to *one second* to receive a reply. If the one-second timer expires, assume the packet is lost or the server is down. Report the following statistics for each host:

* packet loss
* maximum round-trip time
* minimum RTT
* average RTT
* RTT standard deviation

The output of this application should be similar (preferably, identical) to the output of the Linux `ping` command. An example can be found in *tests/projects/pinger/pinger.txt*.

## General implementation notes

You need to receive the structure ICMP_ECHO_REPLY and fetch the information you need, such as checksum, sequence number, time to live (TTL), etc.

Seeing that some functions are already implemented, you main goals for this project are as follows:

* understand what's already implemented and write new code that would integrate with the existing codebase
* use `struct` to format and parse message
* use `select` to manage incoming and outgoing queues of messages
* use *ICMP* and *raw* sockets

This application requires the use of raw sockets. You may need administrator/root privileges to run your program.

When running this application as a root, make sure to use `python3.8`.

## Functions

### Can be used without modification

* `bytes_to_str`: auxiliary function, useful for debugging. Takes (received) *packet bytes* as an argument.
* `checksum`: calculates packet checksum. Takes *packet bytes* as an argument.
* `format_request`: formats echo request. Takes *request id* and *sequence number* as arguments amd returns packet data.
* `send_request`: creates a socket and uses sends a message prepared by `format_request`.

### Must be implemented/modified

* `parse_reply`: receives and parses an echo reply. Takes the following arguments: *socket*, *request id*, *timeout*, and the *destination address*. Returns a tuple of the *destination address*, *packet size*, *roundtrip time*, *time to live*, and *sequence number*. This function should raise an error if the response message type, code, or checksum are incorrect.

| 0    |      | 15       |     |
| ---- | ---- | -------- | --- |
| type | code | checksum |
| id   |      | sequence |

* `ping`: main loop. Takes a *destination host*, *number of packets to send*, and *timeout* as arguments. Displays host statistics.

## Running

```bash
sudo python3.8 src/projects/pinger/pinger.py
```

## Testing

```bash
python -m pytest tests/projects/pinger/test_pinger.py
```

## References

* [socket — Low-level networking interface — Python 3.9.0 documentation](https://docs.python.org/3/library/socket.html)
* [https://sock-raw.org/papers/sock_raw](https://sock-raw.org/papers/sock_raw)
* [TCP/IP Raw Sockets | Microsoft Docs](https://docs.microsoft.com/en-us/windows/desktop/WinSock/tcp-ip-raw-sockets-2)
* [Converting between Structs and Byte Arrays – GameDev<T>](http://genericgamedev.com/general/converting-between-structs-and-byte-arrays/)
* [select — Waiting for I/O completion — Python 3.9.0 documentation](https://docs.python.org/3/library/select.html)
* [How to Work with TCP Sockets in Python (with Select Example)](https://steelkiwi.com/blog/working-tcp-sockets/)
* [select — Wait for I/O Efficiently — PyMOTW 3](https://pymotw.com/3/select/)
