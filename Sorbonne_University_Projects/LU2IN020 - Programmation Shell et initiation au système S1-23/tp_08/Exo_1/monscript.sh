#!/bin/bash

sleep 30 &

PID=$!

echo "Initialisation l'info de ce processus"
ps o pid,ppid,state --pid $PID

wait

echo "L'information de ce processus apres adoption"
ps o pid,ppid,state --pid $PID
