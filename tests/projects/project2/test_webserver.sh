#!/bin/bash

addr="127.0.0.2"
port=4300
file="alice30.txt"

echo -e "\e[34mStarting the server\e[0m"
python src/projects/project2/webserver.py &
pid=`echo $!`
echo -e "Server is running with pid $pid"
sleep 1

echo -e "\e[34mChecking status codes\e[0m"
# Testing 200
exp_code=200
code=`curl -s -o /dev/null -w"%{http_code}" http://$addr:$port/$file`
if [ $code == $exp_code ]; then
  echo -e "200 OK:\t\t\t\e[32mPassed\e[0m"
else
  echo -e "200 OK:\t\t\t\e[31mFailed\e[0m ($code instead of $exp_code)"
fi

# Testing 404
exp_code=404
code=`curl -s -o /dev/null -w"%{http_code}" http://$addr:$port/test404.txt`
if [ $code == $exp_code ]; then
  echo -e "404 Not Found:\t\t\e[32mPassed\e[0m"
else
  echo -e "404 Not Found:\t\t\e[31mFailed\e[0m ($code instead of $exp_code)"
fi

# Testing 405
exp_code=405
code=`curl -s -o /dev/null -w"%{http_code}" -X POST http://$addr:$port/test405.txt`
if [ $code == $exp_code ]; then
  echo -e "405 Method Not Allowed:\t\e[32mPassed\e[0m"
else
  echo -e "405 Method Not Allowed:\t\e[31mFailed\e[0m ($code instead of $exp_code)"
fi

# Testing 501
exp_code=501
code=`curl -s -o /dev/null -w"%{http_code}" -I http://$addr:$port/test501.txt`
if [ $code == $exp_code ]; then
  echo -e "501 Not Implemented:\t\e[32mPassed\e[0m"
else
  echo -e "501 Not Implemented:\t\e[31mFailed\e[0m ($code instead of $exp_code)"
fi

echo -e "\e[34mChecking headers\e[0m"
# Testing various options
exp_size=148545
size=`curl -s -o /dev/null -w"%{size_download}" http://$addr:$port/$file`
if [ $size == $exp_size ]; then
  echo -e "Content size:\t\t\e[32mPassed\e[0m"
else
  echo -e "Content size:\t\t\e[31mFailed\e[0m ($size instead of $exp_size)"
fi

exp_type="text/plain"
type=`curl -s -o /dev/null -w"%{content_type}" http://$addr:$port/$file`
if [[ $type == *"$exp_type"* ]]; then
  echo -e "Content type:\t\t\e[32mPassed\e[0m"
else
  echo -e "Content type:\t\t\e[31mFailed\e[0m ($type instead of $exp_type)"
fi

exp_version="1.1"
version=`curl -s -o /dev/null -w"%{http_version}" http://$addr:$port/$file`
if [[ $version == $exp_version ]]; then
  echo -e "HTTP version:\t\t\e[32mPassed\e[0m"
else
  echo -e "HTTP version:\t\t\e[31mFailed\e[0m ($version instead of $exp_version)"
fi

# Display full header
echo -e "\e[34mChecking full header\e[0m"
curl -s -o /dev/null -D - http://$addr:$port/$file

# Display content tail
echo -e "\e[34mChecking file content\e[0m"
curl -s http://$addr:$port/$file | tail

kill -9 $pid
echo -e "\e[34mDone testing\e[0m"
