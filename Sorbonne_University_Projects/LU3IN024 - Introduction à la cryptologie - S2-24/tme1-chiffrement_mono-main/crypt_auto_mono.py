#!/usr/bin/python3

# Usage python3 crypt_auto_mono.py file
# Where file contains the ciphertext
# It is recommended to write a few functions for this exercise

ciphertext = ""
ciphertext_eval = 0
encryption_key = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
plaintext = ""
plaintext_eval = 0
decryption_key = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
iter = 0

# Do not modify these lines except for variable names
print ("texte chiffré\n" + ciphertext)
print ("évaluation " + str(ciphertext_eval))
print ("\nAprès " + str(iter) + " itérations, texte déchiffré\n" + plaintext)
print ("substitution appliquée au texte fourni " + encryption_key)
print ("clef " + decryption_key)
print ("évaluation " + str(plaintext_eval))
