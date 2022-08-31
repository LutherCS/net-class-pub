# Greeting client/server

For this project you need to implement functions `format` and `parse` in files *src/projects/project0/client.py* and *src/projects/project0/server.py* and verify the correctness of your implementation by passing the provided tests. The biggest challenge, of course, is the conversion between strings and bytes. You should use the type annotations and test files to determine the expected output of a function.

This assignment (mostly) follows the general pattern we are going to see in other projects:

1. Client-server communication
2. Breaking code into functions with the following purposes:
   - Collect a message
   - Format the message into data
   - Send data
   - Receive data
   - Parse data into a meaningful message
   - Present the message

3. Test the program functionality and correctness

## Learning goals

- Get familiar with *git* and the course repository
- Get familiar with logging, argument parser, and type annotations
- Start using unit tests
- Use type annotations, doc strings, and tests to better understand the purpose of each function

## Implementation details

1. The client is expected to take **name** as a command-line parameter and send *Hello, my name is **name*** to the server.
2. The server is expected to receive a message *Hello, my name is **name*** and return a message *Hello, **name***.
3. Both client and server disconnect after this exchange.
4. The main event loop on both ends is implemented, your goal is to implement `format` and `parse` functions and pass the provided tests.

## Testing the implementation

    python3 -m pytest tests/projects/project0/

If you want to enable verbose output, use flag `-v`

    python3 -m pytest -v tests/projects/project0/

## Running the server

    python3 src/projects/project0/server.py

If you want to enable debugging/informational messages, use flag `-d`

    python3 src/projects/project0/server.py -d

## Running the client

    python3 src/projects/project0/client.py Avatar Aang

If you want to enable debugging/informational messages, use flag `-d`

    python3 src/projects/project0/client.py Avatar Aang -d

## Capturing the exchange

Use Wireshark to capture the exchange and add the resulting file to your repository.

## References

- [argparse — Parser for command-line options, arguments and sub-commands — Python 3.8.6 documentation](https://docs.python.org/3/library/argparse.html)
- [logging — Logging facility for Python — Python 3.8.6 documentation](https://docs.python.org/3/library/logging.html)
- [socket — Low-level networking interface — Python 3.8.6 documentation](https://docs.python.org/3/library/socket.html)
- [Wireshark · Go Deep.](https://www.wireshark.org/)
- [Home · Wiki · Wireshark Foundation / wireshark · GitLab](https://gitlab.com/wireshark/wireshark/-/wikis/home)
