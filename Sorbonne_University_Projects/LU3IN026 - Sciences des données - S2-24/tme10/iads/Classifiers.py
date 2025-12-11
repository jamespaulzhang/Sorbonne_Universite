# -*- coding: utf-8 -*-

"""
Package: iads
File: Classifiers.py
Année: LU3IN026 - semestre 2 - 2024-2025, Sorbonne Université
"""

# Classfieurs implémentés en LU3IN026
# Version de départ : Février 2025

# Import de packages externes
import numpy as np
import pandas as pd
import copy
import math
import graphviz as gv

# ---------------------------
class Classifier:
    """ Classe (abstraite) pour représenter un classifieur
        Attention: cette classe est ne doit pas être instanciée.
    """

    def __init__(self, input_dimension):
        """ Constructeur de Classifier
            Argument:
                - input_dimension (int) : dimension de la description des exemples
            Hypothèse : input_dimension > 0
        """
        self.dimension = input_dimension

    def train(self, desc_set, label_set):
        """ Permet d'entrainer le modele sur l'ensemble donné
            desc_set: ndarray avec des descriptions
            label_set: ndarray avec les labels correspondants
            Hypothèse: desc_set et label_set ont le même nombre de lignes
        """        
        raise NotImplementedError("Please Implement this method")

    def score(self, x):
        """ rend le score de prédiction sur x (valeur réelle)
            x: une description
        """
        raise NotImplementedError("Please Implement this method")

    def predict(self, x):
        """ rend la prediction sur x (soit -1 ou soit +1)
            x: une description
        """
        raise NotImplementedError("Please Implement this method")

    def accuracy(self, desc_set, label_set):
        """ Permet de calculer la qualité du système sur un dataset donné
            desc_set: ndarray avec des descriptions
            label_set: ndarray avec les labels correspondants
            Hypothèse: desc_set et label_set ont le même nombre de lignes
        """
        predictions = np.array([self.predict(x) for x in desc_set])
        correct_predictions = np.sum(predictions == label_set)
        return correct_predictions / len(label_set)

class ClassifierKNN(Classifier):
    """ Classe pour représenter un classifieur par K plus proches voisins.
        Cette classe hérite de la classe Classifier
    """
    
    def __init__(self, input_dimension, k):
        """ Constructeur de Classifier
            Argument:
                - intput_dimension (int) : dimension d'entrée des exemples
                - k (int) : nombre de voisins à considérer
            Hypothèse : input_dimension > 0
        """
        Classifier.__init__(self,input_dimension)
        self.k = k
    
    def train(self, desc_set, label_set):
        """ Permet d'entrainer le modele sur l'ensemble donné
            desc_set: ndarray avec des descriptions
            label_set: ndarray avec les labels correspondants
            Hypothèse: desc_set et label_set ont le même nombre de lignes
        """
        self.desc_set = desc_set
        self.label_set = label_set
    
    def score(self, x):
        """ rend la proportion de +1 parmi les k ppv de x (valeur réelle)
            x: une description : un ndarray
        """
        distances = np.linalg.norm(self.desc_set - x, axis=1)
        k_nearest_indices = np.argsort(distances)[:self.k]
        k_nearest_labels = self.label_set[k_nearest_indices]
        p = np.mean(k_nearest_labels == +1)
        return p
    
    def predict(self, x):
        """ rend la prediction sur x (-1 ou +1)
            x: une description : un ndarray
        """
        return 1 if self.score(x) >= 0.5 else -1
    
class ClassifierLineaireRandom(Classifier):
    """ Classifieur linéaire avec un vecteur de poids aléatoire.
    """
    def __init__(self, input_dimension):
        """ Constructeur
            Argument:
                - input_dimension (int) : dimension de la description des exemples (>0)
        """
        super().__init__(input_dimension)
        self.w = np.random.rand(input_dimension) * 2 - 1  # Poids initiaux aléatoires entre -1 et 1

    def train(self, desc_set, label_set):
        """ Entraînement : ici, pas d'apprentissage réel, les poids sont fixés aléatoirement """
        pass  # Aucun ajustement des poids

    def score(self, x):
        """ Calcule le score de prédiction pour x
            x: un exemple (ndarray)
            Retourne une valeur réelle correspondant au produit scalaire avec les poids
        """
        return np.dot(self.w, x)

    def predict(self, x):
        """ Prédit la classe de x
            Retourne +1 si le score est positif, -1 sinon
        """
        return 1 if self.score(x) >= 0 else -1

