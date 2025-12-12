#! /bin/bash
if [ "$#" -ne 3 ]; then
  echo "Vous devez saisir trois parametres"
  exit 1
fi
if [ -z "$1" ] ||  [ -z "$2" ] || [ -z "$3" ] ; then
  echo "Vous devez saisir un login, un mot de passe et un nom non vide"
  exit 1
fi

if [ -f login.txt ] && [ ! -z "`grep "^$1$" login.txt`" ] ; then
  echo "Choisissez un login different de $1"
  exit 1
fi

echo "$1" >> login.txt
echo "$2" >> pass.txt
echo "$3" >> nom.txt

