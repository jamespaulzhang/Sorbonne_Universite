#!/bin/bash

# Lancer dd en arrière-plan
dd if=/dev/urandom of=/tmp/iss bs=1b count=5000000 &

# Attendre une seconde
sleep 1

# Envoyer un signal SIGUSR1 au processus dd
pid=$(pgrep -n dd)
kill -USR1 $pid

# Attendre la fin de la commande dd
wait $!

# Supprimer le fichier /tmp/iss généré
rm /tmp/iss