class ClassifierPerceptron(Classifier):
    """ Perceptron de Rosenblatt
    """
    def __init__(self, input_dimension, learning_rate=0.01, init=True):
        """ Constructeur de Classifier
            Argument:
                - input_dimension (int) : dimension de la description des exemples (>0)
                - learning_rate (par défaut 0.01): epsilon
                - init est le mode d'initialisation de w: 
                    - si True (par défaut): initialisation à 0 de w,
                    - si False : initialisation par tirage aléatoire de valeurs petites
        """
        Classifier.__init__(self, input_dimension)
        self.learning_rate = learning_rate
        
        if init:
            self.w = np.zeros(input_dimension)
        else:
            self.w = (np.random.rand(input_dimension) * 2 - 1) * 0.001
        
        self.allw = [self.w.copy()]  # Stocker les poids initiaux

    def train_step(self, desc_set, label_set):
        """ Réalise une unique itération sur tous les exemples du dataset
            donné en prenant les exemples aléatoirement.
            Arguments:
                - desc_set: ndarray avec des descriptions
                - label_set: ndarray avec les labels correspondants
        """        
        indices = list(range(len(desc_set)))
        np.random.shuffle(indices)
        
        for i in indices:
            x_i = desc_set[i]
            y_i = label_set[i]
            y_pred = np.dot(self.w, x_i)
            y_pred_sign = np.sign(y_pred)
            
            if y_pred_sign != y_i:
                self.w += self.learning_rate * y_i * x_i
                self.allw.append(self.w.copy())  # Stocker les poids après chaque mise à jour

    def train(self, desc_set, label_set, nb_max=100, seuil=0.001):
        """ Apprentissage itératif du perceptron sur le dataset donné.
            Arguments:
                - desc_set: ndarray avec des descriptions
                - label_set: ndarray avec les labels correspondants
                - nb_max (par défaut: 100) : nombre d'itérations maximale
                - seuil (par défaut: 0.001) : seuil de convergence
            Retour: la fonction rend une liste
                - liste des valeurs de norme de différences
        """        
        differences = []
        
        for _ in range(nb_max):
            old_w = self.w.copy()
            self.train_step(desc_set, label_set)
                    
            diff = np.linalg.norm(self.w - old_w)
            differences.append(diff)
            
            if diff < seuil:  # Arrêt si convergence
                break
        
        return differences
    
    def score(self, x):
        """ Rend le score de prédiction sur x (valeur réelle)
            x: une description
        """
        return np.dot(self.w, x)
    
    def predict(self, x):
        """ Rend la prediction sur x (soit -1 ou soit +1)
            x: une description
        """
        return np.sign(self.score(x))
    
    def get_allw(self):
        """ Récupère l'historique des poids """
        return self.allw

class ClassifierPerceptronBiais(ClassifierPerceptron):
    """ Perceptron de Rosenblatt avec biais
        Variante du perceptron de base
    """
    def __init__(self, input_dimension, learning_rate=0.01, init=True):
        """ Constructeur de Classifier
            Argument:
                - input_dimension (int) : dimension de la description des exemples (>0)
                - learning_rate (par défaut 0.01): epsilon
                - init est le mode d'initialisation de w: 
                    - si True (par défaut): initialisation à 0 de w,
                    - si False : initialisation par tirage aléatoire de valeurs petites
        """
        # Appel du constructeur de la classe mère
        super().__init__(input_dimension, learning_rate, init)
        # Affichage pour information (décommentez pour la mise au point)
        # print("Init perceptron biais: w= ",self.w," learning rate= ",learning_rate)
        
    def train_step(self, desc_set, label_set):
        """ Réalise une unique itération sur tous les exemples du dataset
            donné en prenant les exemples aléatoirement.
            Arguments:
                - desc_set: ndarray avec des descriptions
                - label_set: ndarray avec les labels correspondants
        """  
        indices = list(range(len(desc_set)))
        np.random.shuffle(indices)
        
        for i in indices:
            x_i = desc_set[i]
            y_i = label_set[i]
            f_xi = np.dot(self.w, x_i)  # Score du perceptron
            
            if f_xi * y_i < 1:  # Critère modifié
                self.w += self.learning_rate * (y_i - f_xi) * x_i
                self.allw.append(self.w.copy())  # Stocker l'évolution des poids   
                
