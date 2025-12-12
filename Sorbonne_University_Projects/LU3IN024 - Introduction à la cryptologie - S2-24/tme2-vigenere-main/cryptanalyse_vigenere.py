# Sorbonne Université 3I024 2024-2025
# TME 2 : Cryptanalyse du chiffre de Vigenere

# Etudiant 1 : Zhang Yuxiang 21202829
# Etudiant 2 : Lecomte Antoine 21103457

import sys, getopt, math

# Alphabet français
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Fréquence moyenne des lettres en français
freq_FR = [0.092060, 0.010360, 0.030219, 0.037547, 0.171768, 0.010960, 0.010608, 0.010718, 0.075126, 0.003824, 0.000070, 0.061318, 0.026482, 0.070310, 0.049171, 0.023706, 0.010156, 0.066094, 0.078126, 0.073770, 0.063540, 0.016448, 0.000011, 0.004080, 0.002296, 0.001231]


# Chiffrement César
def chiffre_cesar(cipher, key):
    """
    Chiffre un texte en utilisant le chiffrement de César avec une clé donnée.

    Paramètres :
        cipher (str) : Le texte à chiffrer.
        key (int) : La clé de chiffrement (décalage des lettres).

    Retourne :
        str : Le texte chiffré où chaque lettre a été décalée selon la clé.
    """
    encrypted_text = ""
    for char in cipher:
        if char.isalpha():  # Si le caractère est une lettre
            start = ord('A') if char.isupper() else ord('a')
            encrypted_char = chr((ord(char) - start + key) % len(alphabet) + start)  # Décalage avec modulo 26
            encrypted_text += encrypted_char
        else:
            encrypted_text += char  # Garder les caractères non alphabétiques tels quels
    return encrypted_text


# Déchiffrement César
def dechiffre_cesar(cipher, key):
    """
    Déchiffre un texte en utilisant le chiffrement de César avec une clé donnée.

    Paramètres :
        cipher (str) : Le texte à déchiffrer.
        key (int) : La clé de chiffrement (décalage des lettres).

    Retourne :
        str : Le texte déchiffré où chaque lettre a été déplacée selon la clé dans la direction inverse.
    """
    decrypted_text = ""
    for char in cipher:
        if char.isalpha():  # Si le caractère est une lettre
            start = ord('A') if char.isupper() else ord('a')
            decrypted_char = chr((ord(char) - start - key) % len(alphabet) + start)  # Décalage inverse avec modulo 26
            decrypted_text += decrypted_char
        else:
            decrypted_text += char  # Garder les caractères non alphabétiques tels quels
    return decrypted_text


# Chiffrement Vigenere
def chiffre_vigenere(cipher, key):
    """
    Chiffrement de Vigenère.

    Paramètres :
        cipher (str) : Le texte à chiffrer (texte clair).
        key (str ou list) : La clé de chiffrement, soit une chaîne de caractères (chaque lettre représentant un décalage),
                            soit une liste d'entiers (chaque entier représentant un décalage numérique).

    Retourne :
        str : Le texte chiffré, où chaque lettre est décalée selon la clé.
    """
    encrypted_text = ""
    
    # Vérifie si la clé est une chaîne ou une liste d'entiers
    if isinstance(key, str):
        key_shifts = [ord(k.upper()) - ord('A') for k in key]  # Conversion de chaque lettre de la clé en un décalage
    else:
        key_shifts = key  # La clé est déjà une liste d'entiers
    
    key_length = len(key_shifts)  # Longueur de la clé (pour répéter la clé si nécessaire)
    
    for i, char in enumerate(cipher):
        if char.isalpha():  # Si le caractère est une lettre
            start = ord('A') if char.isupper() else ord('a')
            shift = key_shifts[i % key_length]  # Utilisation du décalage correspondant dans la clé
            encrypted_char = chr((ord(char) - start + shift) % len(alphabet) + start)  # Calcul du caractère chiffré
            encrypted_text += encrypted_char
        else:
            encrypted_text += char  # Garder les caractères non alphabétiques tels quels
    
    return encrypted_text


