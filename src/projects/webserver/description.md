# Simple Web Server

For this project you are going to write a simple web server using Python sockets only (i.e. no `Flask`, not even `http.server`). Your server should have the following functionality:

1. Bind to TCP port *43080* on *127.0.0.2* and accept 1 request at a time
2. Log details of each incoming request to *webserver.log*
3. Return *200 OK* status message as a response to a valid request (e.g. /alice30.txt).
4. Return *404 Not Found* error for any *GET* request if the file is not in *data/projects/webserver/*
5. Return *405 Method Not Allowed* error for the *POST* method
6. Return *501 Not Implemented* error for any method other than *GET* or *POST*
7. Send the content of the requested file to the client along with proper response header

## Request

A typical request header sent by a browser (Chrome in this case) looks as follows:

```text
GET /alice30.txt HTTP/1.1
Host: 127.0.0.2:43080
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9

```

## Log

Log file should contain the following information:

1. Time of the request.
2. Requested file.
3. IP address of the client.
4. Browser vendor and version.

```text
2024-10-02 18:45:53.094734 | /alice.txt | 127.0.0.1 | Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0
2024-10-02 18:45:53.129352 | /favicon.ico | 127.0.0.1 | Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0
2024-10-02 18:46:11.503072 | /alice30.txt | 127.0.0.1 | Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0
2024-10-02 18:50:45.930996 | /alice30.txt | 127.0.0.1 | curl/8.5.0
2024-10-02 18:50:45.938917 | /test404.txt | 127.0.0.1 | curl/8.5.0
2024-10-02 18:50:45.942959 | /test405.txt | 127.0.0.1 | curl/8.5.0
2024-10-02 18:50:45.946633 | /test501.txt | 127.0.0.1 | curl/8.5.0

```

## Response

Your server must include the following headers in the response:

1. `HTTP version`: 1.1
2. `Response code`: 200 OK (or another *valid* HTTP response code)
3. `Content-Length`: length of the requested file
4. `Content-Type`: plain text (**not** html)
5. `Date`: current date
6. `Last-Modified`: modification time of the requested file (get this information from file)
7. `Server`: CS430/2024

The response header sent by your server should look as follows:

```text
HTTP/1.1 200 OK
Date: 2024-10-02 19:53:18.150733
Server: CS430/2024
Content-Type: text/plain; charset=utf-8
Last-Modified: 2020-10-15 14:21:49.524000
Content-Length: 148545

```

In case of the client-side errors (*404 Not Found* and *405 Method Not Allowed*) the server should return HTML code in the following format:

```html
<html><head></head><body><h1>ERROR MESSAGE</h1></body></html>
```

See the test file for details of the message.

## Testing

```bash
python -m pytest tests/projects/webserver/test_server.py
```

```bash
tests/projects/webserver/test_webserver.sh
```

## References

* [RFC 7231 - Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content](https://tools.ietf.org/html/rfc7231)
* [HTTP response status codes - HTTP | MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
* [Request header - MDN Web Docs Glossary: Definitions of Web-related terms | MDN](https://developer.mozilla.org/en-US/docs/Glossary/Request_header)
* [Response header - MDN Web Docs Glossary: Definitions of Web-related terms | MDN](https://developer.mozilla.org/en-US/docs/Glossary/Response_header)
* [Alice's Adventures in Wonderland](www.umich.edu/~umfandsf/other/ebooks/alice30.txt)
