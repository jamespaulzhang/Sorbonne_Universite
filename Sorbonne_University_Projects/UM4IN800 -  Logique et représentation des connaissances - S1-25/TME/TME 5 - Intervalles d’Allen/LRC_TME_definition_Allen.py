# Yuxiang ZHANG 21202829
# Kenan ALSAFADI 21502362

#### Dictionnaires décrivant les transposées et symétries de relations, 
#### ainsi que les listes de relations obtenues avec les compositions de base
#### dans le tableau donné en cours

# --- Dictionnaire des transposées : relation inversée dans le temps ---
transpose = {
    '<':'>',
    '>':'<',
    'e':'et',
    's':'st',
    'et':'e',
    'st':'s',
    'd':'dt',
    'm':'mt',
    'dt':'d',
    'mt':'m',
    'o':'ot',
    'ot':'o',
    '=':'='                 
}

# --- Dictionnaire des symétries : relation miroir (échange passé/futur) ---
symetrie = {
    '<':'>',
    '>':'<',
    'e':'s',
    's':'e',
    'et':'st',
    'st':'et',
    'd':'d',
    'm':'mt',
    'dt':'dt',
    'mt':'m',
    'o':'ot',
    'ot':'o',
    '=':'='
}

# --- Table de composition de base (r1 ◦ r2) → ensemble de relations possibles ---
compositionBase = {        
    ('<','<'):{'<'},
    ('<','m'):{'<'},
    ('<','o'):{'<'},
    ('<','et'):{'<'},
    ('<','s'):{'<'},
    ('<','d'):{'<','m','o','s','d'},
    ('<','dt'):{'<'},
    ('<','e'):{'<','m','o','s','d'},
    ('<','st'):{'<'},
    ('<','ot'):{'<','m','o','s','d'},
    ('<','mt'):{'<','m','o','s','d'},
    ('<','>'):{'<','>','m','mt','o','ot','e','et','s','st','d','dt','='},
    ('m','m'):{'<'},
    ('m','o'):{'<'},
    ('m','et'):{'<'},
    ('m','s'):{'m'},
    ('m','d'):{'o','s','d'},
    ('m','dt'):{'<'},
    ('m','e'):{'o','s','d'},
    ('m','st'):{'m'},
    ('m','ot'):{'o','s','d'},
    ('m','mt'):{'e','et','='},
    ('o','o'):{'<','m','o'},
    ('o','et'):{'<','m','o'},
    ('o','s'):{'o'},
    ('o','d'):{'o','s','d'},
    ('o','dt'):{'<','m','o','et','dt'},
    ('o','e'):{'o','s','d'},
    ('o','st'):{'o','et','dt'},
    ('o','ot'):{'o','ot','e','et','d','dt','st','s','='},
    ('s','et'):{'<','m','o'},
    ('s','s'):{'s'},
    ('s','d'):{'d'},
    ('s','dt'):{'<','m','o','et','dt'},
    ('s','e'):{'d'},
    ('s','st'):{'s','st','='},
    ('et','s'):{'o'},
    ('et','d'):{'o','s','d'},
    ('et','dt'):{'dt'},
    ('et','e'):{'e','et','='},
    ('d','d'):{'d'},
    ('d','dt'):{'<','>','m','mt','o','ot','e','et','s','st','d','dt','='},
    ('dt','d'):{'o','ot','e','et','d','dt','st','s','='}
}

# ------------------------------------------------------------
# --- FONCTIONS DE BASE SUR LES ENSEMBLES DE RELATIONS ---
# ------------------------------------------------------------

def transposeSet(S):
    """
    Renvoie l'ensemble des transposées d'un ensemble de relations S.
    Exemple : {'<' , 'd'} -> {'>', 'dt'}.
    """
    return {transpose[s] for s in S}

def symetrieSet(S):
    """
    Renvoie l'ensemble des symétries d'un ensemble de relations S.
    Exemple : {'<' , 'd'} -> {'>', 'd'}.
    """
    return {symetrie[s] for s in S}