class ClassifierMultiOAA(Classifier):
    """ Classifieur multiclasses basé sur la stratégie One-vs-All avec gestion d'erreurs. """
    
    def __init__(self, cl_bin):
        """ Constructeur de ClassifierMultiOAA
            cl_bin : classifieur binaire utilisé pour chaque modèle binaire
        """
        self.cl_bin = cl_bin
        self.models = {}
        self.classes = None
        
    def train(self, desc_set, label_set):
        """ Entraînement du modèle One-vs-All """
        self.classes = np.unique(label_set)
        
        for c in self.classes:
            # Créer une version binaire des labels : +1 pour la classe c, -1 pour les autres
            labels_bin = np.where(label_set == c, 1, -1)
            
            # Créer une copie du classifieur binaire et l'entraîner
            cl_bin_copy = copy.deepcopy(self.cl_bin)
            cl_bin_copy.train(desc_set, labels_bin)  # Entraînement sur les données
            self.models[c] = cl_bin_copy  # Stocker le classifieur pour la classe c
        
    def score(self, x):
        """ Retourne le score de prédiction pour x (valeur réelle) """
        scores = {}
        for c, model in self.models.items():
            try:
                score = model.score(x)  # Tenter d'obtenir le score du modèle pour la classe c
                if score is None:  # Vérifier si le score est None
                    score = -np.inf  # Attribuer un score faible si score est None
            except Exception as e:  # Capturer toutes les erreurs possibles
                score = -np.inf  # Attribuer un score faible en cas d'erreur
            
            scores[c] = score  # Ajouter le score pour la classe c
            
        return scores
    
    def predict(self, x):
        """ Retourne la classe avec le score maximal """
        scores = self.score(x)  # Obtenir les scores pour chaque classe
        return max(scores, key=scores.get)  # Retourner la classe avec le score maximal

    def accuracy(self, X, y):
        """ Calcul de l'exactitude sur un ensemble de données X avec les labels y """
        predictions = np.array([self.predict(x) for x in X])
        correct_predictions = np.sum(predictions == y)
        return correct_predictions / len(y)

class NoeudCategoriel:
    """ Classe pour représenter des noeuds d'un arbre de décision
    """
    def __init__(self, num_att=-1, nom=''):
        """ Constructeur: il prend en argument
            - num_att (int) : le numéro de l'attribut auquel il se rapporte: de 0 à ...
              si le noeud se rapporte à la classe, le numéro est -1, on n'a pas besoin
              de le préciser
            - nom (str) : une chaîne de caractères donnant le nom de l'attribut si
              il est connu (sinon, on ne met rien et le nom sera donné de façon 
              générique: "att_Numéro")
        """
        self.attribut = num_att    # numéro de l'attribut
        if (nom == ''):            # son nom si connu
            self.nom_attribut = 'att_'+str(num_att)
        else:
            self.nom_attribut = nom 
        self.Les_fils = None       # aucun fils à la création, ils seront ajoutés
        self.classe   = None       # valeur de la classe si c'est une feuille
        
    def est_feuille(self):
        """ rend True si l'arbre est une feuille 
            c'est une feuille s'il n'a aucun fils
        """
        return self.Les_fils == None
    
    def ajoute_fils(self, valeur, Fils):
        """ valeur : valeur de l'attribut de ce noeud qui doit être associée à Fils
                     le type de cette valeur dépend de la base
            Fils (NoeudCategoriel) : un nouveau fils pour ce noeud
            Les fils sont stockés sous la forme d'un dictionnaire:
            Dictionnaire {valeur_attribut : NoeudCategoriel}
        """
        if self.Les_fils == None:
            self.Les_fils = dict()
        self.Les_fils[valeur] = Fils
        # Rem: attention, on ne fait aucun contrôle, la nouvelle association peut
        # écraser une association existante.
    
    def ajoute_feuille(self,classe):
        """ classe: valeur de la classe
            Ce noeud devient un noeud feuille
        """
        self.classe    = classe
        self.Les_fils  = None   # normalement, pas obligatoire ici, c'est pour être sûr
        
    def classifie(self, exemple):
        """ exemple : numpy.array
            rend la classe de l'exemple 
            on rend la valeur None si l'exemple ne peut pas être classé (cf. les questions
            posées en fin de ce notebook)
        """
        if self.est_feuille():
            return self.classe
        if exemple[self.attribut] in self.Les_fils:
            # descente récursive dans le noeud associé à la valeur de l'attribut
            # pour cet exemple:
            return self.Les_fils[exemple[self.attribut]].classifie(exemple)
        else:
            # Cas particulier : on ne trouve pas la valeur de l'exemple dans la liste des
            # fils du noeud... Voir la fin de ce notebook pour essayer de résoudre ce mystère...
            print('\t*** Warning: attribut ',self.nom_attribut,' -> Valeur inconnue: ',exemple[self.attribut])
            return None
    
    def compte_feuilles(self):
        """ rend le nombre de feuilles sous ce noeud
        """
        if self.est_feuille():
            return 1
        total = 0
        for noeud in self.Les_fils:
            total += self.Les_fils[noeud].compte_feuilles()
        return total
     
    def to_graph(self, g, prefixe='A'):
        """ construit une représentation de l'arbre pour pouvoir l'afficher graphiquement
            Cette fonction ne nous intéressera pas plus que ça, elle ne sera donc pas expliquée            
        """
        if self.est_feuille():
            g.node(prefixe,str(self.classe),shape='box')
        else:
            g.node(prefixe, self.nom_attribut)
            i =0
            for (valeur, sous_arbre) in self.Les_fils.items():
                sous_arbre.to_graph(g,prefixe+str(i))
                g.edge(prefixe,prefixe+str(i), valeur)
                i = i+1        
        return g

