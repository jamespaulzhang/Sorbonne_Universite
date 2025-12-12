#! bin/bash

egrep "^.{15}$" dico.txt > /tmp/dico15.txt
for m in $(egrep "^.{8}$" dico.txt); do
    egrep "$m" /tmp/dico15.txt
done