def compose(r1: str, r2: str) -> set:
    """
    Calcule la composition de deux relations d'Allen : r1 ◦ r2.
    Stratégie hiérarchique (4 niveaux de recherche) :
     1. Recherche directe dans la table compositionBase.
     2. Astuce de transposée : r1◦r2 = (r2^t ◦ r1^t)^t.
     3. Astuce de symétrie : r1◦r2 = (r1^s ◦ r2^s)^s.
     4. Double astuce : r1◦r2 = (r2^{st} ◦ r1^{st})^{ts}.
    Retour :
        Ensemble des relations résultantes (éventuellement vide).
    """

    # Cas neutre : la relation "=" ne modifie rien
    if r1 == "=":
        return {r2}
    if r2 == "=":
        return {r1}
    
    # 1) Composition directe
    direct = compositionBase.get((r1, r2))
    if direct is not None:
        return set(direct)

    # 2) Utilisation de la transposée
    try:
        rt1 = transpose[r1]
        rt2 = transpose[r2]
        comp = compositionBase.get((rt2, rt1))
        if comp is not None:
            return transposeSet(set(comp))
    except KeyError:
        pass

    # 3) Utilisation de la symétrie
    try:
        rs1 = symetrie[r1]
        rs2 = symetrie[r2]
        comp = compositionBase.get((rs1, rs2))
        if comp is not None:
            return symetrieSet(set(comp))
    except KeyError:
        pass

    # 4) Astuce double (symétrie + transposée)
    try:
        rst1 = transpose[symetrie[r1]]
        rst2 = transpose[symetrie[r2]]
        comp = compositionBase.get((rst2, rst1))
        if comp is not None:
            return symetrieSet(transposeSet(set(comp)))
    except KeyError:
        pass

    # Si aucune règle n'est applicable
    return set()

def compositionSet(S1, S2):
    """
    Calcule la composition de deux ensembles de relations :
        S1 ◦ S2 = ⋃_{r1∈S1, r2∈S2} (r1 ◦ r2)
    """
    result = set()
    for r1 in S1:
        for r2 in S2:
            result |= compose(r1, r2)
    return result

# ------------------------------------------------------------
# --- CLASSE PRINCIPALE : GRAPHE TEMPOREL D'ALLEN ---
# ------------------------------------------------------------

