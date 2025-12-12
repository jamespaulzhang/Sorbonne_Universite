#!/bin/bash

# Verifier si le nombre de parametres est correct

if test $# -lt 1; then
	echo "Parametre manquant"
	echo "usage : $0 <repertoire>"
	exit 22
fi

# Verifier si le repertoire existe

if test ! -d $1; then
	echo "Le repertoire $1 n'existe pas."
	echo "usage : $0 <repertoire>"
	exit 1
fi

size=0
for f in $1/*; do
	cur=$(wc -c < $f)
	if test $cur -gt $size; then
		size=$cur
		biggest=$f
	fi
done

echo $biggest
