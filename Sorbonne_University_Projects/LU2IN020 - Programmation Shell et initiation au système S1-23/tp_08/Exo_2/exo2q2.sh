#!/bin/bash
for letter in {A..Z}; do
    touch "/home/laviestbelle/Desktop/ISS/tp_07/Exo_2/dico/$letter.txt"
done

process_letter(){
    letter=$1
    grep -E "^$letter" dico.txt > "/home/laviestbelle/Desktop/ISS/tp_07/Exo_2/dico/$letter.txt"
}

for letter in {A..Z}; do
    process_letter "$letter" &
done

wait
