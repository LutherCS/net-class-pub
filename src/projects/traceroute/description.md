# Tracing the Route

Implement `traceroute` (`tracert`) utility.

Language of implementation: any.

Use ICMP socket to send probing messages to the specified host.

Display relevant statistics of the probe, similar to the `tracert` utility on Windows.

Python implementation is provided, with lines of code sorted in ascending order for the convenience of search.

This project is supposed to work (and will be graded) on *Ubuntu 18.04* and may not work on other platforms. It definitely **DOES NOT** work on Mac (see BUGS section of the FreeBSD man pages).

## C++

```bash
g++ --std=gnu++14 traceroute.cpp -o traceroute.out
./traceroute.out example.com
```

## Java

```bash
javac Traceroute.java
java Traceroute example.com
```

## Python

```bash
sudo python3.8 src/projects/tracepath/traceroute.py example.com
```

### Functions

* `checksum`: takes *packet* as an argument and returns its Internet **checksum**.

* `format_request`: takes *request ID* and *sequence number* as arguments and returns a properly formatted **ICMP request packet** with *VOTE!* as *data*. This function has to compute the packet's *checksum* and add it to the header of the outgoing message.

* `send_request`: takes *socket*, *packet bytes*, *destination address*, and *Time-to-Live* value as arguments, sends the specified data to the address, and returns current time. This function sets the socket's time-to-live option to the supplied value.

* `receive_reply`: takes a *socket* as an argument and returns a tuple of the *received packet*, responding host's  *address* (it's another tuple!), and current time.

* `parse_reply`: takes a *packet* as an argument and raises `ValueError` (with different messages) if it is not properly formatted. This function parses the response header and verifies that the *ICMP type* is 0, 3, 8, or 11; *ICMP code* matches the type; validates the received checksum.

* `traceroute`: takes *hostname* (domain) name (and an optional number of max hops) as arguments and traces a path to that host. The general approach is to have a big loop that sends *ICMP Echo Request* messages to the host, incrementally increasing TTL value until the host responds or we reach the *max hops* limit. Each iteration of this loop generates 3 messages. There are two possible sources of errors: `Timeout` (response was not received within *1 sec*) and `Value` (something is wrong with the response). For each attempt you should do the following:
    1. Format an ICMP Request
    2. Send the request to the destination host
    3. Receive a response (may or may not be a proper ICMP Reply)
    4. Parse the response and check for errors
    5. Print the relevant statistics, if possible
    6. Print the error message, if any
    7. Stop the probe after 30 attempts or once a response from the destination host is received

* `main`: parses command line arguments, sets up logger, and starts the probe.

## References

* [Traceroute - Wikipedia](https://en.wikipedia.org/wiki/Traceroute)
* [traceroute(8) - Linux man page](https://linux.die.net/man/8/traceroute)
* [Ping, traceroute, and netstat: The network troubleshooting trifecta | Enable Sysadmin](https://www.redhat.com/sysadmin/ping-traceroute-netstat)
* [Internet Control Message Protocol (ICMP) Parameters](https://www.iana.org/assignments/icmp-parameters/icmp-parameters.xhtml)
* [Linux Howtos: C/C++ -> Sockets Tutorial](http://www.linuxhowtos.org/C_C++/socket.htm)
* [Socket (Java SE 10 & JDK 10 )](https://docs.oracle.com/javase/10/docs/api/java/net/Socket.html)
* [socket — Low-level networking interface — Python 3.7.1 documentation](https://docs.python.org/3/library/socket.html)
* [macos - Mac changes IP total length field - Stack Overflow](https://stackoverflow.com/questions/13829712/mac-changes-ip-total-length-field)
* [ip(4) [freebsd man page]](https://www.unix.com/man-page/FreeBSD/4/ip/)
