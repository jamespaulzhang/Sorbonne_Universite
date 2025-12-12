#!/bin/bash

# Vérifier si le nombre d'arguments est correct
if [ $# -ne 1 ]; then
    echo "Usage: $0 <répertoire>"
    exit 1
fi

# Récupérer le nom du répertoire en tant que premier argument
repertoire=$1

# Vérifier si le répertoire existe
if [ ! -d "$repertoire" ]; then
    echo "Erreur : Le répertoire $repertoire n'existe pas."
    exit 1
fi

# Vérifier si le répertoire est lisible
if [ ! -r "$repertoire" ]; then
    echo "Erreur : Impossible de lire le répertoire $repertoire."
    exit 1
fi

# Utiliser find pour obtenir la liste des fichiers dans le répertoire
fichiers=$(find "$repertoire" -type f)

# Utiliser une boucle for pour exécuter le script longest.sh en arrière-plan sur tous les fichiers
for fichier in $fichiers; do
    ./longest.sh "$fichier" &
done

# Attendre que toutes les tâches en arrière-plan se terminent
wait

echo "Toutes les recherches parallèles sont terminées."
