# Projet MOGPL - La balade du robot

## Auteurs
- Yuxiang ZHANG
- Kenan ALSAFADI

## Date
Décembre 2025

## Description
Ce projet résout le problème de la "balade du robot" qui consiste à trouver le chemin optimal pour un robot se déplaçant dans un entrepôt modélisé sous forme de grille avec obstacles. Le robot doit atteindre sa destination en un temps minimal en utilisant des commandes spécifiques d'avancement et de rotation.

## Table des matières
1. [Fonctionnalités implémentées](#fonctionnalités-implémentées)
2. [Structure du projet](#structure-du-projet)
3. [Utilisation](#utilisation)
4. [Formats des fichiers](#formats-des-fichiers)
5. [Résultats des tests](#résultats-des-tests)
6. [Gestion des poids aléatoires](#gestion-des-poids-aléatoires)
7. [Exemple détaillé de génération avec Gurobi](#exemple-détaillé-de-génération-avec-gurobi)
8. [Dépendances et installation](#dépendances-et-installation)

## Fonctionnalités implémentées

### Algorithmes de résolution
- **BFS** (Breadth-First Search) - Parcours en largeur
- **Dijkstra** - Algorithme avec file de priorité  
- **Bellman** - Programmation dynamique avec relâchement d'arcs

### Tests de performance (parties c et d)
- **(c)** Évaluation en fonction de la taille de la grille (de 10×10 à 50×50)
- **(d)** Évaluation en fonction du nombre d'obstacles (de 10 à 50 obstacles)

### Génération de grilles avec contraintes (partie e)
- Génération de grilles avec contraintes structurelles utilisant Gurobi
- Contraintes appliquées :
  - Limites par ligne : au plus ⌊2P/M⌋ obstacles par ligne
  - Limites par colonne : au plus ⌊2P/N⌋ obstacles par colonne
  - Interdiction du motif "101" (obstacle-libre-obstacle) dans les lignes et colonnes
- Interface interactive pour la génération et la comparaison des algorithmes
- **Fonctionnalité avancée** : Affichage et sauvegarde des poids aléatoires (0-1000) attribués à chaque case

## Structure du projet

```
projet_mogpl/
│
├── robot_pathfinder.py          # Programme principal (tout le code est dans un seul fichier)
├── README.md                    # Ce fichier d'instructions
├── rapport.pdf                  # Rapport détaillé du projet
│
├── instances/                   # Dossier pour les fichiers d'instances (créé automatiquement)
│   ├── instance_enonce.txt      # Exemple de fichier d'instance fourni
│   ├── instances_taille.txt     # Généré par l'option 1 (c)
│   ├── instances_obstacles.txt  # Généré par l'option 2 (d)
│   └── instances_generees_par_gurobi.txt # Optionnel : généré par l'option 3 (e) si l'utilisateur choisit de sauvegarder
│
├── resultats/                   # Dossier pour les résultats (créé automatiquement)
│   ├── resultats_bfs.txt        # Résultats avec BFS (option 4)
│   ├── resultats_dijkstra.txt   # Résultats avec Dijkstra (option 5)
│   ├── resultats_bellman.txt    # Résultats avec Bellman (option 6)
│   ├── resultats_detaille_taille.txt     # Résultats détaillés des tests de taille
│   ├── resultats_moyens_taille.txt       # Résultats moyens des tests de taille
│   ├── resultats_detaille_obstacles.txt  # Résultats détaillés des tests d'obstacles
│   ├── resultats_moyens_obstacles.txt    # Résultats moyens des tests d'obstacles
│   ├── resultats_comparaison_algorithmes.txt # Comparaison des algorithmes (option 3)
│   └── poids_grille_MxN_PP_TIMESTAMP.txt     # Fichiers de poids aléatoires (option 3)
│
└── graphiques/                  # Dossier pour les graphiques (créé automatiquement)
    ├── performance_taille.png    # Graphique des tests de taille
    └── performance_obstacles.png # Graphique des tests d'obstacles
```

**Note** : Les dossiers `instances/`, `resultats/` et `graphiques/` sont créés automatiquement lors de l'exécution.

## Utilisation

### Lancement du programme
```bash
python robot_pathfinder.py
```

### Menu principal interactif

Le programme propose un menu interactif avec 7 options :

```
==================================================
         ROBOT PATHFINDER - MENU PRINCIPAL
==================================================
1. Tests de performance - Taille de grille (c)
2. Tests de performance - Nombre d'obstacles (d)
3. Génération avec contraintes et Gurobi (e)
4. Résoudre un fichier avec BFS
5. Résoudre un fichier avec Dijkstra
6. Résoudre un fichier avec Bellman
7. Quitter
--------------------------------------------------
```

#### 1. Tests de performance - Taille de grille (c)
- Génère automatiquement 50 instances (10 pour chaque taille : 10×10, 20×20, 30×30, 40×40, 50×50)
- Teste les 3 algorithmes sur chaque instance
- Produit :
  - Graphique comparatif (`graphiques/performance_taille.png`)
  - Résultats détaillés (`resultats/resultats_detaille_taille.txt`)
  - Résultats moyens (`resultats/resultats_moyens_taille.txt`)
  - Fichier d'instances (`instances/instances_taille.txt`)

#### 2. Tests de performance - Nombre d'obstacles (d)
- Génère 50 instances avec une grille fixe 20×20 (10 pour chaque nombre d'obstacles : 10, 20, 30, 40, 50)
- Compare les performances des 3 algorithmes
- Produit :
  - Graphique comparatif (`graphiques/performance_obstacles.png`)
  - Résultats détaillés (`resultats/resultats_detaille_obstacles.txt`)
  - Résultats moyens (`resultats/resultats_moyens_obstacles.txt`)
  - Fichier d'instances (`instances/instances_obstacles.txt`)

#### 3. Génération avec contraintes et Gurobi (e)
- **Interface interactive** pour créer des grilles avec contraintes spécifiques
- **Gurobi** est utilisé pour résoudre le programme linéaire (méthode heuristique en backup)
- Étapes de l'interface :
  1. Saisie des dimensions M et N (≤ 50)
  2. Saisie du nombre d'obstacles P
  3. Génération de la grille avec contraintes
  4. **Fonctionnalité avancée** : Affichage et sauvegarde optionnelle des poids aléatoires
  5. Vérification détaillée des contraintes
  6. Sélection des positions de départ et d'arrivée (croisements)
  7. Sélection de la direction initiale
  8. Comparaison des 3 algorithmes sur la même instance
- Produit :
  - Fichier de comparaison (`resultats/resultats_comparaison_algorithmes.txt`)
  - **Fichiers de poids** : Optionnel, si l'utilisateur choisit de sauvegarder (`resultats/poids_grille_MxN_PP_TIMESTAMP.txt`)
  - **Sauvegarde automatique** : À la fin de la génération, le programme demande si vous voulez sauvegarder l'instance dans `instances/instances_generees_par_gurobi.txt`

#### 4-6. Résolution d'un fichier avec un algorithme spécifique
- Permet de résoudre un fichier d'instances existant avec un algorithme choisi
- **Format du chemin d'accès** : Utilisez le chemin relatif, par exemple `instances/instance_enonce.txt`
- Formate la sortie selon les spécifications du projet
- Sauvegarde les résultats dans un fichier dédié :
  - BFS : `resultats/resultats_bfs.txt`
  - Dijkstra : `resultats/resultats_dijkstra.txt`
  - Bellman : `resultats/resultats_bellman.txt`

#### 7. Quitter
- Ferme le programme proprement

## Formats des fichiers

### Explication du système de coordonnées

**Important** : Il existe **deux systèmes de coordonnées** distincts dans ce problème :

1. **Coordonnées des cases (grille)** : (ligne, colonne) ∈ [0, M-1] × [0, N-1]
   - Utilisées pour les obstacles (0 = libre, 1 = obstacle)
   - (0,0) = coin nord-ouest (en haut à gauche)
   - (M-1, N-1) = coin sud-est (en bas à droite)

2. **Coordonnées des croisements** : (x, y) ∈ [0, M] × [0, N]
   - Utilisées pour les positions du robot (départ et arrivée)
   - Le robot se positionne sur les **intersections des rails**, pas sur les cases
   - Chaque croisement (x,y) couvre les 4 cases adjacentes :
     - Case en haut à gauche : (x-1, y-1) si dans les limites
     - Case en haut à droite : (x-1, y) si dans les limites  
     - Case en bas à gauche : (x, y-1) si dans les limites
     - Case en bas à droite : (x, y) si dans les limites

**Visualisation** :
```
Coordonnées des croisements (x,y)    Cases de la grille [ligne][colonne]
                                 y=0    y=1    y=2    ...    y=N
x=0  →  (0,0)  (0,1)  (0,2) ...      [0][0]  [0][1]  [0][2] ...  [0][N-1]
x=1  →  (1,0)  (1,1)  (1,2) ...      [1][0]  [1][1]  [1][2] ...  [1][N-1]
...                                  ...
x=M  →  (M,0)  (M,1)  (M,2) ...      [M-1][0][M-1][1][M-1][2] ... [M-1][N-1]
```

**Exemple concret** : Pour une grille de 9×10 (M=9, N=10) :
- Indices des cases : de (0,0) à (8,9)
- Coordonnées des croisements : 
  - x : de 0 à 9 (inclus) → 10 valeurs possibles
  - y : de 0 à 10 (inclus) → 11 valeurs possibles
- Nombre total de croisements : (9+1) × (10+1) = 110 croisements

**Validation d'un croisement** : Un croisement (x,y) est sûr si **toutes les cases adjacentes existantes** sont libres :
- Pour x=0, y=0 : vérifie seulement la case (0,0)
- Pour x=9, y=10 : vérifie seulement la case (8,9)
- Pour x=5, y=5 : vérifie les 4 cases (4,4), (4,5), (5,4), (5,5)

### Format d'entrée pour les instances

Le fichier d'instances doit suivre ce format strict, en utilisant le système de coordonnées expliqué ci-dessus :

```
M N
grid[0][0] grid[0][1] ... grid[0][N-1]
grid[1][0] grid[1][1] ... grid[1][N-1]
...
grid[M-1][0] grid[M-1][1] ... grid[M-1][N-1]
start_x start_y end_x end_y direction
[bloc suivant...]
0 0
```

**Exemple concret** (basé sur l'instance fournie dans l'énoncé) :
```
9 10
0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 1 0
0 0 0 1 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 1 0 0 0 0
0 0 0 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 1 0
7 2 2 7 sud
0 0
```

**Détails des champs** :
- `M` : nombre de lignes (1 ≤ M ≤ 50)
- `N` : nombre de colonnes (1 ≤ N ≤ 50)
- `grid[i][j]` : `0` pour libre, `1` pour obstacle (coordonnées de case)
- `start_x, start_y` : coordonnées du **croisement** de départ (x ∈ [0,M], y ∈ [0,N])
- `end_x, end_y` : coordonnées du **croisement** d'arrivée (x ∈ [0,M], y ∈ [0,N])
- `direction` : direction initiale (`nord`, `est`, `sud`, `ouest`)
- `0 0` : marqueur de fin de fichier

### Format de sortie des résultats

Pour chaque instance, une ligne contenant :
- Le temps minimal en secondes, suivi des commandes séparées par des espaces
- Ou `-1` si aucun chemin n'existe

**Exemple** :
```
12 D a1 D a3 a3 D a3 a1 D a1 G a2
-1
```

**Commandes** :
- `a1`, `a2`, `a3` : avancer de 1, 2 ou 3 cases
- `G` : tourner à gauche
- `D` : tourner à droite

## Résultats des tests

### Résolution de fichiers d'instances

**Avec BFS :**
```
Nom du fichier d'instances: instances/instance_enonce.txt

=== RÉSULTATS AVEC BFS ===
12 D a1 D a3 a3 D a1 a3 D a1 G a2

Temps total de calcul: 0.004011 secondes
Résultats sauvegardés dans 'resultats/resultats_bfs.txt'
```

**Avec Dijkstra :**
```
Nom du fichier d'instances: instances/instance_enonce.txt

=== RÉSULTATS AVEC Bellman ===
12 D a2 D a3 a3 D a2 a3 D a1 G a2

Temps total de calcul: 0.004958 secondes
Résultats sauvegardés dans 'resultats/resultats_dijkstra.txt'
```

**Avec Bellman :**
```
Nom du fichier d'instances: instances/instance_enonce.txt

=== RÉSULTATS AVEC Bellman ===
12 D a2 D a3 a3 D a2 a3 D a1 G a2

Temps total de calcul: 0.027291 secondes
Résultats sauvegardés dans 'resultats/resultats_bellman.txt'
```

### Tests de performance - Taille de grille (c)

Les résultats moyens obtenus pour différentes tailles de grille sont :

```
=== RÉSULTATS MOYENS TESTS TAILLE ===
Taille | BFS (s)     | Dijkstra (s) | Bellman (s)
-------|-------------|-------------|-------------
    10 | 0.001071   | 0.001226   | 0.009954
    20 | 0.003060   | 0.003597   | 0.066110
    30 | 0.009008   | 0.010636   | 0.185021
    40 | 0.017126   | 0.019999   | 0.459039
    50 | 0.020263   | 0.023807   | 0.832398
```

### Tests de performance - Nombre d'obstacles (d)

Les résultats moyens obtenus pour différents nombres d'obstacles (sur une grille 20×20) sont :

```
=== RÉSULTATS MOYENS TESTS OBSTACLES ===
Obstacles | BFS (s)    | Dijkstra (s) | Bellman (s)
----------|------------|-------------|-------------
       10 | 0.027974  | 0.027268   | 0.293152
       20 | 0.011834  | 0.012888   | 0.351492
       30 | 0.019906  | 0.022268   | 0.338031
       40 | 0.017052  | 0.020726   | 0.292523
       50 | 0.005820  | 0.006748   | 0.227604
```

## Gestion des poids aléatoires

### Description
Dans le cadre de la partie (e) du projet, chaque case de la grille reçoit un poids aléatoire entre 0 et 1000. L'objectif de Gurobi est de minimiser la somme des poids des cases sélectionnées comme obstacles, tout en respectant les contraintes structurelles.

### Fonctionnalités implémentées
1. **Génération aléatoire** : Attribution automatique d'un poids à chaque case
2. **Affichage dans la console** : Option pour visualiser la matrice des poids
3. **Sauvegarde dans un fichier** : Option pour exporter les poids avec statistiques
4. **Intégration dans les résultats** : Les statistiques des poids sont incluses dans le fichier de comparaison

### Format des fichiers de poids
```
# Matrice de poids aléatoires pour grille MxN avec P obstacles
# Poids générés aléatoirement entre 0 et 1000
# Les obstacles sont indiqués par [poids]

Format: Ligne,Colonne,Est_Obstacle,Poids
--------------------------------------------------
0,0,0,550
0,1,0,538
0,2,0,238
...
49,47,0,837
49,48,0,357
49,49,0,177

==================================================
STATISTIQUES:
Somme de tous les poids: 1264761
Somme des poids des obstacles: 2341
Nombre d'obstacles: 100
Poids moyen de tous les cases: 505.90
Poids moyen des obstacles: 23.41
Pourcentage du poids total utilisé: 0.19%
```

## Exemple détaillé de génération avec Gurobi

### Génération d'une grille 50×50 avec 100 obstacles

```
=== GÉNÉRATION DE GRILLES AVEC CONTRAINTES (GUROBI) ===
Test des trois algorithmes sur la même grille
Hauteur de la grille (M, nombre de lignes, 1-50): 50
Largeur de la grille (N, nombre de colonnes, 1-50): 50
Nombre d'obstacles (P, 0 à 2500): 100

Contraintes appliquées (selon l'énoncé):
- Obstacles totaux: 100
- Max par ligne: 4 (2P/M = 4.00, arrondi à l'entier inférieur)
- Max par colonne: 4 (2P/N = 4.00, arrondi à l'entier inférieur)
- Aucune séquence '101' (1-0-1) dans aucune ligne ou colonne

Génération de la grille avec Gurobi...
Étape 1: Génération des poids aléatoires (0-1000) pour chaque case...
Set parameter Username
Set parameter LicenseID to value 2620263
Academic license - for non-commercial use only - expires 2026-02-10
Grille générée en 0.29 secondes
```

### Statistiques des poids aléatoires

```
STATISTIQUES DES POIDS:
  Tous les poids: min=0, max=1000, moyenne=505.9
  Poids des obstacles (100): min=0, max=61, moyenne=23.4
  Somme des poids des obstacles: 2341

  Obstacles sélectionnés (poids les plus bas):
    Position (12,44): poids = 0
    Position (16,26): poids = 0
    Position (22,46): poids = 0
    Position (42,40): poids = 0
    Position (4,38): poids = 1
  ... et 95 autres obstacles

  Obstacle avec le poids le plus élevé (coûteux):
    Position (4,37): poids = 61
```

### Comparaison des algorithmes

```
=== POINT DE DÉPART ===
Coordonnée x du croisement de départ (0 à 50): 0
Coordonnée y du croisement de départ (0 à 50): 0

=== POINT D'ARRIVÉE ===
Coordonnée x du croisement d'arrivée (0 à 50): 50
Coordonnée y du croisement d'arrivée (0 à 50): 50

=== DIRECTION INITIALE ===
Direction initiale du robot: nord

============================================================
COMPARAISON DES TROIS ALGORITHMES
============================================================

--- Exécution de BFS ---
Résultat: 38 secondes
Nombre de commandes: 38
Commandes (premières 20): D a2 a3 a3 a3 a3 a3 a3 D a2 a3 a3 a3 a3 a3 a3 G a3 a3 a3...
Temps de calcul: 0.300591 secondes

--- Exécution de Dijkstra ---
Résultat: 38 secondes
Nombre de commandes: 38
Commandes (premières 20): D a2 a3 a3 a3 a3 a3 a3 D a2 a3 a3 a3 a3 a3 a3 G a3 a3 a3...
Temps de calcul: 0.367222 secondes

--- Exécution de Bellman ---
Résultat: 38 secondes
Nombre de commandes: 38
Commandes (premières 20): D a2 a3 a3 a3 a3 a3 a3 D a2 a3 a3 a3 a3 a3 a3 G a3 a3 a3...
Temps de calcul: 1.681684 secondes
```

## Dépendances et installation

### Dépendances requises
- Python 3.6 ou supérieur
- Matplotlib (pour les graphiques)
- Gurobi (pour la génération optimale de grilles avec contraintes)

### Installation des dépendances
```bash
# Installer matplotlib
pip install matplotlib

# Installer Gurobi (optionnel, mais recommandé pour la partie e)
# Note: Gurobi nécessite une licence académique gratuite
pip install gurobipy
```

### Configuration de Gurobi
1. Obtenir une licence académique gratuite sur [le site de Gurobi](https://www.gurobi.com/)
2. Suivre les instructions d'installation pour votre système
3. Configurer la licence avec la commande `grbgetkey`

### Exécution sans Gurobi
Si Gurobi n'est pas installé, le programme utilisera automatiquement une méthode heuristique pour générer les grilles avec contraintes (option 3). Un message d'avertissement s'affichera dans le menu.

## Conclusion

Ce projet implémente complètement la "balade du robot" avec trois algorithmes différents, des tests de performance complets, et une génération sophistiquée de grilles avec contraintes. L'interface utilisateur interactive facilite l'exploration des différentes fonctionnalités.