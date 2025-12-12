#!/bin/bash

# Function to be called when a signal is received
no_exit() {
    echo "Il ne doit en rester qu'un."
}

# Ignore all signals
for ((sig=1; sig <= 64; sig++)); do
    trap 'no_exit' $sig
done

# Infinite loop displaying the message
while true; do
    echo "Il ne doit en rester qu'un."
    sleep 1
done