def construit_AD(X, Y, epsilon, LNoms=[]):
    """ 
    X,Y : dataset
    epsilon : seuil d'entropie pour le critère d'arrêt 
    LNoms : liste des noms de features (colonnes) de description 
    """
    
    entropie_ens = entropie(Y)
    if entropie_ens <= epsilon:
        # ARRET : on crée une feuille
        noeud = NoeudCategoriel(-1, "Label")
        noeud.ajoute_feuille(classe_majoritaire(Y))
        return noeud

    # Initialisation pour trouver le meilleur attribut
    min_entropie = float('inf')
    i_best = -1
    Xbest_valeurs = None
    
    # Parcours de tous les attributs
    for i in range(X.shape[1]):
        valeurs = np.unique(X[:, i])  # Valeurs distinctes de l'attribut
        entropie_cond = 0.0
        
        for v in valeurs:
            Y_v = Y[X[:, i] == v]
            if len(Y_v) > 0:
                p = len(Y_v) / len(Y)
                entropie_cond += p * entropie(Y_v)
        
        # Mise à jour du meilleur attribut
        if entropie_cond < min_entropie:
            min_entropie = entropie_cond
            i_best = i
            Xbest_valeurs = valeurs
    
    # Si aucun attribut n'apporte un gain d'information
    if i_best == -1:
        noeud = NoeudCategoriel(-1, "Label")
        noeud.ajoute_feuille(classe_majoritaire(Y))
        return noeud
    
    # Création du noeud avec le meilleur attribut
    nom_attribut = LNoms[i_best] if LNoms else ''
    noeud = NoeudCategoriel(i_best, nom_attribut)
    
    # Vérification que Xbest_valeurs n'est pas vide
    if Xbest_valeurs is None:
        return noeud
    
    # Ajout des fils pour chaque valeur de l'attribut
    for v in Xbest_valeurs:
        X_v = X[X[:, i_best] == v, :]  # Assurer que X_v reste en 2D
        Y_v = Y[X[:, i_best] == v]

        # Vérifier que l'ensemble n'est pas vide avant l'appel récursif
        if len(Y_v) > 0:
            noeud.ajoute_fils(v, construit_AD(X_v, Y_v, epsilon, LNoms))

    return noeud

class ClassifierArbreDecision(Classifier):
    """ Classe pour représenter un classifieur par arbre de décision
    """
    
    def __init__(self, input_dimension, epsilon, LNoms=[]):
        """ Constructeur
            Argument:
                - intput_dimension (int) : dimension de la description des exemples
                - epsilon (float) : paramètre de l'algorithme (cf. explications précédentes)
                - LNoms : Liste des noms de dimensions (si connues)
            Hypothèse : input_dimension > 0
        """
        Classifier.__init__(self,input_dimension)  # Appel du constructeur de la classe mère
        self.epsilon = epsilon
        self.LNoms = LNoms
        # l'arbre est manipulé par sa racine qui sera un Noeud
        self.racine = None
        
    def toString(self):
        """  -> str
            rend le nom du classifieur avec ses paramètres
        """
        return 'ClassifierArbreDecision ['+str(self.dimension) + '] eps='+str(self.epsilon)
        
    def train(self, desc_set, label_set):
        """ Permet d'entrainer le modele sur l'ensemble donné
            desc_set: ndarray avec des descriptions
            label_set: ndarray avec les labels correspondants
            Hypothèse: desc_set et label_set ont le même nombre de lignes
        """        
        self.racine = construit_AD(desc_set, label_set, self.epsilon, self.LNoms)
    
    def score(self, x):
        """ rend le score de prédiction sur x (valeur réelle)
            x: une description
        """
        # cette méthode ne fait rien dans notre implémentation :
        pass
    
    def predict(self, x):
        """ x (array): une description d'exemple
            rend la prediction sur x             
        """
        if self.racine is None:
            raise ValueError("L'arbre n'a pas été entraîné")
        return self.racine.classifie(x)

    def number_leaves(self):
        """ rend le nombre de feuilles de l'arbre
        """
        return self.racine.compte_feuilles()
    
    def draw(self, GTree):
        """ affichage de l'arbre sous forme graphique
            Cette fonction modifie GTree par effet de bord
        """
        if self.racine:
            self.racine.to_graph(GTree)

def classe_majoritaire(Y):
    """ Y : (array) : array de labels
        rend la classe majoritaire ()
    """
    valeurs, nb_fois = np.unique(Y, return_counts=True)
    index_max = np.argmax(nb_fois)
    return valeurs[index_max]

def shannon(P):
    """ list[Number] -> float
        Hypothèse: P est une distribution de probabilités
        - P: distribution de probabilités
        rend la valeur de l'entropie de Shannon correspondante
    """
    k = len(P)  # base du logarithme
    
    # Cas particulier : k = 1 (entropie nulle)
    if k == 1:
        return 0.0
    
    entropy = 0.0
    
    for p in P:
        if p > 0:  # ignorer si p = 0 (terme = 0)
            entropy += p * math.log(p, k)  # log en base k
    
    return -entropy
    
