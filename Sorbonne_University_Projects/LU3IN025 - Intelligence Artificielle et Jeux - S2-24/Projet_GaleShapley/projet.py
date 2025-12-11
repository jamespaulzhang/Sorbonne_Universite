from collections import deque
import heapq
import random
import time
import matplotlib.pyplot as plt
import numpy as np
import subprocess
from gurobipy import *
import pulp

def lire_pref_etudiants(fichier):
    with open(fichier, "r") as f:
        lignes = f.readlines()
    
    CE = []
    
    for ligne in lignes[1:]:  # On saute la première ligne (nombre d'étudiants)
        _, _, *preferences = ligne.strip().split()  # On ignore l'ID et le nom
        CE.append(list(map(int, preferences)))  # Conversion en liste d'entiers
    
    return CE


def lire_pref_parcours(fichier):
    with open(fichier, "r") as f:
        lignes = f.readlines()

    capacites = list(map(int, lignes[1].strip().split()[1:]))  # On ignore "Cap"

    CP = []

    for ligne in lignes[2:]:  # On saute les deux premières lignes (NbEtu et Cap)
        _, _, *preferences = ligne.strip().split()  # On ignore l'ID et le nom du parcours
        CP.append(list(map(int, preferences)))  # Conversion en liste d'entiers

    return CP, capacites


def gale_shapley_etudiants(CE, CP, capacites):
    n = len(CE)  # Nombre d'étudiants
    m = len(CP)  # Nombre de parcours

    # 1. Trouver un étudiant libre : deque permet un accès rapide en O(n)
    etudiants_libres = deque(range(n))  # File des étudiants libres

    # 2. Prochain parcours à proposer : tableau pour accès direct en O(n)
    prochain_parcours = [0] * n  # Indice du prochain parcours que chaque étudiant va proposer

    # 3. Classement des étudiants pour chaque parcours : dictionnaire pour accès rapide en O(n*m)
    classement_parcours = [{etudiant: rang for rang, etudiant in enumerate(CP[j])} for j in range(m)]

    # 4. Affectations des parcours : heapq pour trouver l'étudiant le moins préféré en O(m*log k) car O(log k) par insertion/suppression
    affectations = {j: [] for j in range(m)}

    # 5. Capacités restantes pour chaque parcours : tableau pour accès direct en O(m)
    capacite_restante = capacites[:]

    while etudiants_libres:
        i = etudiants_libres.popleft()  # O(1)

        while prochain_parcours[i] < m:
            j = CE[i][prochain_parcours[i]]  # O(1)
            prochain_parcours[i] += 1

            if capacite_restante[j] > 0:
                heapq.heappush(affectations[j], (-classement_parcours[j][i], i))  # O(log k)
                capacite_restante[j] -= 1  # O(1)
                break
            else:
                moins_prefere_rang, moins_prefere = affectations[j][0]  # O(1)

                if classement_parcours[j][i] < -moins_prefere_rang:
                    heapq.heappop(affectations[j])  # O(k)
                    etudiants_libres.append(moins_prefere)  # O(1)
                    heapq.heappush(affectations[j], (-classement_parcours[j][i], i))  # O(k)
                    break

    result = {j: [etudiant for _, etudiant in sorted(affectations[j])] for j in range(m)}
    return result


def gale_shapley_parcours(CE, CP, capacites):
    n = len(CE)  # Nombre d'étudiants
    m = len(CP)  # Nombre de parcours

    # 1. Parcours libres : deque pour accès rapide en O(m)
    parcours_libres = deque(range(m))

    # 2. Capacités restantes : tableau pour accès direct en O(m)
    capacite_restante = capacites[:]

    # 3. Affectation actuelle des étudiants : tableau pour accès rapide en O(n)
    etudiant_affecte = [-1] * n

    # 4. Classement des parcours pour chaque étudiant : dictionnaire pour accès rapide en O(n*m)
    classement_etudiants = [{parcours: rang for rang, parcours in enumerate(CE[i])} for i in range(n)]

    # 5. Affectations des parcours : liste pour gestion des étudiants en O(m)
    affectations = {j: [] for j in range(m)}

    while parcours_libres:
        parcours = parcours_libres.popleft()  # O(1)

        while capacite_restante[parcours] > 0 and CP[parcours]:
            etudiant = CP[parcours].pop(0)  # O(1)

            if etudiant_affecte[etudiant] == -1: 
                etudiant_affecte[etudiant] = parcours
                affectations[parcours].append(etudiant)  # O(1)
                capacite_restante[parcours] -= 1
            else:
                ancien_parcours = etudiant_affecte[etudiant]

                if classement_etudiants[etudiant][parcours] < classement_etudiants[etudiant][ancien_parcours]:
                    affectations[ancien_parcours].remove(etudiant)  # O(k)
                    capacite_restante[ancien_parcours] += 1
                    affectations[parcours].append(etudiant)  # O(1)
                    capacite_restante[parcours] -= 1
                    etudiant_affecte[etudiant] = parcours

                    if capacite_restante[ancien_parcours] > 0:
                        parcours_libres.append(ancien_parcours)  # O(1)

        if capacite_restante[parcours] > 0:
            parcours_libres.append(parcours)  # O(1)

    return affectations


