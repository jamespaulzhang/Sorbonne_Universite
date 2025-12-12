#!/bin/bash

#Verifier le nombre de parametres
if [ $# -ne 2 ]; then
	echo "Usage: $0 <source> <destination>"
	exit 1
fi

# Verifier si le repertoire source existe
if [ ! -d "$1" ]; then
	echo "Le repertoire source $1 n'existe pas."
	exit 1
fi

# Verifier si le repertoire destination existe
if [ ! -d "$2" ]; then
	echo "Le repertoire destination $2 n'exitse pas."
	exit 1
fi

# Creer un repertoire selection s'il n'existe pas
mkdir -p selection

# Utiliser biggest.sh pour trouver les 4 plus gros fichers
./biggest.sh "$1" > selection/
head -n 4 selection/ | xargs -I {} cp "$1"/{} "$2"


