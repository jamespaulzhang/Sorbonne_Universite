#!/bin/bash

if [ "$#" -ne 1 ];then
    echo "Usage: $0 <PID>"
    exit 1;
fi

while ps -p $1 &> /dev/null;do
    sleep 1
done

echo "Le processus est devenu zombie !!!"

    