# Q6
def trouver_paires_instables(CE, CP, affectation):
    """
    Trouve les paires instables dans l'affectation donnée.
    
    Une paire est instable si l'étudiant et le parcours préfèrent être ensemble
    plutôt qu'avec leur affectation actuelle.
    
    :param CE: Matrice des préférences des étudiants
    :param CP: Matrice des préférences des parcours
    :param affectation: Dictionnaire d'affectation des étudiants aux parcours
    :return: Liste des paires instables sous forme de tuples (étudiant, parcours)
    """
    paires_instables = []

    # Parcours chaque parcours pour examiner les étudiants affectés
    for parcours, etudiants in affectation.items():
        # Les étudiants actuellement affectés à ce parcours
        for etudiant in etudiants:
            # Vérifier si cette affectation est stable
            # 1. L'étudiant préfère un autre parcours à celui auquel il est affecté
            for autre_parcours in CE[etudiant]:
                if autre_parcours != parcours:
                    # Vérifier que l'autre parcours préfère cet étudiant à certains de ses étudiants actuels
                    for etudiant_autre_parcours in affectation.get(autre_parcours, []):
                        if etudiant in CP[autre_parcours] and etudiant_autre_parcours in CP[autre_parcours]:
                            if (CE[etudiant].index(autre_parcours) < CE[etudiant].index(parcours)) and \
                            (CP[autre_parcours].index(etudiant) < CP[autre_parcours].index(etudiant_autre_parcours)):
                                paires_instables.append((etudiant, autre_parcours))  # Ajouter la paire instable


    return paires_instables


def afficher_paires_instables(paires_instables):
    """
    Affiche les paires instables, ou un message si aucune paire instable n'est trouvée.
    
    :param paires_instables: Liste des paires instables sous forme de tuples (étudiant, parcours)
    """
    if paires_instables:
        print("Paires instables trouvées :")
        for etudiant, parcours in paires_instables:
            print(f"Étudiant {etudiant} préfère le parcours {parcours}.")
    else:
        print("Aucune paire instable trouvée. L'affectation est stable.")


# Partie 2: Evolution du temps de calcul
# Q7
def generer_pref_etudiants(n):
    """
    Génère une matrice de préférences des étudiants pour 9 parcours.
    Chaque étudiant a un ordre de préférence aléatoire pour les 9 parcours.
    
    :param n: Nombre d'étudiants
    :return: Matrice CE (liste de listes)
    """
    nb_parcours = 9
    CE = [random.sample(range(nb_parcours), nb_parcours) for _ in range(n)]
    return CE


def generer_pref_parcours(n):
    """
    Génère une matrice de préférences des 9 parcours pour les étudiants.
    Chaque parcours a un ordre de préférence aléatoire pour les n étudiants.
    
    :param n: Nombre d'étudiants
    :return: Matrice CP (liste de listes)
    """
    nb_parcours = 9
    CP = [random.sample(range(n), n) for _ in range(nb_parcours)]
    return CP


# Fonctions pour affichage
def afficher_matrice(titre, matrice, prefixe_ligne=""):
    print(titre)
    for i, ligne in enumerate(matrice):
        print(f"{prefixe_ligne}{i}: {ligne}")
    print("\n")


def afficher_affectations_etudiants(titre, affectations):
    """ Affiche les affectations sous un format clair. """
    print(f"\n{titre}:")
    for parcours, etudiants in affectations.items():
        print(f"  Etudiants {', '.join(map(str, etudiants))}: {parcours}")


