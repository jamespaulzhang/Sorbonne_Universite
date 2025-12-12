#!/bin/bash

# Demander confirmation a l'utilisateur
read -p "Etes-vous sur de vouloir tout supprimer ? (y/n) " reponse

# Verifier la reponse de l'utilisateur
[ "$reponse" = "y" ] && echo "You lost everything" || echo "Operation annulee"