def entropie(Y):
    """ Y : (array) : ensemble de labels de classe
        rend l'entropie de l'ensemble Y
    """
    # Calcul des fréquences de chaque classe
    valeurs, counts = np.unique(Y, return_counts=True)
    total = len(Y)
    P = counts / total  # Distribution de probabilité
    
    return shannon(P)

class NoeudNumerique:
    """ Classe pour représenter des noeuds numériques d'un arbre de décision
    """
    def __init__(self, num_att=-1, nom=''):
        """ Constructeur: il prend en argument
            - num_att (int) : le numéro de l'attribut auquel il se rapporte: de 0 à ...
              si le noeud se rapporte à la classe, le numéro est -1, on n'a pas besoin
              de le préciser
            - nom (str) : une chaîne de caractères donnant le nom de l'attribut si
              il est connu (sinon, on ne met rien et le nom sera donné de façon 
              générique: "att_Numéro")
        """
        self.attribut = num_att    # numéro de l'attribut
        if (nom == ''):            # son nom si connu
            self.nom_attribut = 'att_'+str(num_att)
        else:
            self.nom_attribut = nom 
        self.seuil = None          # seuil de coupure pour ce noeud
        self.Les_fils = None       # aucun fils à la création, ils seront ajoutés
        self.classe   = None       # valeur de la classe si c'est une feuille
        
    def est_feuille(self):
        """ rend True si l'arbre est une feuille 
            c'est une feuille s'il n'a aucun fils
        """
        return self.Les_fils == None
    
    def ajoute_fils(self, val_seuil, fils_inf, fils_sup):
        """ val_seuil : valeur du seuil de coupure
            fils_inf : fils à atteindre pour les valeurs inférieures ou égales à seuil
            fils_sup : fils à atteindre pour les valeurs supérieures à seuil
        """
        if self.Les_fils == None:
            self.Les_fils = dict()            
        self.seuil = val_seuil
        self.Les_fils['inf'] = fils_inf
        self.Les_fils['sup'] = fils_sup        
    
    def ajoute_feuille(self,classe):
        """ classe: valeur de la classe
            Ce noeud devient un noeud feuille
        """
        self.classe    = classe
        self.Les_fils  = None   # normalement, pas obligatoire ici, c'est pour être sûr
        
    def classifie(self, exemple):
        """ exemple : numpy.array
            rend la classe de l'exemple (pour nous, soit +1, soit -1 en général)
            on rend la valeur 0 si l'exemple ne peut pas être classé (cf. les questions
            posées en fin de ce notebook)
        """
        if self.est_feuille():
            return self.classe
        valeur = exemple[self.attribut]
        if valeur <= self.seuil:
            return self.Les_fils['inf'].classifie(exemple)
        else:
            return self.Les_fils['sup'].classifie(exemple)

    
    def compte_feuilles(self):
        """ rend le nombre de feuilles sous ce noeud
        """
        if self.est_feuille():
            return 1
        return self.Les_fils['inf'].compte_feuilles() + self.Les_fils['sup'].compte_feuilles()
     
    def to_graph(self, g, prefixe='A'):
        """ construit une représentation de l'arbre pour pouvoir l'afficher graphiquement
            Cette fonction ne nous intéressera pas plus que ça, elle ne sera donc 
            pas expliquée            
        """
        if self.est_feuille():
            g.node(prefixe,str(self.classe),shape='box')
        else:
            g.node(prefixe, str(self.nom_attribut))
            self.Les_fils['inf'].to_graph(g,prefixe+"g")
            self.Les_fils['sup'].to_graph(g,prefixe+"d")
            g.edge(prefixe,prefixe+"g", '<='+ str(self.seuil))
            g.edge(prefixe,prefixe+"d", '>'+ str(self.seuil))                
        return g
    