def afficher_affectations_parcours(titre, affectations):
    """ Affiche les affectations sous un format clair. """
    print(f"\n{titre}:")
    for parcours, etudiants in affectations.items():
        print(f"  Parcours {parcours}: {', '.join(map(str, etudiants))}")


def generer_capacites(n, nb_parcours=9):
    """
    Génère une liste de capacités équilibrées pour les parcours.
    La somme des capacités est égale à n.
    Le reste est réparti aléatoirement entre les parcours.
    """
    base_capacite = n // nb_parcours
    capacites = [base_capacite] * nb_parcours
    reste = n % nb_parcours

    # Sélectionner aléatoirement des indices pour distribuer le reste
    indices_aleatoires = random.sample(range(nb_parcours), reste)
    for i in indices_aleatoires:
        capacites[i] += 1

    return capacites


# Mesure du temps d'exécution des deux algorithmes
def mesurer_temps_gale_shapley(n, nb_tests):
    """
    Mesure le temps moyen d'exécution des algorithmes de Gale-Shapley côté étudiants et parcours pour une valeur donnée de n.
    """
    temps_etudiants = []
    temps_parcours = []

    for _ in range(nb_tests):
        CE = generer_pref_etudiants(n)
        CP = generer_pref_parcours(n)
        capacites = generer_capacites(n)

        # Mesurer le temps pour l'algorithme côté étudiants
        debut_etudiants = time.time()
        gale_shapley_etudiants(CE, CP, capacites)
        fin_etudiants = time.time()
        temps_etudiants.append(fin_etudiants - debut_etudiants)

        # Mesurer le temps pour l'algorithme côté parcours
        debut_parcours = time.time()
        gale_shapley_parcours(CE, CP, capacites)
        fin_parcours = time.time()
        temps_parcours.append(fin_parcours - debut_parcours)

    return np.mean(temps_etudiants), np.mean(temps_parcours)


# Q8
def tracer_courbes(nb_tests=100):
    """Générer les temps d'exécution pour différentes valeurs de n"""
    valeurs_n = range(200, 2001, 200)
    temps_moyens_etudiants = []
    temps_moyens_parcours = []

    for n in valeurs_n:
        temps_etudiants, temps_parcours = mesurer_temps_gale_shapley(n, nb_tests)
        temps_moyens_etudiants.append(temps_etudiants)
        temps_moyens_parcours.append(temps_parcours)

    # Tracer la courbe
    plt.figure(figsize=(10, 6))
    plt.plot(valeurs_n, temps_moyens_etudiants, label='Gale-Shapley (Étudiants)', color='b', marker='o')
    plt.plot(valeurs_n, temps_moyens_parcours, label='Gale-Shapley (Parcours)', color='g', marker='o')
    plt.xlabel('Nombre d\'étudiants (n)')
    plt.ylabel('Temps moyen d\'exécution (secondes)')
    plt.title(f'Temps d\'exécution des algorithmes de Gale-Shapley (Tests : {nb_tests})')
    plt.legend()
    plt.grid(True)
    plt.show()


# Partie 3
# Q11
def generate_lp_file_k(n, preferences, capacities, k, filename="problem.lp"):
    """
    Génère un fichier .lp pour s'assurer qu'un étudiant obtient un de ses k premiers choix.
    
    :param n: Nombre d'étudiants
    :param preferences: Dictionnaire des préférences des étudiants (clé: étudiant, valeur: liste de parcours classés)
    :param capacities: Liste des capacités des parcours
    :param k: Nombre maximum de choix considérés pour chaque étudiant
    :param filename: Nom du fichier LP généré
    """
    with open(filename, "w") as f:
        f.write("\\* PLNE - Affectation avec contrainte sur k premiers choix *\\\n")
        f.write("Minimize\n")
        f.write(" obj: 0\n")  # Pas d'objectif, on cherche la faisabilité
        f.write("Subject To\n")
        
        # Contraintes d'affectation unique pour chaque étudiant
        for i in range(n):
            f.write(f" c_assign_{i}: " + " + ".join([f"x_{i}_{j}" for j in preferences[i][:k]]) + " = 1\n")
        
        # Contraintes de capacité des parcours
        num_parcours = len(capacities)
        for j in range(num_parcours):
            f.write(f" c_capacity_{j}: " + " + ".join([f"x_{i}_{j}" for i in range(n) if j in preferences[i][:k]]) + f" <= {capacities[j]}\n")
        
        # Déclaration des variables binaires
        f.write("Binary\n")
        for i in range(n):
            for j in preferences[i][:k]:
                f.write(f" x_{i}_{j}\n")
        
        f.write("End\n")


