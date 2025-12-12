#!/usr/bin/python3

# Usage: python3 frequence.py fichier_texte

import sys

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
Occurrences = {letter: 0 for letter in alphabet}
length = 0

if len(sys.argv) != 2:
    print("Usage: python3 frequence.py <fichier_texte>")
    sys.exit(1)

file_path = sys.argv[1]

try:
    with open(file_path, 'r') as file:
        text = file.read().upper()
        for char in text:
            if char.isalpha():
                Occurrences[char] += 1
                length += 1
except FileNotFoundError:
    print(f"File {file_path} not found.")
    sys.exit(1)

for c in alphabet:
    if length > 0:
        frequency = Occurrences[c] / length
    else:
        frequency = 0.0
    print(f"{c} {frequency:.6f}")
