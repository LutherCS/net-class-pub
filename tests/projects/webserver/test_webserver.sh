#!/bin/bash
# Server testing with curl

# @author: Roman Yasinovskyy
# @version: 2026.9
# @usage: ./test_webserver.sh
# curl options:
#       -o: output file
#       -s: silent mode
#       -w: display specific information (http response code)
#       -d: send data (e.g n=430)
#       -D: dump header

addr="127.0.0.1"
port=4380
file="alice30.txt"
testfile="test26.txt"

passed_tests=0
failed_tests=0

echo -e "\e[1;44mEnd-to-end testing of the web server using $testfile and $file\e[0m"
echo -e "\e[34mStarting the server\e[0m"
python src/projects/webserver/server.py -l src/projects/webserver/webserver.log &
pid=`echo $!`
echo -e "Server is running with pid $pid"
sleep 1

echo -e "\e[34mChecking status codes\e[0m"
# Test "200 OK"
# curl http://localhost:4380/test26.txt
exp_code=200
code=`curl -s -o /dev/null -w"%{http_code}" http://$addr:$port/$testfile`
if [ $code == $exp_code ]; then
  echo -e "200 OK:\t\t\t\t\e[32mPassed\e[0m"
  ((passed_tests++))
else
  echo -e "200 OK:\t\t\t\t\e[31mFailed\e[0m ($code instead of $exp_code)"
  ((failed_tests++))
fi

# Test "204 No Content"
# curl http://localhost:4380/test26.txt -X DELETE
exp_code=204
code=`curl -s -o /dev/null -w"%{http_code}" http://$addr:$port/$testfile -X DELETE`
if [ $code == $exp_code ]; then
  echo -e "204 No content:\t\t\t\e[32mPassed\e[0m"
  ((passed_tests++))
else
  echo -e "204 No Content:\t\t\t\e[31mFailed\e[0m ($code instead of $exp_code)"
  ((failed_tests++))
fi

# Test "301 Moved Permanently"
# curl http://localhost:4380/test.txt
exp_code=301
code=`curl -s -o /dev/null -w"%{http_code}" http://$addr:$port/test.txt`
if [ $code == $exp_code ]; then
  echo -e "301 Moved Permanently:\t\t\e[32mPassed\e[0m"
  ((passed_tests++))
else
  echo -e "301 Moved Permanently:\t\t\e[31mFailed\e[0m ($code instead of $exp_code)"
  ((failed_tests++))
fi

# Test "404 Not Found"
# curl http://localhost:4380/test404.txt
exp_code=404
code=`curl -s -o /dev/null -w"%{http_code}" http://$addr:$port/test404.txt`
if [ $code == $exp_code ]; then
  echo -e "404 Not Found:\t\t\t\e[32mPassed\e[0m"
  ((passed_tests++))
else
  echo -e "404 Not Found:\t\t\t\e[31mFailed\e[0m ($code instead of $exp_code)"
  ((failed_tests++))
fi

# Test "405 Method Not Allowed"
# curl http://localhost:4380/test26.txt -I
exp_code=405
code=`curl -s -o /dev/null -w"%{http_code}" http://$addr:$port/$testfile -I`
if [ $code == $exp_code ]; then
  echo -e "405 Method Not Allowed:\t\t\e[32mPassed\e[0m"
  ((passed_tests++))
else
  echo -e "405 Method Not Allowed:\t\t\e[31mFailed\e[0m ($code instead of $exp_code)"
  ((failed_tests++))
fi

# Test "418 I'm a teapot"
# curl http://localhost:4380/test26.txt -X POST
exp_code=418
code=`curl -s -o /dev/null -w"%{http_code}" http://$addr:$port/$testfile -X POST`
if [ $code == $exp_code ]; then
  echo -e "418 I'm a teapot:\t\t\e[32mPassed\e[0m"
  ((passed_tests++))
else
  echo -e "418 I'm a teapot:\t\t\e[31mFailed\e[0m ($code instead of $exp_code)"
  ((failed_tests++))
fi

# Test "501 Not Implemented"
# curl http://localhost:4380/test26.txt -X PUT
exp_code=501
code=`curl -s -o /dev/null -w"%{http_code}" http://$addr:$port/$testfile -X PUT`
if [ $code == $exp_code ]; then
  echo -e "501 Not Implemented:\t\t\e[32mPassed\e[0m"
  ((passed_tests++))
else
  echo -e "501 Not Implemented:\t\t\e[31mFailed\e[0m ($code instead of $exp_code)"
  ((failed_tests++))
fi

# Test "505 HTTP Version Not Supported"
# curl http://localhost:4380/test26.txt --http1.0
exp_code=505
code=`curl -s -o /dev/null -w"%{http_code}" http://$addr:$port/$testfile --http1.0`
if [ $code == $exp_code ]; then
  echo -e "505 HTTP Version Not Supported:\t\e[32mPassed\e[0m"
  ((passed_tests++))