# Q13
def score_borda_combined(student_preferences, course_preferences):
    """
    Calculer la matrice de scores Borda combinée, en fusionnant les préférences des étudiants et des cours.

    :param student_preferences: Préférences des étudiants (n lignes, m colonnes)
    :param course_preferences: Préférences des cours (m lignes, n colonnes)
    :return: Matrice des scores Borda combinés (n lignes, m colonnes)
    """
    num_students = len(student_preferences)  # Nombre d'étudiants (n)
    num_courses = len(student_preferences[0])  # Nombre de cours (m)

    # Calculer les scores Borda des étudiants (n * m)
    student_borda_scores = [[num_courses - rank - 1 for rank in student] for student in student_preferences]

    # Calculer les scores Borda des cours (m * n) puis les transposer en (n * m)
    course_borda_scores = [[num_students - rank - 1 for rank in course] for course in course_preferences]
    course_borda_scores_T = list(map(list, zip(*course_borda_scores)))  # Transposition (m*n → n*m)

    # Calculer les scores Borda combinés (n * m)
    combined_borda_scores = [[student_borda_scores[i][j] + course_borda_scores_T[i][j] for j in range(num_courses)]
                              for i in range(num_students)]

    return combined_borda_scores


def find_min_k(n, preferences_students, capacities):
    """
    Trouver la valeur minimale de k telle que chaque étudiant puisse obtenir au moins un cours parmi ses k premiers choix.

    :param n: Le nombre d'étudiants
    :param preferences_students: Liste des préférences des étudiants (classement des cours de chaque étudiant)
    :param capacities: Capacités des cours
    :return: La valeur minimale de k
    """
    k = 1
    while True:
        try:
            # Générer un fichier LP pour vérifier si la valeur actuelle de k est réalisable
            lp_filename = f"temp_k_{k}.lp"
            generate_lp_file_k(n, preferences_students, capacities, k, lp_filename)

            # Utiliser gurobi_cl pour résoudre ce fichier LP
            # gurobi_cl est l'outil en ligne de commande de Gurobi
            result = subprocess.run(['gurobi_cl', lp_filename], capture_output=True, text=True)

            # Si la solution est trouvée, retourner k
            if 'Optimal solution found' in result.stdout:
                print(f"Solution trouvée pour k = {k}")
                return k
            else:
                print(f"Aucune solution trouvée pour k = {k}, tentative avec k = {k + 1}")
                k += 1
        except Exception as e:
            print(f"Erreur lors de la tentative de résolution du LP pour k = {k}: {e}")
            # Si le LP n'est pas solvable, augmenter k et réessayer
            k += 1


def maximize_min_utility(n, m, preferences_students, preferences_parcours, capacities, k):
    """
    Maximiser l'utilité minimale des étudiants pour un k donné.
    
    :param n: Nombre d'étudiants
    :param m: Nombre de cours
    :param preferences_students: Préférences des étudiants (liste de listes)
    :param preferences_parcours: Préférences des cours (liste de listes)
    :param capacities: Capacités des cours (liste)
    :param k: Nombre de premiers choix considérés pour chaque étudiant
    :return: Affectation optimale et utilité minimale atteinte
    """
    # Calculer la matrice des scores Borda combinés
    combined_borda_scores = score_borda_combined(preferences_students, preferences_parcours)

    # Définir le problème
    problem = pulp.LpProblem("Maximize_Min_Utility", pulp.LpMaximize)

    # Variables de décision binaires pour les affectations
    x = pulp.LpVariable.dicts("x", ((i, j) for i in range(n) for j in preferences_students[i][:k]), cat='Binary')

    # Variable pour l'utilité minimale
    U_min = pulp.LpVariable("U_min", lowBound=0, cat='Continuous')

    # Fonction objectif : maximiser l'utilité minimale
    problem += U_min

    # Contrainte : chaque étudiant doit être affecté à un seul cours parmi ses k premiers choix
    for i in range(n):
        problem += pulp.lpSum(x[(i, j)] for j in preferences_students[i][:k]) == 1, f"Assign_Student_{i}"

    # Contrainte : respect des capacités des cours
    for j in range(m):
        course_vars = [x[(i, j)] for i in range(n) if j in preferences_students[i][:k]]
        if course_vars:
            problem += pulp.lpSum(course_vars) <= capacities[j], f"Capacity_Course_{j}"

    # Contrainte : l'utilité de chaque étudiant doit être >= U_min
    for i in range(n):
        utility_expr = pulp.lpSum(combined_borda_scores[i][j] * x[(i, j)] for j in preferences_students[i][:k])
        problem += utility_expr >= U_min, f"Min_Utility_Student_{i}"

    # Résolution du problème
    solver = pulp.PULP_CBC_CMD(msg=False)
    result = problem.solve(solver)

    # Vérification de la solution
    if pulp.LpStatus[problem.status] == "Optimal":
        allocation = {(i, j): pulp.value(x[(i, j)]) for i in range(n) for j in preferences_students[i][:k] if pulp.value(x[(i, j)]) == 1}
        return allocation, pulp.value(U_min)
    else:
        print("Aucune solution optimale trouvée.")
        return None, None