# Déchiffrement Vigenere
def dechiffre_vigenere(cipher, key):
    """
    Déchiffrement de Vigenère.

    Paramètres :
        cipher (str) : Le texte à déchiffrer (texte chiffré).
        key (str ou list) : La clé de chiffrement, soit une chaîne de caractères (chaque lettre représentant un décalage),
                            soit une liste d'entiers (chaque entier représentant un décalage numérique).

    Retourne :
        str : Le texte déchiffré, où chaque lettre est déplacée selon la clé dans la direction inverse.
    """
    decrypted_text = ""
    
    # Vérifie si la clé est une chaîne ou une liste d'entiers
    if isinstance(key, str):
        key_shifts = [ord(k.upper()) - ord('A') for k in key]  # Conversion de chaque lettre de la clé en un décalage
    else:
        key_shifts = key  # La clé est déjà une liste d'entiers
    
    key_length = len(key_shifts)  # Longueur de la clé (pour répéter la clé si nécessaire)
    
    for i, char in enumerate(cipher):
        if char.isalpha():  # Si le caractère est une lettre
            start = ord('A') if char.isupper() else ord('a')
            shift = key_shifts[i % key_length]  # Utilisation du décalage correspondant dans la clé
            decrypted_char = chr((ord(char) - start - shift) % len(alphabet) + start)  # Calcul du caractère déchiffré
            decrypted_text += decrypted_char
        else:
            decrypted_text += char  # Garder les caractères non alphabétiques tels quels
    
    return decrypted_text


# Analyse de fréquences
def freq(cipher):
    """
    Calcule la fréquence d'apparition de chaque lettre de l'alphabet dans un texte donné.
    
    Paramètres :
        cipher (str) : Le texte à analyser
    
    Retourne :
        list : Une liste contenant le nombre d'occurrences de chaque lettre de l'alphabet (en ordre)
    """
    hist = [0] * len(alphabet)
    
    # Filtrer et compter seulement les caractères valides (lettres)
    for char in cipher:
        if char in alphabet:
            hist[alphabet.index(char)] += 1
    
    return hist


# Renvoie l'indice dans l'alphabet
# de la lettre la plus fréquente d'un texte
def lettre_freq_max(cipher):
    """
    Renvoie l'indice dans l'alphabet de la lettre la plus fréquente d'un texte.
    Si plusieurs lettres ont la même fréquence maximale, renvoie la première dans l'ordre alphabétique.
    
    Paramètres :
        cipher (str) : Le texte à analyser
    
    Retourne :
        int : L'indice de la lettre la plus fréquente dans l'alphabet
    """
    hist = freq(cipher)
    max_freq = max(hist)
    return hist.index(max_freq)


# indice de coïncidence
def indice_coincidence(hist):
    """
    Calcule l'indice de coïncidence d'un texte à partir de son histogramme de fréquences.
    
    Paramètres :
        hist (list) : Une liste contenant le nombre d'occurrences de chaque lettre de l'alphabet
    
    Retourne :
        float : L'indice de coïncidence du texte
    """
    n = sum(hist)  # Nombre total de lettres dans le texte
    if n <= 1:
        return 0  # Éviter la division par zéro
    
    ic = sum(ni * (ni - 1) for ni in hist) / (n * (n - 1))
    return ic