def discretise(m_desc, m_class, num_col):
    """ input:
            - m_desc : (np.array) matrice des descriptions toutes numériques
            - m_class : (np.array) matrice des classes (correspondant à m_desc)
            - num_col : (int) numéro de colonne de m_desc à considérer
            - nb_classes : (int) nombre initial de labels dans le dataset (défaut: 2)
        output: tuple : ((seuil_trouve, entropie), (liste_coupures,liste_entropies))
            -> seuil_trouve (float): meilleur seuil trouvé
            -> entropie (float): entropie du seuil trouvé (celle qui minimise)
            -> liste_coupures (List[float]): la liste des valeurs seuils qui ont été regardées
            -> liste_entropies (List[float]): la liste des entropies correspondantes aux seuils regardés
            (les 2 listes correspondent et sont donc de même taille)
            REMARQUE: dans le cas où il y a moins de 2 valeurs d'attribut dans m_desc, aucune discrétisation
            n'est possible, on rend donc ((None , +Inf), ([],[])) dans ce cas            
    """
    # Liste triée des valeurs différentes présentes dans m_desc:
    l_valeurs = np.unique(m_desc[:,num_col])
    
    # Si on a moins de 2 valeurs, pas la peine de discrétiser:
    if (len(l_valeurs) < 2):
        return ((None, float('Inf')), ([],[]))
    
    # Initialisation
    best_seuil = None
    best_entropie = float('Inf')
    
    # pour voir ce qui se passe, on va sauver les entropies trouvées et les points de coupures:
    liste_entropies = []
    liste_coupures = []
    
    nb_exemples = len(m_class)
    
    for v in l_valeurs:
        cl_inf = m_class[m_desc[:,num_col]<=v]
        cl_sup = m_class[m_desc[:,num_col]>v]
        nb_inf = len(cl_inf)
        nb_sup = len(cl_sup)
        
        # calcul de l'entropie de la coupure
        val_entropie_inf = entropie(cl_inf) # entropie de l'ensemble des inf
        val_entropie_sup = entropie(cl_sup) # entropie de l'ensemble des sup
        
        val_entropie = (nb_inf / float(nb_exemples)) * val_entropie_inf \
                       + (nb_sup / float(nb_exemples)) * val_entropie_sup
        
        # Ajout de la valeur trouvée pour retourner l'ensemble des entropies trouvées:
        liste_coupures.append(v)
        liste_entropies.append(val_entropie)
        
        # si cette coupure minimise l'entropie, on mémorise ce seuil et son entropie:
        if (best_entropie > val_entropie):
            best_entropie = val_entropie
            best_seuil = v
    
    return (best_seuil, best_entropie), (liste_coupures,liste_entropies)

def partitionne(m_desc,m_class,n,s):
    """ input:
            - m_desc : (np.array) matrice des descriptions toutes numériques
            - m_class : (np.array) matrice des classes (correspondant à m_desc)
            - n : (int) numéro de colonne de m_desc
            - s : (float) seuil pour le critère d'arrêt
        Hypothèse: m_desc peut être partitionné ! (il contient au moins 2 valeurs différentes)
        output: un tuple composé de 2 tuples
    """
    return ((m_desc[m_desc[:,n]<=s], m_class[m_desc[:,n]<=s]), \
            (m_desc[m_desc[:,n]>s], m_class[m_desc[:,n]>s]))
    
def construit_AD_num(X,Y,epsilon,LNoms = []):
    """ X,Y : dataset
        epsilon : seuil d'entropie pour le critère d'arrêt 
        LNoms : liste des noms de features (colonnes) de description 
    """
    
    # dimensions de X:
    (nb_lig, nb_col) = X.shape
    
    entropie_classe = entropie(Y)
    
    if (entropie_classe <= epsilon) or  (nb_lig <=1):
        # ARRET : on crée une feuille
        noeud = NoeudNumerique(-1,"Label")
        noeud.ajoute_feuille(classe_majoritaire(Y))
    else:
        gain_max = 0.0  # meilleur gain trouvé (initalisé à 0.0 => aucun gain)
        i_best = -1     # numéro du meilleur attribut (init à -1 (aucun))
        
        #############
        
        # COMPLETER CETTE PARTIE : ELLE DOIT PERMETTRE D'OBTENIR DANS
        # i_best : le numéro de l'attribut qui maximise le gain d'information.  En cas d'égalité,
        #          le premier rencontré est choisi.
        # gain_max : la plus grande valeur de gain d'information trouvée.
        # Xbest_tuple : le tuple rendu par partionne() pour le meilleur attribut trouvé
        # Xbest_seuil : le seuil de partitionnement associé au meilleur attribut
        #
        # Remarque : attention, la fonction discretise() peut renvoyer un tuple contenant
        # None (pas de partitionnement possible)n dans ce cas, on considèrera que le
        # résultat d'un partitionnement est alors ((X,Y),(None,None))
        
        Xbest_tuple = None
        Xbest_seuil = None
        
        for num_col in range(nb_col):
            (seuil, entropie), _ = discretise(X, Y, num_col)
            if seuil is None:
                continue
            gain = entropie_classe - entropie
            if gain > gain_max:
                gain_max = gain
                i_best = num_col
                Xbest_seuil = seuil
                Xbest_tuple = partitionne(X, Y, num_col, seuil)
        
        ############
        if (i_best != -1): # Un attribut qui amène un gain d'information >0 a été trouvé
            if len(LNoms)>0:  # si on a des noms de features
                noeud = NoeudNumerique(i_best,LNoms[i_best]) 
            else:
                noeud = NoeudNumerique(i_best)
            ((left_data,left_class), (right_data,right_class)) = Xbest_tuple
            noeud.ajoute_fils( Xbest_seuil, \
                              construit_AD_num(left_data,left_class, epsilon, LNoms), \
                              construit_AD_num(right_data,right_class, epsilon, LNoms) )
        else: # aucun attribut n'a pu améliorer le gain d'information
              # ARRET : on crée une feuille
            noeud = NoeudNumerique(-1,"Label")
            noeud.ajoute_feuille(classe_majoritaire(Y))
        
    return noeud