# Q14
def generate_lp_file_maximum(n, m, preferences_students, preferences_parcours, capacities, k, filename="problem.lp"):
    """
    Générer un fichier LP pour maximiser l'utilité totale des étudiants et des cours, tout en s'assurant que chaque étudiant 
    obtienne au moins un cours parmi ses k premiers choix.

    :param n: Le nombre d'étudiants
    :param m: Le nombre de cours
    :param preferences_students: Préférences des étudiants (liste, classement des cours pour chaque étudiant)
    :param preferences_parcours: Préférences des cours (liste, classement des étudiants pour chaque cours)
    :param capacities: Capacités des cours (liste)
    :param k: Nombre maximum de choix de cours pour chaque étudiant
    :param filename: Nom du fichier LP
    """
    # Calculer la matrice des scores Borda combinés
    combined_borda_scores = score_borda_combined(preferences_students, preferences_parcours)

    with open(filename, "w") as f:
        f.write("\\* PLNE - Maximisation de la somme des utilités *\\\n")
        f.write("Maximize\n")

        # Fonction objectif : maximiser la somme des scores
        obj_terms = []
        for i in range(n):
            for j in preferences_students[i][:k]:
                score = combined_borda_scores[i][j]  # Correction de l'index
                obj_terms.append(f"{score} x_{i}_{j}")

        f.write(" obj: " + " + ".join(obj_terms) + "\n")

        f.write("Subject To\n")

        # Contrainte 1 : chaque étudiant ne peut être affecté qu'à un seul cours
        for i in range(n):
            student_vars = [f"x_{i}_{j}" for j in preferences_students[i][:k]]
            f.write(f" c_assign_{i}: " + " + ".join(student_vars) + " = 1\n")

        # Contrainte 2 : capacité de chaque cours
        for j in range(m):
            course_vars = [f"x_{i}_{j}" for i in range(n) if j in preferences_students[i][:k]]
            if course_vars:
                f.write(f" c_capacity_{j}: " + " + ".join(course_vars) + f" <= {capacities[j]}\n")

        # Contrainte 3 : contrainte sur l'utilité minimale de chaque étudiant
        for i in range(n):
            min_utility = m - k  # Utilité minimale
            utility_terms = [f"{combined_borda_scores[i][j]} x_{i}_{j}" for j in preferences_students[i][:k]]
            f.write(f" c_min_utility_{i}: " + " + ".join(utility_terms) + f" >= {min_utility}\n")

        # Déclaration des variables : toutes les variables sont binaires
        f.write("Binary\n")
        for i in range(n):
            for j in preferences_students[i][:k]:
                f.write(f" x_{i}_{j}\n")

        f.write("End\n")


