#!/bin/bash

# Vérifier si le nombre d'arguments est correct
if [ $# -ne 1 ]; then
    echo "Usage: $0 <fichier>"
    exit 1
fi

# Récupérer le nom du fichier en tant que premier argument
fichier=$1

# Vérifier si le fichier existe
if [ ! -e "$fichier" ]; then
    echo "Erreur : Le fichier $fichier n'existe pas."
    exit 1
fi

# Vérifier si le fichier est lisible
if [ ! -r "$fichier" ]; then
    echo "Erreur : Impossible de lire le fichier $fichier."
    exit 1
fi

# Trouver le mot le plus long
mot_long=$(awk '{ print length, $0 }' "$fichier" | sort -nr | head -n 1 | cut -d" " -f2-)

# Créer un nouveau fichier avec le mot le plus long
nouveau_fichier="${fichier}.tmp"
echo "$mot_long" > "$nouveau_fichier"

# Afficher un message de succès
echo "Le mot le plus long dans $fichier est '$mot_long' et a été écrit dans $nouveau_fichier."