class ClassifierArbreNumerique(Classifier):
    """ Classe pour représenter un classifieur par arbre de décision numérique
    """
    
    def __init__(self, input_dimension, epsilon, LNoms=[]):
        """ Constructeur
            Argument:
                - intput_dimension (int) : dimension de la description des exemples
                - epsilon (float) : paramètre de l'algorithme (cf. explications précédentes)
                - LNoms : Liste des noms de dimensions (si connues)
            Hypothèse : input_dimension > 0
        """
        self.dimension = input_dimension
        self.epsilon = epsilon
        self.LNoms = LNoms
        # l'arbre est manipulé par sa racine qui sera un Noeud
        self.racine = None
        
    def toString(self):
        """  -> str
            rend le nom du classifieur avec ses paramètres
        """
        return 'ClassifierArbreDecision ['+str(self.dimension) + '] eps='+str(self.epsilon)
        
    def train(self, desc_set, label_set):
        """ Permet d'entrainer le modele sur l'ensemble donné
            desc_set: ndarray avec des descriptions
            label_set: ndarray avec les labels correspondants
            Hypothèse: desc_set et label_set ont le même nombre de lignes
        """        
        self.racine = construit_AD_num(desc_set,label_set,self.epsilon,self.LNoms)
    
    def score(self,x):
        """ rend le score de prédiction sur x (valeur réelle)
            x: une description
        """
        # cette méthode ne fait rien dans notre implémentation :
        pass
    
    def predict(self, x):
        """ x (array): une description d'exemple
            rend la prediction sur x             
        """
        return self.racine.classifie(x)

    def accuracy(self, desc_set, label_set):  # Version propre à aux arbres
        """ Permet de calculer la qualité du système sur un dataset donné
            desc_set: ndarray avec des descriptions
            label_set: ndarray avec les labels correspondants
            Hypothèse: desc_set et label_set ont le même nombre de lignes
        """
        nb_ok=0
        for i in range(desc_set.shape[0]):
            if self.predict(desc_set[i,:]) == label_set[i]:
                nb_ok=nb_ok+1
        acc=nb_ok/(desc_set.shape[0] * 1.0)
        return acc

    def number_leaves(self):
        """ rend le nombre de feuilles de l'arbre
        """
        return self.racine.compte_feuilles()
    
    def affiche(self,GTree):
        """ affichage de l'arbre sous forme graphique
            Cette fonction modifie GTree par effet de bord
        """
        self.racine.to_graph(GTree)