# Q15
def maximize_utility_and_fairness(n, m, preferences_students, preferences_parcours, capacities, k):
    """
    Maximiser la somme des utilités (efficacité totale) tout en garantissant une utilité minimale pour les étudiants.

    :param n: Nombre d'étudiants
    :param m: Nombre de cours
    :param preferences_students: Préférences des étudiants (liste de listes)
    :param preferences_parcours: Préférences des cours (liste de listes)
    :param capacities: Capacités des cours (liste)
    :param k: Nombre de premiers choix considérés pour chaque étudiant
    :return: Affectation optimale, utilité minimale atteinte et utilité moyenne
    """

    # Calculer la matrice des scores Borda combinés
    combined_borda_scores = score_borda_combined(preferences_students, preferences_parcours)

    # Définir le problème
    problem = pulp.LpProblem("Maximize_Utility_and_Fairness", pulp.LpMaximize)

    # Variables de décision binaires pour les affectations
    x = pulp.LpVariable.dicts("x", ((i, j) for i in range(n) for j in preferences_students[i][:k]), cat='Binary')

    # Variable pour l'utilité minimale
    U_min = pulp.LpVariable("U_min", lowBound=0, cat='Continuous')

    # Fonction objectif : maximiser la somme des utilités
    total_utility = pulp.lpSum(combined_borda_scores[i][j] * x[(i, j)] for i in range(n) for j in preferences_students[i][:k])
    problem += total_utility + U_min

    # Contrainte : chaque étudiant doit être affecté à un seul cours parmi ses k premiers choix
    for i in range(n):
        problem += pulp.lpSum(x[(i, j)] for j in preferences_students[i][:k]) == 1, f"Assign_Student_{i}"

    # Contrainte : respect des capacités des cours
    for j in range(m):
        course_vars = [x[(i, j)] for i in range(n) if j in preferences_students[i][:k]]
        if course_vars:
            problem += pulp.lpSum(course_vars) <= capacities[j], f"Capacity_Course_{j}"

    # Contrainte : l'utilité de chaque étudiant doit être >= U_min
    for i in range(n):
        utility_expr = pulp.lpSum(combined_borda_scores[i][j] * x[(i, j)] for j in preferences_students[i][:k])
        problem += utility_expr >= U_min, f"Min_Utility_Student_{i}"

    # Résolution du problème avec Gurobi
    solver = pulp.GUROBI_CMD(msg=False)
    result = problem.solve(solver)

    # Vérification de la solution
    if pulp.LpStatus[problem.status] == "Optimal":
        allocation = {(i, j): pulp.value(x[(i, j)]) for i in range(n) for j in preferences_students[i][:k] if pulp.value(x[(i, j)]) == 1}
        total_utility_value = pulp.value(total_utility)
        U_min_value = pulp.value(U_min)
        average_utility = total_utility_value / n

        print(f"Utilité totale atteinte : {total_utility_value}")
        print(f"Utilité moyenne atteinte : {average_utility}")
        print(f"Utilité minimale des étudiants : {U_min_value}")

        return allocation, U_min_value, average_utility
    else:
        print("Aucune solution optimale trouvée.")
        return None, None, None

