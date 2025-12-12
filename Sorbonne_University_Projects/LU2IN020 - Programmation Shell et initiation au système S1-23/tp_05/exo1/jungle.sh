#!/bin/bash

# Demander à l'utilisateur de choisir entre VF et VO
read -p "Choisissez entre VF et VO : " choix

# Parcourir le fichier CSV et exécuter cowsay avec les paramètres appropriés
while IFS=',' read -r animal cri_VF cri_VO; do
    if [ "$choix" = "VF" ]; then
        cowsay -f "$animal" "$cri_VF"
    elif [ "$choix" = "VO" ]; then
        cowsay -f "$animal" "$cri_VO"
    else
        echo "Choix invalide. Veuillez entrer VF ou VO."
        exit 1
    fi
done < blabla.csv