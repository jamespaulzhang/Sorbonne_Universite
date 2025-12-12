#!/bin/bash

# Lancer dd en arrière-plan
dd if=/dev/urandom of=/tmp/iss bs=1b count=5000000 status=progress &

# Afficher l'avancement toutes les secondes
while pidof dd >/dev/null; do
    sleep 1
    pkill -USR1 dd
done