# Recherche la longueur de la clé
def longueur_clef(cipher, max_len=20):
    """
    Estime la longueur de la clé en testant plusieurs longueurs de clé,
    et en calculant l'indice de coïncidence moyen pour chaque longueur.
    
    Paramètres :
        cipher (str) : Le texte chiffré
    
    Retourne :
        int : La longueur de la clé estimée
    """
    best_key_length = 0
    best_avg_ic = 0  # La meilleure moyenne d'indice de coïncidence trouvée

    # Tester pour chaque longueur de clé entre 1 et 20
    for key_length in range(1, max_len + 1):  
        colonnes = ["".join(cipher[j] for j in range(i, len(cipher), key_length) if cipher[j] in alphabet)
                    for i in range(key_length)]
        
        # Calcul de la moyenne des indices de coïncidence pour toutes les colonnes
        avg_ic = sum(indice_coincidence(freq(col)) for col in colonnes) / key_length
        
        # Si la moyenne de l'indice de coïncidence dépasse 0.06, on retourne immédiatement la clé
        if avg_ic > 0.06:
            return key_length
    
        # Sinon, on cherche à garder la meilleure longueur de clé
        if avg_ic > best_avg_ic:
            best_avg_ic = avg_ic  # On met à jour la meilleure moyenne
            best_key_length = key_length  # Et on garde cette longueur de clé
    
    # Si aucune longueur de clé n'a dépassé 0.06, on retourne la meilleure trouvée
    return best_key_length

    
# Renvoie le tableau des décalages probables étant
# donné la longueur de la clé
# en utilisant la lettre la plus fréquente
# de chaque colonne
def clef_par_decalages(cipher, key_length):
    """
    Détermine la clé sous forme d'une table de décalages en supposant que la lettre la plus fréquente est 'E'.
    
    Paramètres :
        cipher (str) : Le texte chiffré
        key_length (int) : La longueur de la clé estimée
    
    Retourne :
        list : Une liste d'entiers représentant les décalages de la clé
    """
    reference_letter = 'E'
    ref_index = alphabet.index(reference_letter)
    
    key_shifts = []
    
    for i in range(key_length):
        colonne = "".join(cipher[j] for j in range(i, len(cipher), key_length) if cipher[j] in alphabet)
        
        if colonne:
            most_freq_index = lettre_freq_max(colonne)  # Trouver la lettre la plus fréquente
            shift = (most_freq_index - ref_index) % len(alphabet)  # Calculer le décalage
            key_shifts.append(shift)
    
    return key_shifts


# Cryptanalyse V1 avec décalages par frequence max
def cryptanalyse_v1(cipher):
    """
    Déchiffre un texte chiffré par le chiffrement de Vigenère en estimant la longueur de la clé,
    en calculant les décalages relatifs de chaque colonne et en utilisant ces informations 
    pour déchiffrer le texte chiffré.
    
    Paramètres :
        cipher (str) : Le texte chiffré à analyser
    
    Retourne :
        str : Le texte déchiffré obtenu après cryptanalyse
    """
    # Estimer la longueur de la clé à partir de l'indice de coïncidence
    key_length = longueur_clef(cipher)
    
    # Déterminer la clé sous forme de décalages
    best_key = clef_par_decalages(cipher, key_length)
    
    # Utiliser la fonction dechiffre_vigenere avec la clé obtenue pour déchiffrer le texte
    decrypted_text = dechiffre_vigenere(cipher, best_key)
    
    return decrypted_text


################################################################


### Les fonctions suivantes sont utiles uniquement
### pour la cryptanalyse V2.

# Indice de coincidence mutuelle avec décalage
def indice_coincidence_mutuelle(freq1, freq2, d):
    """
    Calcule l'indice de coïncidence mutuelle entre deux distributions de fréquences de lettres,
    avec un décalage appliqué au second texte.

    Paramètres :
        freq1 : Liste représentant la fréquence d'apparition de chaque lettre dans le premier texte.
        freq2 : Liste représentant la fréquence d'apparition de chaque lettre dans le second texte.
        d : Entier représentant le décalage à appliquer aux positions des lettres dans le second texte avant de les comparer aux fréquences du premier texte.
        
    Retourne :
        float : L'indice de coïncidence mutuelle entre les deux textes après avoir appliqué le décalage.
    """
    n1 = sum(freq1)
    n2 = sum(freq2)

    # Calcul de l'ICM avec décalage
    icm = sum(freq1[i] * freq2[(i + d) % len(alphabet)] for i in range(len(alphabet))) / (n1 * n2)

    return icm