class Graphe:
    """
    Représente un graphe temporel au sens d'Allen.
    Chaque nœud correspond à un intervalle temporel,
    et chaque arête (i,j) décrit les relations temporelles possibles entre eux.
    """

    def __init__(self, noeuds=None, relations=None):
        """
        Initialise un graphe vide ou avec des nœuds et relations donnés.
        """
        self.noeuds = noeuds if noeuds is not None else set()
        self.relations = relations if relations is not None else dict()

    def getRelations(self, i: str, j: str):
        """
        Renvoie l'ensemble des relations connues entre deux intervalles i et j.
        Si (i,j) n'existe pas, retourne l'ensemble complet de 13 relations d'Allen.
        Si seule la relation inverse (j,i) existe, renvoie sa transposée.
        """
        if (i,j) in self.relations:
            return set(self.relations[(i,j)])
        if (j,i) in self.relations:
            return transposeSet(self.relations[(j,i)])
        # Ensemble maximal = absence de contrainte
        return {'<','>','m','mt','o','ot','e','et','s','st','d','dt','='}
    
    def set_relation(self, a: str, b: str, rels: set[str]):
        """
        Définit la relation entre a et b, et met automatiquement à jour
        la relation transposée (b,a) = transpose(rels).
        """
        self.relations[(a, b)] = set(rels)
        self.relations[(b, a)] = transposeSet(set(rels))

    def propagation(self, i: str, j: str, verbose=False):
        """
        Propage les contraintes dans le graphe à partir de la relation (i,j),
        selon l’algorithme de cohérence de chemin (path consistency).
        Chaque fois qu’une relation est restreinte, les conséquences
        sur les autres arcs sont recalculées.
        """
        pile = [(i, j)]

        while pile:
            (i, j) = pile.pop()
            Rij = self.getRelations(i, j)

            for k in self.noeuds:
                if k in (i, j):
                    continue

                # --- Propagation vers Rik ---
                Rik = self.getRelations(i, k)
                Rjk = self.getRelations(j, k)
                newRik = Rik.intersection(compositionSet(Rij, Rjk))
                if not newRik:
                    raise ValueError(f"⚠️ Contradiction temporelle entre {i} et {k}")
                if newRik != Rik:
                    self.set_relation(i, k, newRik)
                    pile.append((i, k))
                    if verbose:
                        print(f"[MàJ] {i}-{k} ← {newRik}")

                # --- Propagation vers Rkj ---
                Rki = self.getRelations(k, i)
                newRkj = self.getRelations(k, j).intersection(compositionSet(Rki, Rij))
                if not newRkj:
                    raise ValueError(f"⚠️ Contradiction temporelle entre {k} et {j}")
                if newRkj != self.getRelations(k, j):
                    self.set_relation(k, j, newRkj)
                    pile.append((k, j))
                    if verbose:
                        print(f"[MàJ] {k}-{j} ← {newRkj}")

    def ajouter(self, i: str, j: str, rels: set[str], verbose=False):
        """
        Ajoute une contrainte (i,j) au graphe et propage les effets de cette
        contrainte à l’ensemble des autres relations du graphe.
        Si un des nœuds est nouveau, il est automatiquement ajouté.
        """
        if i not in self.noeuds:
            self.noeuds.add(i)
            if verbose:
                print(f"[Ajout nœud] {i}")
        if j not in self.noeuds:
            self.noeuds.add(j)
            if verbose:
                print(f"[Ajout nœud] {j}")

        old_rels = self.getRelations(i, j)
        new_rels = old_rels & set(rels)

        if not new_rels:
            raise ValueError(f"⚠️ Contradiction : aucune relation possible entre {i} et {j}")

        self.set_relation(i, j, new_rels)
        if verbose:
            print(f"[Ajout relation] {i}–{j} ← {new_rels}")

        try:
            self.propagation(i, j, verbose=verbose)
        except ValueError as e:
            print(f"[Erreur propagation] {e}")

    def retirer(self, n: str):
        """
        Supprime un nœud du graphe ainsi que toutes ses relations associées.
        Si le nœud n’existe pas, ne fait rien.
        """
        if n not in self.noeuds:
            return

        self.noeuds.remove(n)
        to_remove = [(i, j) for (i, j) in self.relations.keys() if i == n or j == n]
        for key in to_remove:
            del self.relations[key]

# ------------------------------------------------------------
# --- PROGRAMME PRINCIPAL DE TEST / MENU INTERACTIF ---
# ------------------------------------------------------------