def main():
    while True:
        print("\n=== Menu Principal ===")
        print("1. Charger les préférences et exécuter Gale-Shapley (Données depuis les fichiers PrefEtu.txt et PrefSpe.txt)")
        print("2. Générer des préférences aléatoires et afficher les matrices et tracer le graphe")
        print("3. Générer un fichier LP pour l'affectation (n = 11, Données depuis les fichiers PrefEtu.txt et PrefSpe.txt)")
        print("4. Trouver le minimum k et afficher une solution maximisant l'utilite minimale des etudiants")
        print("5. Générer un fichier LP pour maximiser les utilités des étudiants et des parcours")
        print("6. Maximiser la somme des utilités (efficacité totale) tout en garantissant une utilité minimale pour les étudiants.")
        print("7. Verifier les couples si ils sont stables ou pas")
        print("8. Quitter")

        choix = input("Votre choix : ")

        if choix == "1":
            # Charger les préférences depuis les fichiers
            CE = lire_pref_etudiants("data/PrefEtu.txt")
            #print(CE)
            CP, capacites = lire_pref_parcours("data/PrefSpe.txt")
            #print(CP)

            # Exécuter les algorithmes Gale-Shapley
            affectations_etudiants = gale_shapley_etudiants(CE, CP, capacites)
            print(affectations_etudiants)
            affectations_parcours = gale_shapley_parcours(CE, CP, capacites)
            print(affectations_parcours)

            # Vérifier la stabilité
            print("\nVérification de la stabilité de l'affectation (étudiants):")
            afficher_paires_instables(trouver_paires_instables(CE, CP, affectations_etudiants))

            print("\nVérification de la stabilité de l'affectation (parcours):")
            afficher_paires_instables(trouver_paires_instables(CE, CP, affectations_parcours))

            # Afficher les résultats finaux
            afficher_affectations_etudiants("Affectations finales (Côté étudiants)", affectations_etudiants)
            afficher_affectations_parcours("Affectations finales (Côté parcours)", affectations_parcours)

        elif choix == "2":
            # Générer des préférences aléatoires
            n = int(input("Entrez le nombre d'étudiants : "))
            CE = generer_pref_etudiants(n)
            CP = generer_pref_parcours(n)

            # Afficher les matrices générées
            afficher_matrice("Matrice CE (Préférences des étudiants) :", CE, "Etudiant ")
            afficher_matrice("Matrice CP (Préférences des parcours) :", CP, "Parcours ")

            print("Veuillez attendre quelques secondes :\n")
            tracer_courbes()

        elif choix == "3":
            # Générer un fichier LP pour l'affectation
            n = 11
            preferences_students = lire_pref_etudiants("data/PrefEtu.txt")
            _, capacities = lire_pref_parcours("data/PrefSpe.txt")
            k = int(input("Entrez la valeur de k : "))
            generate_lp_file_k(n, preferences_students, capacities, k, "affectation_k.lp")
            print("Fichier LP généré : affectation_k.lp")

        elif choix == "4":
            # Tester la fonction find_min_k et afficher le résultat
            n = 11
            m = 9
            preferences_students = lire_pref_etudiants("data/PrefEtu.txt")
            preferences_parcours, capacities = lire_pref_parcours("data/PrefSpe.txt")
            k_min = find_min_k(n, preferences_students, capacities)
            print(f"Le plus petit k pour lequel la solution est faisable est : {k_min}")
            # Maximiser l'utilité minimale des étudiants pour ce k
            allocation, U_min = maximize_min_utility(n, m, preferences_students, preferences_parcours, capacities, k_min)
            print(f"Affectation optimale : {allocation}")
            print(f"Utilité minimale atteinte : {U_min}")

        elif choix == "5":
            # Générer un fichier LP pour maximiser les utilités des étudiants et des parcours
            n = 11
            preferences_students = lire_pref_etudiants("data/PrefEtu.txt")
            preferences_parcours, capacities = lire_pref_parcours("data/PrefSpe.txt")
            k = int(input("Entrez la valeur de k : "))
            generate_lp_file_maximum(n, len(preferences_parcours), preferences_students, preferences_parcours, capacities, k, "affectation_max.lp")
            print("Fichier LP généré : affectation_max.lp")
        
        elif choix == "6":
            n = 11
            preferences_students = lire_pref_etudiants("data/PrefEtu.txt")
            preferences_parcours, capacities = lire_pref_parcours("data/PrefSpe.txt")
            k = int(input("Entrez la valeur de k : "))
            maximize_utility_and_fairness(n, len(preferences_parcours), preferences_students, preferences_parcours, capacities, k)

        elif choix == "7":
            CE = lire_pref_etudiants("data/PrefEtu.txt")
            CP, capacites = lire_pref_parcours("data/PrefSpe.txt")
            
            affectations_etudiants = gale_shapley_etudiants(CE, CP, capacites)
            affectations_parcours = gale_shapley_parcours(CE, CP, capacites)
            print("\nVérification de la stabilité de l'affectation (étudiants):")
            afficher_paires_instables(trouver_paires_instables(CE, CP, affectations_etudiants))

            print("\nVérification de la stabilité de l'affectation (parcours):")
            afficher_paires_instables(trouver_paires_instables(CE, CP, affectations_parcours))

            # resultat du q13 k = 5
            resultat_q13 = {            
                0: [2, 3], 1: [4], 2: [7], 3: [10], 
                4: [1], 5: [6], 6: [8], 7: [5], 8: [0, 9]
            }
            afficher_paires_instables(trouver_paires_instables(CE,CP,resultat_q13))

            # resultat du q14 k = 7
            resultat_q14 = {
                0: [4, 5], 1: [10], 2: [7], 3: [3], 
                4: [9], 5: [0], 6: [8], 7: [6], 8: [1, 2]
            }

            afficher_paires_instables(trouver_paires_instables(CE,CP,resultat_q14))

            # resultat du q15 k* = 5
            resultat_q15 = {
                0: [7, 10], 1: [4], 2: [6], 3: [9], 
                4: [5], 5: [0], 6: [1], 7: [3], 8: [2, 8]
            }
            afficher_paires_instables(trouver_paires_instables(CE,CP,resultat_q15))

        elif choix == "8":
            print("Au revoir !")
            break

        else:
            print("Choix invalide, veuillez réessayer.")
main()