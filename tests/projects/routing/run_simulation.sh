#!/usr/bin/env bash

echo -e "\e[34mStarting the simulation\e[0m"

python src/projects/routing/udp_router.py -c data/projects/routing/network_simple.txt 127.0.0.1 &
pid1=`echo $!`
sleep 1

python src/projects/routing/udp_router.py -c data/projects/routing/network_simple.txt 127.0.0.2 &
pid2=`echo $!`
sleep 1

python src/projects/routing/udp_router.py -c data/projects/routing/network_simple.txt 127.0.0.3 &
pid3=`echo $!`
sleep 1

python src/projects/routing/udp_router.py -c data/projects/routing/network_simple.txt 127.0.0.4 &
pid4=`echo $!`
sleep 1

sleep 30
kill -9 $pid1
kill -9 $pid2
kill -9 $pid3
kill -9 $pid4

echo -e "\e[34mSimulation is over\e[0m"