# Renvoie le tableau des décalages probables étant
# donné la longueur de la clé
# en comparant l'indice de décalage mutuel par rapport
# à la première colonne
def tableau_decalages_ICM(cipher, key_length):
    """
    Détermine les décalages relatifs des colonnes par rapport à la première colonne
    en maximisant l'indice de coïncidence mutuelle.

    Paramètres :
        cipher (str) : Le texte chiffré
        key_length (int) : La longueur de la clé estimée

    Retourne :
        list : Une liste d'entiers représentant les décalages de la clé
    """
    # Découper le texte en colonnes
    colonnes = ["".join(cipher[j] for j in range(i, len(cipher), key_length)) for i in range(key_length)]

    # Calcul des fréquences pour chaque colonne
    colonnes_freq = [freq(colonne) for colonne in colonnes]

    # Initialisation du tableau des décalages
    decalages = [0] * key_length

    # Calcul des décalages relatifs
    for i in range(1, key_length):
        max_icm = -1
        meilleur_decalage = 0
        for d in range(len(alphabet)):  # Parcourir tous les décalages possibles pour un alphabet de 26 lettres
            icm = indice_coincidence_mutuelle(colonnes_freq[0], colonnes_freq[i], d)
            if icm > max_icm:
                max_icm = icm
                meilleur_decalage = d
        decalages[i] = meilleur_decalage

    return decalages


