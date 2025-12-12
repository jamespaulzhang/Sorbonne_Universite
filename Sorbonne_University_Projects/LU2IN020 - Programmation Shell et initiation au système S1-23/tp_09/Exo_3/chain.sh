#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Usage: $0 <nombre>"
  exit 1
fi

n=$1

if [ $n -le 0 ]; then
  echo "Le nombre doit être strictement positif."
  exit 1
fi

spaces=""
for ((i = 0; i < n; i++)); do
  spaces+=" "
done

echo "Ola :$spaces O"

if [ $n -gt 1 ]; then
  ./chain.sh $((n-1))
fi
