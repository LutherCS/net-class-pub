# Custom dig

Complete the following programming project and push code to your GitHub repository.

**Process records of type A (IPv4) or AAAA (IPv6) only. If a server returns CNAME record instead, ignore it.**

Use *yahoo.com* as an example of a clean and simple response.

Read the domain name, record type (*A* by default, *AAAA* is acceptable), and an optional DNS server as parameters passed to your program.

```bash
python src/projects/dnsresolver/resolver.py luther.edu
```

or

```bash
python src/projects/dnsresolver/resolver.py luther.edu --server 1.1.1.1
```

or

```bash
python src/projects/dnsresolver/resolver.py yahoo.com -t AAAA -s 8.8.8.8
```

1. Parse command-line arguments and validate user input
   - If the DNS address is not specified, pick one of the well-known public servers
   - If the requested record type is not A or AAAA, raise an error
2. Format a DNS request using the following values:
   - Transaction ID: random
   - Flags: standard query (recursion bit set to 1, other bits are 0)
   - Questions: 1
   - Answer RRs: 0
   - Authority RRs: 0
   - Additional RRs: 0
   - Name: user-provided
   - Type: user-provided
   - Class: IN (0x0001)
3. Create a UDP socket connection and send the request to the DNS server
4. Parse the response message from the DNS server to extract all addresses (there could be more than 1)
5. Print the address of the DNS server used
6. Display the received information in the following format:

```text
Name:    <domain name>
Address: <human-readable address>
TTL:     <received time-to-live>
```

## Testing

```bash
python -m pytest tests/projects/dnsresolver/test_resolver.py
```

## Approach

- Use `argparse` to grab command-line arguments and `parse_cli_query` to parse them into the specified format
- Look at a valid DNS request (eg. ping luther.edu and capture the traffic)
![DNS request](dns_query.png)

- Analyze the structure of a message (see the links below for details) and replicate it
![DNS request](dns_query_hex.png)

