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

counter=0
while true; do
  spaces=""
  for ((i = n; i > counter; i--)); do
    spaces+=" "
  done

  echo "Ola :${spaces:0:-1} O" &

  # Utilisation de wait pour attendre que tous les processus en arrière-plan se terminent
  wait

  ((counter++))

  if [ $counter -ge $n ]; then
    counter=0
  fi

  sleep 1  # Ajouter une pause pour contrôler la fréquence d'affichage
done
