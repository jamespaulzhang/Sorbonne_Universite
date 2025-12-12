#! /bin/bash
# ecriture.sh
if [ $# -lt 1 ] ; then
  echo Il faut au moins un parametre
  exit 1
fi
for elem in "$@" ; do
  iss_synchro lock verrou
  if [ ! -e "$elem" ] ; then
    echo premier $$ > "$elem"
  else
    echo suivant $$ >> "$elem"
  fi
  iss_synchro unlock verrou
done