- Format your own message, byte by byte (you may want to use Python's bytearray for that)
- Make your client format a message based on user input (domain, record type)
- Send the message and receive the response
- Parse the response and present the result (IP address). Consider simple cases (domain - one or more address(es)), ignore complex paypal-like resolutions with multiple pseudos.

## Functions

> 'Begin at the beginning,' the King said gravely, 'and go on till you come to the end: then stop.'

**This guide is tentative and informational. Rely on the code template and test file for specific implementation details.**

### `val_to_2_bytes(value: int) -> tuple`

`val_to_2_bytes` takes an integer and returns that number converted to a tuple of 2 bytes (numbers between 0 and 255). Use shift (>>) and binary and (&) to extract left and right 8 bits. This function is used extensively as many fields in the DNS request and response are using 2 bytes, even if a value fits 1 byte.

```text
43043 = 0b1010100000100011 => [0b10101000, 0b00100011] = [168, 35]
                                 left 8      right 8
```

### `val_to_n_bytes(value: int, n_bytes: int) -> tuple`

`val_to_n_bytes` takes an integer and the target tuple size, converting the number to a tuple of the specified size. Use shifting (<<, >>) and bit masking (&) in a loop to generate the tuple. You don't have to use this function but it's a great way to learn bitwise operations and it can be an alias for `val_to_2_bytes` if `n_bytes` is set to 2.

```text
430430 = 0b1101001000101011110 => [0b00000110, 0b10010001, 0b01011110] = [6, 145, 94]
                                     left 8      middle 8    right 8
```

### `bytes_to_val(data: bytes) -> int`

`bytes_to_val` takes a list of bytes and returns their value as a single integer. Use shift (<<) and addition in a loop to construct the result. This function is used extensively as many DNS fields are stored in 2 bytes. You should be able to process input lists of any size.

```text
[6, 145, 94] = [0b110, 0b10010001, 0b01011110] => 0b1101001000101011110 = 430430
```

### `get_2_bits(data: bytes) -> int`

`get_2_bits` extracts the leftmost 2 bits from a 2-byte sequence. Use a simple shift to extract the target bits. This function is used to determine whether the domain is stored in the answer as a label or a pointer. See the provided references for details on those two formats.

```text
0xc00c = 0b1100000000001100 => leftmost 2 bits are 0b11 = 3
```

### `get_offset(data: bytes) -> int`

`get_offset` extracts the rightmost 14 bits from a 2-byte sequence. This function can be used to extract the location of the domain name inside a response. Note that a response may contain either labels or pointers, so don't rely on the *magic* of `0xc00c`. A more descriptive name for this function is *get_domain_name_location_within_a_server_response*. Do not confuse the offset found by this function with the offset of answers within the response.

```text
0xc00c = 0b1100000000001100 => rightmost 14 bits are 0b1100= 12
```

### `parse_cli_query(q_domain: str, q_type: str, q_server: str | None = None) -> tuple[list, int, str]`

`parse_cli_query` takes the domain name, a query type, and an optional server address as parameters. It returns a tuple of the domain name (as a list of strings), numeric value of the query type (as found in the `DNS_TYPES` dictionary), and the server address. If the server address is not specified, pick one randomly from the `PUBLIC_DNS_SERVER` collection. If the requested record type is not *A* or *AAAA*, raise a `ValueError`.

### `format_query(q_domain: list, q_type: int) -> bytearray`

`format_query` takes the domain name and the query type as parameters. It builds a query as a bytearray and returns the resulting bytes to be sent to the server. Bytearrays are mutable byte sequences in Python, so you should start with an empty one and use `append` or `extend` to form a valid DNS query. Transaction id should be chosen at random as a vaslue in the 0..65535 range (inclusive). Use default value, `0x100` for the flags. The domain name should be in the **QNAME** format, terminated by `\0`.

```text
56 f0 01 00 00 01 00 00 00 00 00 00 06 6c 75 74 68 65 72 03 65 64 75 00 00 01 00 01
|---| |---| |---| |---| |---| |---| |------------------| |---------| || |---| |---|
|id | |flags, # of questions etc  | | luther           | | edu     | \0 |typ| |cls|
```

### `parse_response(resp_bytes: bytes) -> list`

`parse_response` takes bytes received from the server and returns a list where each item is a tuple of the domain name, the address, and the TTL as extracted from the server's response. This function processes the response header (first 12 bytes and the query), calls `parse_answers` to parse the specific answer(s), and returns the results returned by `parse_answers`. You don't need to validate values in the response (i.e. transaction id and flags) but you have to extract the number of answers from the header and the starting byte of the answers.

### `parse_answers(resp_bytes: bytes, offset: int, rr_ans: int) -> list`

`parse_answers` takes the response message bytes, starting position for the answer(s) within the response, and the number of answers. It returns a list of tuples (domain, address, ttl). Do not confuse the *offset* in this function (a better(?) name would be *number_of_bytes_from_the_beginning_of_the_response_to_the_first_answer*) and the *domain_name_start_offset*. Keep in mind that the domain name may be in different format, *label* or *pointer*. You should be able to process both.

Once you've processed an answer, add the results to the list and move to the next one, if present. Once all the answers are collected, return the list of tuples.

```text
c0 0c 00 01 00 01 00 00 00 05 00 04 ae 81 19 aa
|---| |---| |---| |---------| |---| |---------|
|ptr| |typ| |cls| | ttl     | |len| | address |
```

### `parse_address_a(addr_len: int, addr_bytes: bytes) -> str`

`parse_address_a` extracts IPv4 address from the response and returns it in the dotted-decimal notation.

### `parse_address_aaaa(addr_len: int, addr_bytes: bytes) -> str`

`parse_address_aaaa` extracts IPv6 address from the response and returns it in the hex-colon notation.

### `resolve(query: str) -> None`

`resolve` calls and other functions and prints the results. It is implemented for your convenience.

## Resources

- [RFC 1035 - Domain names - implementation and specification](https://tools.ietf.org/html/rfc1035)
- [The TCP/IP Guide - DNS Messaging and Message, Resource Record and Master File Formats](http://www.tcpipguide.com/free/t_DNSMessagingandMessageResourceRecordandMasterFileF.htm)
- [Chapter 15 DNS Messages](http://www.zytrax.com/books/dns/ch15/)
- [Domain Name System (DNS) Parameters](http://www.iana.org/assignments/dns-parameters/dns-parameters.xhtml)
- [Python Bytes, Bytearray - w3resource](https://www.w3resource.com/python/python-bytes.php)