class ClassifierArbre(Classifier):
    """ Classe pour représenter un classifieur par arbre de décision généralisé
        qui gère à la fois les variables numériques et catégorielles.
    """

    def __init__(self, input_dimension, epsilon, LNoms=[]):
        """ Constructeur
            Argument:
                - input_dimension (int) : dimension de la description des exemples
                - epsilon (float) : paramètre de l'algorithme (seuil d'entropie pour le critère d'arrêt)
                - LNoms : Liste des noms de dimensions (si connues)
            Hypothèse : input_dimension > 0
        """
        super().__init__(input_dimension)
        self.epsilon = epsilon
        self.LNoms = LNoms
        self.racine = None

    def toString(self):
        """ Rend le nom du classifieur avec ses paramètres """
        return f'ClassifierArbre [{self.dimension}] eps={self.epsilon}'

    def train(self, desc_set, label_set):
        """ Permet d'entraîner le modèle sur l'ensemble donné
            desc_set: ndarray avec des descriptions
            label_set: ndarray avec les labels correspondants
            Hypothèse: desc_set et label_set ont le même nombre de lignes
        """
        self.racine = self.construit_AD(desc_set, label_set, self.epsilon, self.LNoms)

    def score(self, x):
        """ Rend le score de prédiction sur x (valeur réelle)
            x: une description
        """
        pass

    def predict(self, x):
        """ x (array): une description d'exemple
            Rend la prédiction sur x
        """
        if self.racine is None:
            raise ValueError("L'arbre n'a pas été entraîné")
        return self.racine.classifie(x)

    def accuracy(self, desc_set, label_set):
        """ Permet de calculer la qualité du système sur un dataset donné
            desc_set: ndarray avec des descriptions
            label_set: ndarray avec les labels correspondants
            Hypothèse: desc_set et label_set ont le même nombre de lignes
        """
        nb_ok = 0
        for i in range(desc_set.shape[0]):
            if self.predict(desc_set[i, :]) == label_set[i]:
                nb_ok += 1
        acc = nb_ok / (desc_set.shape[0] * 1.0)
        return acc

    def number_leaves(self):
        """ Rend le nombre de feuilles de l'arbre """
        return self.racine.compte_feuilles()

    def affiche(self, GTree):
        """ Affichage de l'arbre sous forme graphique
            Cette fonction modifie GTree par effet de bord
        """
        if self.racine:
            self.racine.to_graph(GTree)

    def construit_AD(self, X, Y, epsilon, LNoms=[]):
        """ Construit l'arbre de décision en fonction du type des attributs
            X, Y : dataset
            epsilon : seuil d'entropie pour le critère d'arrêt
            LNoms : liste des noms de features (colonnes) de description
        """
        entropie_classe = entropie(Y)
        if entropie_classe <= epsilon or len(Y) <= 1:
            # ARRET : on crée une feuille
            noeud = NoeudCategoriel(-1, "Label")
            noeud.ajoute_feuille(classe_majoritaire(Y))
            return noeud

        # Initialisation pour trouver le meilleur attribut
        min_entropie = float('inf')
        i_best = -1
        Xbest_valeurs = None
        Xbest_seuil = None

        # Parcours de tous les attributs
        for i in range(X.shape[1]):
            if np.issubdtype(X[:, i].dtype, np.number):
                # Attribut numérique
                (seuil, entropie_cond), _ = discretise(X, Y, i)
                if seuil is None:
                    continue
                if entropie_cond < min_entropie:
                    min_entropie = entropie_cond
                    i_best = i
                    Xbest_seuil = seuil
            else:
                # Attribut catégoriel
                valeurs = np.unique(X[:, i])
                entropie_cond = 0.0
                for v in valeurs:
                    Y_v = Y[X[:, i] == v]
                    if len(Y_v) > 0:
                        p = len(Y_v) / len(Y)
                        entropie_cond += p * entropie(Y_v)
                if entropie_cond < min_entropie:
                    min_entropie = entropie_cond
                    i_best = i
                    Xbest_valeurs = valeurs

        # Si aucun attribut n'apporte un gain d'information
        if i_best == -1:
            noeud = NoeudCategoriel(-1, "Label")
            noeud.ajoute_feuille(classe_majoritaire(Y))
            return noeud

        # Création du noeud avec le meilleur attribut
        nom_attribut = LNoms[i_best] if LNoms else ''
        if Xbest_seuil is not None:
            # Attribut numérique
            noeud = NoeudNumerique(i_best, nom_attribut)
            (left_data, left_class), (right_data, right_class) = partitionne(X, Y, i_best, Xbest_seuil)
            noeud.ajoute_fils(Xbest_seuil, self.construit_AD(left_data, left_class, epsilon, LNoms),
                              self.construit_AD(right_data, right_class, epsilon, LNoms))
        else:
            # Attribut catégoriel
            noeud = NoeudCategoriel(i_best, nom_attribut)
            for v in Xbest_valeurs:
                X_v = X[X[:, i_best] == v, :]
                Y_v = Y[X[:, i_best] == v]
                if len(Y_v) > 0:
                    noeud.ajoute_fils(v, self.construit_AD(X_v, Y_v, epsilon, LNoms))

        return noeud
        
        
class ClassifierBaggingTree(Classifier):
    """ Classifier utilisant le bagging d'arbres de décision """
    
    def __init__(self, input_dimension, B, pourcentage_echantillon, epsilon, avecRemise):
        """ Initialisation avec epsilon avant avecRemise """
        super().__init__(input_dimension)
        self.B = B
        self.pourcentage_echantillon = pourcentage_echantillon
        self.epsilon = epsilon
        self.avecRemise = avecRemise
        self.arbres = []
    
    def train(self, desc_set, label_set):
        """ Entraînement du modèle en construisant B arbres de décision """
        n = len(desc_set)
        m = int(n * self.pourcentage_echantillon)
    
        for _ in range(self.B):
            # Créer un échantillon bootstrap
            echantillon_desc, echantillon_labels = echantillonLS((desc_set, label_set), m, self.avecRemise)
            
            # Vérifier que l'échantillon contient au moins 2 classes
            if len(np.unique(echantillon_labels)) < 2:
                print("Avertissement: Échantillon ne contient qu'une seule classe")
                continue
                
            # Créer et entraîner un arbre avec epsilon
            arbre = ClassifierArbre(self.dimension, self.epsilon, [])
            arbre.train(echantillon_desc, echantillon_labels)
            
            if arbre.racine is not None:
                self.arbres.append(arbre)
            else:
                print("Avertissement: Échec construction arbre - données peut-être non séparables")

    def predict(self, x):
        """ Prédiction basée sur le vote des arbres """
        votes = [arbre.predict(x) for arbre in self.arbres if arbre.racine is not None]
        if not votes:
            raise ValueError("Aucun arbre n'a été correctement entraîné.")
        return 1 if sum(votes) >= 0 else -1
    
    def score(self, x):
        """ Calcul du score de classification (valeur réelle) """
        votes = np.array([arbre.predict(x) for arbre in self.arbres])
        score = np.sum(votes)
        return score / self.B
# ------------------------ 
