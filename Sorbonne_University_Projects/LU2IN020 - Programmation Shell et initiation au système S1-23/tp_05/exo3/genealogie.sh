#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Erreur : Aucun PID fourni en paramètre."
    exit 1
fi

pid=$1

if ! ps -p $pid > /dev/null; then
    echo "Erreur : Le PID $pid n'existe pas."
    exit 1
fi

while [ $pid -ne 1 ]; do
    echo $pid
    stat_file="/proc/$pid/stat"
    ppid=$(cut -d ' ' -f 4 $stat_file)
    pid=$ppid
done

echo 1