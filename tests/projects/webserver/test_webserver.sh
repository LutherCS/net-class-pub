#!/bin/bash
# # `web server` testing using curl

# # @authors: Roman Yasinovskyy
# # @version: 2024.10

addr="127.0.0.2"
port=43080
file="alice30.txt"
testfile="test.txt"

echo -e "\e[34mStarting the server\e[0m"
python src/projects/webserver/server.py -l src/projects/webserver/webserver.log &
pid=`echo $!`
echo -e "Server is running with pid $pid"
sleep 1

echo -e "\e[34mChecking status codes\e[0m"
# Test "200 OK"
exp_code=200
code=`curl -s -o /dev/null -w"%{http_code}" http://$addr:$port/$file`
if [ $code == $exp_code ]; then
  echo -e "200 OK:\t\t\t\e[32mPassed\e[0m"
else
  echo -e "200 OK:\t\t\t\e[31mFailed\e[0m ($code instead of $exp_code)"
fi

# Test "404 Not Found"
exp_code=404
code=`curl -s -o /dev/null -w"%{http_code}" http://$addr:$port/test404.txt`
if [ $code == $exp_code ]; then
  echo -e "404 Not Found:\t\t\e[32mPassed\e[0m"
else
  echo -e "404 Not Found:\t\t\e[31mFailed\e[0m ($code instead of $exp_code)"
fi

# Test "405 Method Not Allowed" by pretending the request is POST
exp_code=405
code=`curl -s -o /dev/null -w"%{http_code}" -X POST http://$addr:$port/test405.txt`
if [ $code == $exp_code ]; then
  echo -e "405 Method Not Allowed:\t\e[32mPassed\e[0m"
else
  echo -e "405 Method Not Allowed:\t\e[31mFailed\e[0m ($code instead of $exp_code)"
fi

# Test "501 Not Implemented" by pretending the request is HEAD
exp_code=501
code=`curl -s -o /dev/null -w"%{http_code}" -X HEAD http://$addr:$port/test501.txt`
if [ $code == $exp_code ]; then
  echo -e "501 Not Implemented:\t\e[32mPassed\e[0m"
else
  echo -e "501 Not Implemented:\t\e[31mFailed\e[0m ($code instead of $exp_code)"
fi

echo -e "\e[34mChecking headers\e[0m"
# Test the HTTP version
exp_version="1.1"
version=`curl -s -o /dev/null -w"%{http_version}" http://$addr:$port/$file`
if [[ $version == $exp_version ]]; then
  echo -e "HTTP version:\t\t\e[32mPassed\e[0m"
else
  echo -e "HTTP version:\t\t\e[31mFailed\e[0m ($version instead of $exp_version)"
fi

# Test the content type
exp_type="text/plain"
type=`curl -s -o /dev/null -w"%{content_type}" http://$addr:$port/$file`
if [[ $type == *"$exp_type"* ]]; then
  echo -e "Content type:\t\t\e[32mPassed\e[0m\t($file)"
else
  echo -e "Content type:\t\t\e[31mFailed\e[0m ($type instead of $exp_type)\t($testfile)"
fi

exp_type="text/plain"
type=`curl -s -o /dev/null -w"%{content_type}" http://$addr:$port/$testfile`
if [[ $type == *"$exp_type"* ]]; then
  echo -e "Content type:\t\t\e[32mPassed\e[0m\t($testfile)"
else
  echo -e "Content type:\t\t\e[31mFailed\e[0m ($type instead of $exp_type)\t($testfile)"
fi

# Test file modification timestamp
exp_datetime="2020-10-15 14:21:49.524000"
datetime=`curl -s -o /dev/null -D - http://$addr:$port/$file | grep -i Last-Modified:`
if [[ $datetime == *"$exp_datetime"* ]]; then
  echo -e "Content timestamp:\t\e[32mPassed\e[0m\t($file)"
else
  echo -e "Content timestamp:\t\e[31mFailed\e[0m ($datetime instead of $exp_datetime)\t($file)"
fi

exp_datetime="2024-10-02 19:11:36.428240"
datetime=`curl -s -o /dev/null -D - http://$addr:$port/$testfile | grep -i Last-Modified:`
if [[ $datetime == *"$exp_datetime"* ]]; then
  echo -e "Content timestamp:\t\e[32mPassed\e[0m\t($testfile)"
else
  echo -e "Content timestamp:\t\e[31mFailed\e[0m ($datetime instead of $exp_datetime)\t($testfile)"
fi

# Test the content size
exp_size=148545
size=`curl -s -o /dev/null -w"%{size_download}" http://$addr:$port/$file`
if [ $size == $exp_size ]; then
  echo -e "Content size:\t\t\e[32mPassed\e[0m\t($file)"
else
  echo -e "Content size:\t\t\e[31mFailed\e[0m ($size instead of $exp_size)\t($file)"
fi

exp_size=6
size=`curl -s -o /dev/null -w"%{size_download}" http://$addr:$port/$testfile`
if [ $size == $exp_size ]; then
  echo -e "Content size:\t\t\e[32mPassed\e[0m\t($testfile)"
else
  echo -e "Content size:\t\t\e[31mFailed\e[0m ($size instead of $exp_size)\t($testfile)"
fi

# Display full header
echo -e "\e[34mChecking full header\e[0m"
curl -s -o /dev/null -D - http://$addr:$port/$file

# Display content tail
echo -e "\e[34mChecking file content\e[0m"
curl -s http://$addr:$port/$file | tail -n 12

kill -9 $pid
echo -e "\e[34mDone testing\e[0m"
