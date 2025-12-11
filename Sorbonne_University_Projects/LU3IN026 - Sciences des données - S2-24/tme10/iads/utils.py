# -*- coding: utf-8 -*-

"""
Package: iads
File: utils.py
Année: LU3IN026 - semestre 2 - 2024-2025, Sorbonne Université
"""

# ------------------------ 
# Fonctions utiles
# Version de départ : Février 2025

# import externe
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------ 
# genere_dataset_uniform:
def genere_dataset_uniform(d, nc, binf=-1, bsup=1):
    """ int * int * float^2 -> tuple[ndarray, ndarray]
        Hyp: n est pair
        d: nombre de dimensions de la description
        nc: nombre d'exemples de chaque classe
        les valeurs générées uniformément sont dans [binf,bsup]
    """
    X = np.random.uniform(binf, bsup, size=(2 * nc, d))
    Y = np.array([-1] * nc + [+1] * nc)

    return X,Y

# genere_dataset_gaussian:
def genere_dataset_gaussian(positive_center, positive_sigma, negative_center, negative_sigma, nc):
    """ les valeurs générées suivent une loi normale
        rend un tuple (data_desc, data_labels)
    """

    negative_data = np.random.multivariate_normal(negative_center, negative_sigma, nc)
    positive_data = np.random.multivariate_normal(positive_center, positive_sigma, nc) 
    data_desc = np.vstack((negative_data, positive_data))
    data_labels = np.array([-1] * nc + [1] * nc)
    
    return data_desc, data_labels


# plot2DSet:
def plot2DSet(desc,labels,nom_dataset= "Dataset", avec_grid=False):    
    """ ndarray * ndarray * str * bool-> affichage
        nom_dataset (str): nom du dataset pour la légende
        avec_grid (bool) : True si on veut afficher la grille
        la fonction doit utiliser la couleur 'red' pour la classe -1 et 'blue' pour la +1
    """

    data2_positifs = desc[labels == +1]
    data2_negatifs = desc[labels == -1]

    # Tracé de l'ensemble des exemples :
    plt.scatter(data2_negatifs[:,0],data2_negatifs[:,1],marker='o', color="red", label='classe -1') # 'o' rouge pour la classe -1
    plt.scatter(data2_positifs[:,0],data2_positifs[:,1],marker='x', color="blue", label='classe +1') # 'x' bleu pour la classe +1

    # Informations d'affichage :
    plt.title(nom_dataset)
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.legend()
    if avec_grid:
        plt.grid(True, linestyle='--', alpha=0.6)

    # Visualisation du résultat
    plt.show()

# plot_frontiere:
def plot_frontiere(desc_set, label_set, classifier, step=30):
    """ desc_set * label_set * Classifier * int -> NoneType
        Remarque: le 4e argument est optionnel et donne la "résolution" du tracé: plus il est important
        et plus le tracé de la frontière sera précis.        
        Cette fonction affiche la frontière de décision associée au classifieur
    """
    mmax=desc_set.max(0)
    mmin=desc_set.min(0)
    x1grid,x2grid=np.meshgrid(np.linspace(mmin[0],mmax[0],step),np.linspace(mmin[1],mmax[1],step))
    grid=np.hstack((x1grid.reshape(x1grid.size,1),x2grid.reshape(x2grid.size,1)))
    
    # calcul de la prediction pour chaque point de la grille
    res=np.array([classifier.predict(grid[i,:]) for i in range(len(grid)) ])
    res=res.reshape(x1grid.shape)
    # tracer des frontieres
    # colors[0] est la couleur des -1 et colors[1] est la couleur des +1
    plt.contourf(x1grid,x2grid,res,colors=["darksalmon","skyblue"],levels=[-1000,0,1000])

def create_XOR(n, var):
    """ int * float -> tuple[ndarray, ndarray]
        Hyp: n et var sont positifs
        n: nombre de points voulus
        var: variance sur chaque dimension
    """
    assert n % 4 == 0, "n doit être un multiple de 4 pour garantir un nombre égal de points par classe."
    
    centers = np.array([[0, 0], [1, 1], [1, 0], [0, 1]])  
    sigma_matrix = np.array([[var, 0], [0, var]])  
    
    data_desc_list = []
    data_labels_list = []
    
    for i in range(4):
        desc = np.random.multivariate_normal(centers[i], sigma_matrix, n)
        
        if i == 2 or i == 3:
            lab = np.ones(n)
        else:
            lab = -np.ones(n)
        
        data_desc_list.append(desc)
        data_labels_list.append(lab)
    
    data_desc = np.vstack(data_desc_list)
    data_labels = np.concatenate(data_labels_list)
    
    return data_desc, data_labels
# ------------------------ 