def main():
    """
    Interface interactive permettant de tester différentes configurations
    de graphes temporels d’Allen. 
    L’utilisateur peut choisir un scénario parmi plusieurs exercices.
    """
    while True:
        print("\n=== Allen Intervals - Menu ===")
        print("1 - Test Compose de base")
        print("2 - Cas 1 : A{<}B, A{>}C, puis B{=}C")
        print("3 - Cas 2 : A{<}B, A{<}C, puis B{=}C")
        print("4 - Exercice 1 : Graphe temporel Jean / Colis")
        print("5 - Exercice 3 : Conducteur / Moteur / Voiture")
        print("6 - Exercice 4 : Alfred et son petit-déjeuner")
        print("0 - Quitter")

        choix = input("Sélectionnez une option : ")

        if choix == '1':
            print("\n--- Test Compose de base ---")
            print("= ◦ d  ->", compose("=", "d"))
            print("m ◦ d  ->", compose("m", "d"))
            print("ot ◦ > ->", compose("ot", ">"))
            print("> ◦ e  ->", compose(">", "e"))
            print("ot ◦ m ->", compose("ot", "m"))

        elif choix == '2':
            print("\n--- Cas 1 : A{<}B, A{>}C, propagation B{=}C ---")
            g1 = Graphe()
            g1.ajouter('A', 'B', {'<'}, verbose=True)
            g1.ajouter('A', 'C', {'>'}, verbose=True)
            g1.ajouter('B', 'C', {'='}, verbose=True)
            print("\nÉtat final du graphe 1 :")
            print("Noeuds :", g1.noeuds)
            print("Relations :", g1.relations)

        elif choix == '3':
            print("\n--- Cas 2 : A{<}B, A{<}C, propagation B{=}C ---")
            g2 = Graphe()
            g2.ajouter('A','B', {'<'}, verbose=True)
            g2.ajouter('A','C', {'<'}, verbose=True)
            g2.ajouter('B','C', {'='}, verbose=True)
            print("\nÉtat final du graphe 2 :")
            print("Noeuds :", g2.noeuds)
            print("Relations :", g2.relations)

        elif choix == '4':
            print("\n--- Exercice 1 : Graphe temporel Jean / Colis ---")
            g = Graphe()
            g.ajouter('tE','tH', {'d'}, verbose=True)
            g.ajouter('tH','tA', {'et'}, verbose=True)
            g.ajouter('tE','tL', {'<'}, verbose=True)
            g.ajouter('tL','tA', {'<'}, verbose=True)
            print("\nGraphe final Exercice 1 :")
            print("Noeuds :", g.noeuds)
            print("Relations :")
            for k,v in g.relations.items():
                print(f"{k} : {v}")

        elif choix == '5':
            print("\n--- Exercice 3 : Conducteur / Moteur / Voiture ---")
            g3 = Graphe()
            g3.ajouter('C','T', {'m','o'}, verbose=True)
            g3.ajouter('R','T', {'=','d','e','s'}, verbose=True)
            CR_possible = compositionSet(g3.getRelations('C','T'), g3.getRelations('T','R'))
            print("\nContraintes déduites entre C et R :", CR_possible)
            g3.ajouter('C','R', CR_possible, verbose=True)
            for k,v in g3.relations.items():
                print(f"{k} : {v}")

        elif choix == '6':
            print("\n--- Exercice 4 : Alfred et son petit-déjeuner ---")
            g4 = Graphe()
            g4.ajouter('IJ','ID', {'o','et','dt','s','=','st','d','e','ot'}, verbose=True)
            g4.ajouter('IC','IJ', {'d','et','e','o','=','s'}, verbose=True)
            g4.ajouter('ID','IP', {'<','m'}, verbose=True)
            g4.ajouter('IC','ID', {'s','d','=','e'}, verbose=True)
            print("\nGraphe final Exercice 4 :")
            print("Noeuds :", g4.noeuds)
            print("Relations :")
            for k,v in g4.relations.items():
                print(f"{k} : {v}")

        elif choix == '0':
            print("Au revoir !")
            break
        else:
            print("Option invalide !")

if __name__ == "__main__":
    main()