# Cryptanalyse V2 avec décalages par ICM
def cryptanalyse_v2(cipher):
    """
    Déchiffre un texte chiffré du chiffrement de Vigenère en utilisant l'indice de coïncidence pour déterminer la longueur de la clé,
    puis en calculant les décalages relatifs grâce à l'ICM de chaque colonne. Une fois les colonnes alignées, on applique le déchiffrement 
    de César sur le texte reconstruit.
    
    Paramètre :
        cipher (str) : Le texte chiffré
    
    Retourne :
        str : Le texte déchiffré
    """
    
    # Estimer la longueur de la clé à partir de l'indice de coïncidence
    key_length = longueur_clef(cipher)
    
    # Trouver les décalages relatifs par rapport à la première colonne
    decalages = tableau_decalages_ICM(cipher, key_length)
    
    # Découper le texte en colonnes
    colonnes = ["".join(cipher[j] for j in range(i, len(cipher), key_length)) for i in range(key_length)]
    
    # Appliquer les décalages pour aligner les colonnes
    colonnes_alignees = [
        dechiffre_cesar(colonne, decalages[i]) for i, colonne in enumerate(colonnes)
    ]

    # Reconstruire le texte chiffré aligné
    # i % key_length détermine de quelle colonne provient la lettre
    # i // key_length détermine l'index dans la colonne concernée
    texte_aligne = [""] * len(cipher)
    for i in range(len(cipher)):
        texte_aligne[i] = colonnes_alignees[i % key_length][i // key_length] 
    texte_aligne = "".join(texte_aligne)

    # Déterminer le décalage optimal avec la lettre la plus fréquente
    lettre_plus_frequente = lettre_freq_max(texte_aligne)
    decalage_cesar = (lettre_plus_frequente - alphabet.index("E")) % len(alphabet)

    # Déchiffrer le texte chiffré aligné avec César
    decrypted_text = dechiffre_cesar(texte_aligne, decalage_cesar)

    return decrypted_text


################################################################


### Les fonctions suivantes sont utiles uniquement
### pour la cryptanalyse V3.

# Prend deux listes de même taille et
# calcule la correlation lineaire de Pearson
def correlation(L1, L2):
    """
    Calcule la corrélation de Pearson entre deux listes de même taille.

    Paramètres :
        L1 (list) : Première liste
        L2 (list) : Seconde liste
    
    Retourne :
        float : Coefficient de corrélation de Pearson
    """
    if len(L1) != len(L2) or len(L1) == 0:
        return 0.0

    mean1, mean2 = sum(L1) / len(L1), sum(L2) / len(L2)
    
    num = sum((L1[i] - mean1) * (L2[i] - mean2) for i in range(len(L1)))
    denom = math.sqrt(sum((L1[i] - mean1) ** 2 for i in range(len(L1))) * sum((L2[i] - mean2) ** 2 for i in range(len(L2))))
    
    return num / denom if denom != 0 else 0.0


# Renvoie la meilleur clé possible par correlation
# étant donné une longueur de clé fixée
def clef_correlations(cipher, key_length):
    """
    Trouve la clé qui maximise la corrélation avec un texte français pour une longueur de clé donnée.
    
    Paramètres :
        cipher (str) : Le texte chiffré
        key_length (int) : La longueur de la clé estimée
    
    Retourne :
        tuple : (moyenne des corrélations, liste des décalages)
    """
    colonnes = ["".join(cipher[j] for j in range(i, len(cipher), key_length) if cipher[j] in alphabet) for i in range(key_length)]
    
    # Calcul des fréquences pour chaque colonne
    colonnes_freq = [freq(colonne) for colonne in colonnes]
    
    best_shifts = []
    best_corrs = []
    
    for freqs in colonnes_freq:
        best_d, best_corr = 0, -1
        for d in range(len(alphabet)):
            shifted_hist = freqs[d:] + freqs[:d]  # Décalage circulaire
            corr = correlation(shifted_hist, freq_FR) # Fréquences des lettres de Germinal (texte Français) pour freq_FR
            if corr > best_corr:
                best_corr, best_d = corr, d
        
        best_corrs.append(best_corr)
        best_shifts.append(best_d)
    
    # Moyenne des corrélations sur toutes les colonnes
    avg_corr = sum(best_corrs) / key_length
    return avg_corr, best_shifts


# Cryptanalyse V3 avec correlations
def cryptanalyse_v3(cipher):
    """
    Déchiffre un texte chiffré par le chiffrement de Vigenère en utilisant l'analyse de la corrélation de Pearson.
    Teste différentes tailles de clé et choisit celle qui maximise la moyenne des corrélations.
    
    Paramètre :
        cipher (str) : Le texte chiffré
    
    Retourne :
        str : Le texte déchiffré
    """
    best_avg_corr = -1  # Initialiser la meilleure moyenne de corrélation
    best_shifts = []  # Initialiser les meilleurs décalages
    
    # Tester pour chaque taille de clé de 1 à 20
    for key_length in range(1, 21):
        avg_corr, shifts = clef_correlations(cipher, key_length)
        
        # Si la moyenne des corrélations est meilleure, on met à jour les variables
        if avg_corr > best_avg_corr:
            best_avg_corr = avg_corr
            best_shifts = shifts
    
    # Déchiffrer le texte avec la clé obtenue
    best_key = "".join(alphabet[shift] for shift in best_shifts)
    decrypted_text = dechiffre_vigenere(cipher, best_key)
    
    return decrypted_text


################################################################
# NE PAS MODIFIER LES FONCTIONS SUIVANTES
# ELLES SONT UTILES POUR LES TEST D'EVALUATION
################################################################


# Lit un fichier et renvoie la chaine de caracteres
def read(fichier):
    f=open(fichier,"r")
    txt=(f.readlines())[0].rstrip('\n')
    f.close()
    return txt

# Execute la fonction cryptanalyse_vN où N est la version
def cryptanalyse(fichier, version):
    cipher = read(fichier)
    if version == 1:
        return cryptanalyse_v1(cipher)
    elif version == 2:
        return cryptanalyse_v2(cipher)
    elif version == 3:
        return cryptanalyse_v3(cipher)

def usage():
    print ("Usage: python3 cryptanalyse_vigenere.py -v <1,2,3> -f <FichierACryptanalyser>", file=sys.stderr)
    sys.exit(1)

def main(argv):
    size = -1
    version = 0
    fichier = ''
    try:
        opts, args = getopt.getopt(argv,"hv:f:")
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-v"):
            version = int(arg)
        elif opt in ("-f"):
            fichier = arg
    if fichier=='':
        usage()
    if not(version==1 or version==2 or version==3):
        usage()

    print("Cryptanalyse version "+str(version)+" du fichier "+fichier+" :")
    print(cryptanalyse(fichier, version))
    
if __name__ == "__main__":
   main(sys.argv[1:])
