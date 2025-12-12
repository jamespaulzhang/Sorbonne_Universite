#!/bin/bash

function usage() {
    echo "Usage: $0 <fichier_logs>"
    exit 1
}

if [ $# -ne 1 ]; then
    echo "Erreur : veuillez spécifier un fichier de logs."
    usage
fi

if [ ! -r "$1" ]; then
    echo "Erreur : le fichier $1 n'est pas accessible en lecture."
    usage
fi

nb_entrees=$(grep -c "pts" "$1")
echo "Nombre d'entrées : $nb_entrees"

utilisateur=$(whoami)
dernier_utilisateur=$(head -n 1 "$1" | cut -d ' ' -f 1)
if [ "$utilisateur" = "$dernier_utilisateur" ]; then
    echo "Vous êtes le dernier à vous être connecté."
else
    echo "Vous n'êtes pas le dernier à vous être connecté."
fi

nb_connexions=$(grep -c "$utilisateur" "$1")
echo "Nombre de connexions pour $utilisateur : $nb_connexions"

nb_utilisateurs=$(cut -d ' ' -f 1 "$1" | sort | uniq | wc -l)
echo "Nombre d'utilisateurs différents : $nb_utilisateurs"

nb_machines=$(cut -d ' ' -f 3 "$1" | sort -u | grep -cvE '0.0.0.0|localhost')
echo "Nombre de machines distantes : $nb_machines"

utilisateurs_distants=$(cut -d ' ' -f 1,3 "$1" | grep -vE '0.0.0.0|localhost' | sort -u | cut -d ' ' -f 1)
for utilisateur_distant in $utilisateurs_distants; do
    echo "Connexions de $utilisateur_distant :"
    grep "$utilisateur_distant" "$1" | cut -d ' ' -f 3 | sort -u
    echo
done