else
  echo -e "505 HTTP Version Not Supported:\t\e[31mFailed\e[0m ($code instead of $exp_code)"
  ((failed_tests++))
fi

echo
# Working with a testfile
echo -e "\e[35m>$testfile\e[0m"
echo -e "\e[34mChecking headers\e[0m"

# Test HTTP version
exp_version="1.1"
version=`curl -s -o /dev/null -w"%{http_version}" http://$addr:$port/$testfile`
if [[ $version == $exp_version ]]; then
  echo -e "HTTP version:\t\t\t\e[32mPassed\e[0m"
  ((passed_tests++))
else
  echo -e "HTTP version:\t\t\t\e[31mFailed\e[0m ($version instead of $exp_version)"
  ((failed_tests++))
fi

# Test content type
exp_type="text/plain"
type=`curl -s -o /dev/null -w"%{content_type}" http://$addr:$port/$testfile`
if [[ $type == *"$exp_type"* ]]; then
  echo -e "Content type:\t\t\t\e[32mPassed\e[0m"
  ((passed_tests++))
else
  echo -e "Content type:\t\t\t\e[31mFailed\e[0m ($type instead of $exp_type)"
  ((failed_tests++))
fi

# Test file modification timestamp
exp_datetime="2024-10-02 19:11:36.428240"
datetime=`curl -s -o /dev/null -D - http://$addr:$port/$testfile | grep -i Last-Modified:`
if [[ $datetime == *"$exp_datetime"* ]]; then
  echo -e "Content timestamp:\t\t\e[32mPassed\e[0m"
  ((passed_tests++))
else
  echo -e "Content timestamp:\t\t\e[31mFailed\e[0m ($datetime instead of $exp_datetime)"
  ((failed_tests++))
fi

# Test content size
exp_size=6
size=`curl -s -o /dev/null -w"%{size_download}" http://$addr:$port/$testfile`
if [ $size == $exp_size ]; then
  echo -e "Content size:\t\t\t\e[32mPassed\e[0m"
  ((passed_tests++))
else
  echo -e "Content size:\t\t\t\e[31mFailed\e[0m ($size instead of $exp_size)"
  ((failed_tests++))
fi

# Display full header
echo
echo -e "\e[1;34mChecking full header\e[0m"
curl -s -o /dev/null -D - http://$addr:$port/$testfile

# Display content tail
echo -e "\e[1;34mChecking file content\e[0m"
curl -s http://$addr:$port/$testfile | tail -n 12

echo
# Working with Alice in Wonderland
echo -e "\e[35m>$file\e[0m"
echo -e "\e[34mChecking headers\e[0m"

# Test HTTP version
exp_version="1.1"
version=`curl -s -o /dev/null -w"%{http_version}" http://$addr:$port/$file`
if [[ $version == $exp_version ]]; then
  echo -e "HTTP version:\t\t\t\e[32mPassed\e[0m"
  ((passed_tests++))
else
  echo -e "HTTP version:\t\t\t\e[31mFailed\e[0m ($version instead of $exp_version)"
  ((failed_tests++))
fi

# Test t content type
exp_type="text/plain"
type=`curl -s -o /dev/null -w"%{content_type}" http://$addr:$port/$file`
if [[ $type == *"$exp_type"* ]]; then
  echo -e "Content type:\t\t\t\e[32mPassed\e[0m"
  ((passed_tests++))
else
  echo -e "Content type:\t\t\t\e[31mFailed\e[0m ($type instead of $exp_type)"
  ((failed_tests++))
fi

# Test file modification timestamp
exp_datetime="2020-10-15 14:21:49.524000"
datetime=`curl -s -o /dev/null -D - http://$addr:$port/$file | grep -i Last-Modified:`
if [[ $datetime == *"$exp_datetime"* ]]; then
  echo -e "Content timestamp:\t\t\e[32mPassed\e[0m"
  ((passed_tests++))
else
  echo -e "Content timestamp:\t\t\e[31mFailed\e[0m ($datetime instead of $exp_datetime)"
  ((failed_tests++))
fi

# Test content size
exp_size=148545
size=`curl -s -o /dev/null -w"%{size_download}" http://$addr:$port/$file`
if [ $size == $exp_size ]; then
  echo -e "Content size:\t\t\t\e[32mPassed\e[0m"
  ((passed_tests++))
else
  echo -e "Content size:\t\t\t\e[31mFailed\e[0m ($size instead of $exp_size)"
  ((failed_tests++))
fi

# Display full header
echo -e "\e[1;34mChecking full header\e[0m"
curl -s -o /dev/null -D - http://$addr:$port/$file

# Display content tail
echo -e "\e[1;34mChecking file content\e[0m"
curl -s http://$addr:$port/$file | tail -n 12

kill -9 $pid
echo -e "\e[32mPassed tests:$passed_tests\e[0m"
echo -e "\e[31mFailed tests:$failed_tests\e[0m"
echo -e "\e[34mDone testing\e[0m"
