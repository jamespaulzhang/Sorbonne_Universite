#!/bin/bash

# Verifier si le repertoire existe, sinon le creer
mkdir -p chunks

# Telecharger les chunks s'ils n'existent pas deja
for i in {0..99}
do
	chunk="data.$(printf %02d $i)"
	if [ ! -f "chunks/$chunk" ]; then
		wget -q http://julien.sopena.fr/chunks/$chunk -P chunks/
		if [ $? -ne 0 ]; then
			echo "Echec lors du telechargement de $chunk, Arret du script."
			break
		fi
	else
		echo "$chunk existe deja, saute."
	fi
done
