#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <nombre>"
  exit 1
fi

n=$1

if [ "$n" -le 0 ]; then
  echo "Le nombre doit être strictement positif."
  exit 1
fi

trap 'echo "Ola : O"' SIGCONT

for i in $(seq $((n-1)) -1 1); do
  ./ring.sh $i &
  pid[$i]=$!
  kill -STOP ${pid[$i]}
done

sleep 1
kill -CONT ${pid[$n]}
kill -STOP $!

for i in $(seq 1 10); do
  for j in $(seq $((n-1)) -1 1); do
    kill -CONT ${pid[$j]}
    wait ${pid[$j]}
    kill -STOP ${pid[$j]}
  done
  kill -CONT ${pid[$n]}
  wait ${pid[$n]}
  kill -STOP $!
done