"""
--- Exercice 1 : Graphe temporel Jean / Colis ---

# Étape 1 : Ajout des nœuds correspondant aux intervalles d’Allen
[Ajout nœud] tE   # tE : intervalle de la notification d’envoi de colis
[Ajout nœud] tH   # tH : intervalle où Jean est à domicile

# Étape 2 : Ajout des contraintes entre tE et tH
[Ajout relation] tE–tH ← {'d'}   
# d (during) : tE est entièrement inclus dans tH → la notification d’envoi s’est déroulée pendant que Jean était chez lui

# Étape 3 : Ajout du nœud tA
[Ajout nœud] tA   # tA : intervalle correspondant à la notification d’abandon de livraison

# Étape 4 : Ajout des contraintes entre tH et tA
[Ajout relation] tH–tA ← {'et'}  
# et (ended by) : tH se termine en même temps que tA → Jean est chez lui jusqu’à la notification d’abandon

# Étape 5 : Mise à jour de la relation tE–tA via composition
[MàJ] tE-tA ← {'o', 'm', 's', 'd', '<'}  
# Propagation : déduction des relations possibles entre tE et tA à partir de tE–tH et tH–tA

# Étape 6 : Ajout du nœud tL (passage du livreur)
[Ajout nœud] tL

# Étape 7 : Ajout des contraintes entre tE et tL
[Ajout relation] tE–tL ← {'<'}  
# < (before) : tE se termine avant le passage du livreur

# Étape 8 : Propagation de la contrainte C3 (tH–tL)
[MàJ] tH-tL ← {'o', 'm', 'dt', '<', 'et'}  
# Mise à jour après composition avec tE–tL, 
# le graphe n’est pas contradictoire et l’arc contient plusieurs relations

# Étape 9 : Ajout de la contrainte entre tL et tA
[Ajout relation] tL–tA ← {'<'}  

# Étape 10 : Propagation pour dériver tL{d}tH (C5)
[MàJ] tL-tH ← {'d'}  
# d (during) : tL est entièrement inclus dans tH → le passage du livreur s’est produit pendant que Jean était chez lui

# Étape 11 : Mise à jour finale de tE–tA
[MàJ] tE-tA ← {'<'}  

# Graphe final complet :
# Noeuds : {'tH', 'tA', 'tL', 'tE'}
# Relations finales entre intervalles :
('tE', 'tH') : {'d'}        # tE est pendant tH
('tH', 'tE') : {'dt'}       # transposé : tH contient tE
('tH', 'tA') : {'et'}       # tH se termine avec tA
('tA', 'tH') : {'e'}        # tA se termine en même temps que tH
('tE', 'tA') : {'<'}        # tE se termine avant tA
('tA', 'tE') : {'>'}        # transposé : tA commence après tE
('tE', 'tL') : {'<'}        # tE avant tL
('tL', 'tE') : {'>'}        # transposé : tL après tE
('tH', 'tL') : {'dt'}       # tH contient tL
('tL', 'tH') : {'d'}        # tL est pendant tH
('tL', 'tA') : {'<'}        # tL avant tA
('tA', 'tL') : {'>'}        # transposé : tA après tL

--- Exercice 3 : Conducteur / Moteur / Voiture ---

# Étape 1 : Ajout des nœuds correspondant aux intervalles d’Allen
[Ajout nœud] C   # C : intervalle où le conducteur enclenche la clé
[Ajout nœud] T   # T : intervalle pendant lequel le moteur tourne

# Étape 2 : Ajout des contraintes entre C et T
[Ajout relation] C–T ← {'m', 'o'}   
# m (meets) : C se termine exactement au moment où T commence
# o (overlaps) : C commence avant T et se chevauche partiellement avec T

# Étape 3 : Ajout du nœud R
[Ajout nœud] R   # R : intervalle pendant lequel la voiture roule

# Étape 4 : Ajout des contraintes entre R et T
[Ajout relation] R–T ← {'d', 's', '=', 'e'}  
# d (during) : R est entièrement inclus dans T → la voiture roule seulement quand le moteur tourne
# s (starts) : R commence en même temps que T
# = (equals) : R et T ont exactement la même durée
# e (ends) : R se termine en même temps que T

# Étape 5 : Propagation des contraintes pour déduire les relations entre C et R
[MàJ] R–C ← {'>', 'mt', 'd', 'e', 'ot'}  
# R–C est mis à jour via la composition des relations entre C–T et R–T

# Étape 6 : Contraintes déduites entre C et R
Contraintes déduites entre C et R : {'m', 'et', 'dt', 'o', '<'}  
# m (meets) : C se termine quand R commence
# et (ended by) : C se termine en même temps que R
# dt (during inverse) : C contient entièrement R
# o (overlaps) : C chevauche partiellement R
# < (before) : C se termine avant que R commence

# Étape 7 : Mise à jour finale de la relation C–R
[Ajout relation] C–R ← {'m', 'dt', 'et', 'o', '<'}

# Étape 8 : Visualisation des relations finales
('C', 'T') : {'m', 'o'}     # Relation directe C→T
('T', 'C') : {'mt', 'ot'}   # Transposée de C→T
('R', 'T') : {'d', 's', '=', 'e'}  # Relation directe R→T
('T', 'R') : {'dt', 'st', '=', 'et'}  # Transposée de R→T
('R', 'C') : {'d', 'mt', '>', 'e', 'ot'}  # R→C après composition
('C', 'R') : {'m', 'o', 'dt', 'et', '<'}  # C→R après propagation

--- Exercice 4 : Alfred et son petit-déjeuner ---

# Étape 1 : Ajout des nœuds correspondant aux intervalles d’Allen
[Ajout nœud] IJ   # IJ : Alfred lit son journal
[Ajout nœud] ID   # ID : Alfred prend son petit-déjeuner

# Étape 2 : Contraintes entre IJ et ID (première phrase)
[Ajout relation] IJ–ID ← {'d', '=', 'st', 'ot', 'dt', 'e', 'o', 's', 'et'}
# d (during)        : IJ est entièrement inclus dans ID → lire le journal pendant le petit-déjeuner
# dt (during inverse): ID est entièrement inclus dans IJ → théoriquement possible si lecture longue
# o (overlaps)      : IJ commence avant ID et se chevauche partiellement
# ot (overlapped by) : IJ est chevauché partiellement par ID
# s (starts)        : IJ commence en même temps que ID
# st (started by)   : IJ est commencé par ID
# e (ends)          : IJ se termine en même temps que ID
# et (ended by)     : IJ est terminé par ID
# = (equals)        : IJ et ID ont exactement la même durée

# Étape 3 : Ajout du nœud IC
[Ajout nœud] IC   # IC : Alfred boit son café

# Étape 4 : Contraintes entre IC et IJ (deuxième phrase)
[Ajout relation] IC–IJ ← {'d', 'o', '=', 's', 'e', 'et'}
# d (during)        : boire le café est inclus dans le temps de lecture
# o (overlaps)      : café et lecture se chevauchent
# s (starts)        : café commence en même temps que lecture
# e (ends)          : café se termine en même temps que lecture
# et (ended by)     : café est terminé par lecture
# = (equals)        : café et lecture ont même durée (théorique)
# Ces relations expriment que boire le café se déroule pendant la lecture du journal

# Étape 5 : Ajout du nœud IP
[Ajout nœud] IP   # IP : Alfred se promène

# Étape 6 : Contraintes entre ID et IP (troisième phrase)
[Ajout relation] ID–IP ← {'<', 'm'}
# < (before)        : petit-déjeuner terminé avant promenade
# m (meets)         : petit-déjeuner se termine exactement au moment où commence la promenade

# Étape 7 : Propagation des contraintes
[MàJ] IJ–IP ← {'<', 'dt', 'o', 'm', 'et'}
# Propagation : combinaison des contraintes IJ–ID et ID–IP
# → On peut en déduire comment lecture du journal et promenade se situent dans le temps

[MàJ] IC–ID ← {'d', 'e', '=', 's'}
# IC est une étape du petit-déjeuner → propagation contraint IC à rester inclus dans ID

[MàJ] IC–IP ← {'m', '<'}
# Propagation : boire le café doit se terminer avant le début de la promenade

# Étape 8 : Graphe final
Graphe final Exercice 4 :
Noeuds : {'IC', 'IP', 'ID', 'IJ'}
Relations :
('IJ', 'ID') : {'d', '=', 'st', 'ot', 'dt', 'e', 'o', 's', 'et'}
('ID', 'IJ') : {'d', '=', 'st', 'ot', 'dt', 'e', 'o', 's', 'et'}
('IC', 'IJ') : {'d', 'o', '=', 's', 'e', 'et'}
('IJ', 'IC') : {'=', 'st', 'ot', 'dt', 'e', 'et'}
('ID', 'IP') : {'m', '<'}
('IP', 'ID') : {'>', 'mt'}
('IJ', 'IP') : {'o', 'm', '<', 'dt', 'et'}
('IP', 'IJ') : {'d', 'ot', 'e', '>', 'mt'}
('IC', 'ID') : {'d', 'e', '=', 's'}
('ID', 'IC') : {'dt', '=', 'et', 'st'}
('IC', 'IP') : {'m', '<'}
('IP', 'IC') : {'>', 'mt'}
"""