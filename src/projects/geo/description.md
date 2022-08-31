# Geography server

Your goal is to implement a client/server application with two sides communicating over *UDP*. The server should read a list of countries and their capitals from the file specified as a command-line argument (*world.csv*), wait for the client's query (a country name), and respond with the capital, if possible. The client should read user input, send it to the server, and wait for the response.

This exchange should continue until the user enters "BYE", at which point both sides should quit gracefully. Note that some countries have multiple names (e.g. United States of America or USA) and/or capitals (e.g. South Africa). Those are separated by commas in the data file.

The tricky part is the implementation of the *graceful* disconnect since UDP does not have a *connection* to begin with. Your job is to figure out how to terminate the session on both ends, client's and server's.

For this project you need to implement functions `read_file`, `find_capital`, `format` and `parse` and verify the correctness of your implementation by passing the provided tests. You also need to complete the `client_loop` and `server_loop` for your applications to run correctly.

## Learning goals

- Implement a client-server networking application
- Use UDP as a transport protocol
- Get familiar with file parsing
- Use unit tests to verify the program functionality

## Implementation details

1. The client is expected to take no command-line argument except an optional `debug`.
2. The server is expected to take file name as a command-line argument and an optional `debug`.
3. The server is expected to receive a message *name* and return a message *capital(s)* without any additional formatting.
4. Both client and server disconnect once the user enters *BYE*.

## Testing the implementation

    python3 -m pytest tests/projects/project1/

If you want to enable verbose output, use flag `-v`

    python3 -m pytest -v tests/projects/project1/

## Running the server

    python3 src/projects/project1/server.py --file world.csv

If you want to enable debugging/informational messages, use flag `--debug`

    python3 src/projects/project1/server.py --file worlds.csv --debug

## Running the client

    python3 src/projects/project1/client.py

If you want to enable debugging/informational messages, use flag `--debug`

    python3 src/projects/project1/client.py --debug

## Capturing the exchange

Not required for this project but may help you during the debugging phase.

## References

- [Alphabetical List of World Countries and Capitals – Bold Tuesday](https://www.boldtuesday.com/pages/alphabetical-list-of-all-countries-and-capitals-shown-on-list-of-countries-poster)
- [csv — CSV File Reading and Writing — Python 3.8.6 documentation](https://docs.python.org/3/library/csv.html)
