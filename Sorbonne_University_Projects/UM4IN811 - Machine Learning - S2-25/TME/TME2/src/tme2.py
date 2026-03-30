# Yuxiang ZHANG & Kenan Alsafadi

import numpy as np
import matplotlib.pyplot as plt

from mltools import plot_data, plot_frontiere, make_grid, gen_arti

def mse(w, x, y):
    """
    Fonction de coût des moindres carrés (Mean Squared Error)
    
    Paramètres:
    w : vecteur de poids de dimension (d, 1)
    x : matrice des données d'entrée de dimension (n, d)
    y : vecteur des labels de dimension (n, 1)
    
    Retourne:
    Matrice de dimension (n, 1) contenant le coût pour chaque exemple
    """
    # Réorganisation des dimensions pour assurer la cohérence
    w = w.reshape(-1, 1)
    y = y.reshape(-1, 1)
    
    # Calcul des prédictions : X * w
    predictions = x.dot(w)
    
    # Calcul de l'erreur quadratique : (y_pred - y)^2
    cout = (predictions - y) ** 2
    
    return cout

def mse_grad(w, x, y):
    """
    Gradient de la fonction de coût des moindres carrés
    
    Paramètres:
    w : vecteur de poids de dimension (d, 1)
    x : matrice des données d'entrée de dimension (n, d)
    y : vecteur des labels de dimension (n, 1)
    
    Retourne:
    Matrice de dimension (n, d) contenant le gradient pour chaque exemple
    """
    # Réorganisation des dimensions pour assurer la cohérence
    w = w.reshape(-1, 1)
    y = y.reshape(-1, 1)
    
    # Calcul des prédictions : X * w
    predictions = x.dot(w)
    
    # Calcul du gradient : 2 * (X * w - y) * X
    # Pour chaque exemple i : grad_i = 2 * (w^T x_i - y_i) * x_i
    gradient = 2 * (predictions - y) * x
    
    return gradient

def reglog(w, x, y):
    """
    Fonction de coût de la régression logistique
    
    Paramètres:
    w : vecteur de poids de dimension (d, 1)
    x : matrice des données d'entrée de dimension (n, d)
    y : vecteur des labels de dimension (n, 1) avec valeurs dans {-1, 1}
    
    Retourne:
    Matrice de dimension (n, 1) contenant le coût pour chaque exemple
    Formule : log(1 + exp(-y * w^T * x))
    """
    # Réorganisation des dimensions pour assurer la cohérence
    w = w.reshape(-1, 1)
    y = y.reshape(-1, 1)
    
    # Calcul du terme linéaire : y * w^T * x
    terme_lineaire = y * x.dot(w)
    
    # Calcul du coût logistique : log(1 + exp(-y * w^T * x))
    # Utilisation de np.maximum pour éviter les débordements numériques
    cout = np.log(1 + np.exp(-np.maximum(-100, terme_lineaire)))
    
    return cout

def reglog_grad(w, x, y):
    """
    Gradient de la fonction de coût de la régression logistique
    
    Paramètres:
    w : vecteur de poids de dimension (d, 1)
    x : matrice des données d'entrée de dimension (n, d)
    y : vecteur des labels de dimension (n, 1) avec valeurs dans {-1, 1}
    
    Retourne:
    Matrice de dimension (n, d) contenant le gradient pour chaque exemple
    Formule : -y * σ(-y * w^T * x) * x
    où σ est la fonction sigmoïde
    """
    # Réorganisation des dimensions pour assurer la cohérence
    w = w.reshape(-1, 1)
    y = y.reshape(-1, 1)
    
    # Calcul du terme linéaire : y * w^T * x
    terme_lineaire = y * x.dot(w)
    
    # Calcul de σ(-y * w^T * x) = 1 / (1 + exp(y * w^T * x))
    # Limitation de l'exponentielle pour éviter les débordements
    terme_exp = np.exp(np.minimum(100, terme_lineaire))
    terme_sigmoid = 1 / (1 + terme_exp)
    
    # Calcul du gradient : -y * σ(-y * w^T * x) * x
    gradient = -y * terme_sigmoid * x
    
    return gradient

def grad_check(f, f_grad, N=100, d=2):
    """
    Vérification de l'exactitude du calcul du gradient par différence finie
    
    Paramètres:
    f : fonction de coût à tester
    f_grad : fonction de gradient à tester
    N : nombre de points de test
    d : dimension des données
    
    Principe:
    Compare le gradient analytique avec une approximation numérique
    basée sur le développement limité d'ordre 1
    """
    np.random.seed(42)
    erreurs = []
    
    for _ in range(N):
        # Génération aléatoire de données
        x = np.random.randn(10, d)
        y = np.random.choice([-1, 1], size=(10, 1))
        w = np.random.randn(d, 1)
        
        # Calcul du gradient par différence finie
        epsilon = 1e-7
        gradient_numerique = np.zeros_like(w)
        
        for i in range(len(w)):
            w_plus = w.copy()
            w_moins = w.copy()
            w_plus[i] += epsilon
            w_moins[i] -= epsilon
            
            f_plus = f(w_plus, x, y).mean()
            f_moins = f(w_moins, x, y).mean()
            
            # Différence centrée : [f(x+ε) - f(x-ε)] / (2ε)
            gradient_numerique[i] = (f_plus - f_moins) / (2 * epsilon)
        
        # Calcul du gradient analytique
        gradient_analytique = f_grad(w, x, y).mean(axis=0).reshape(-1, 1)
        
        # Calcul de l'erreur relative
        numerateur = np.linalg.norm(gradient_numerique - gradient_analytique)
        denominateur = np.linalg.norm(gradient_numerique) + np.linalg.norm(gradient_analytique)
        
        if denominateur < 1e-10:
            erreur = 0
        else:
            erreur = numerateur / denominateur
        
        erreurs.append(erreur)
    
    erreur_moyenne = np.mean(erreurs)
    print(f"Erreur moyenne de vérification du gradient : {erreur_moyenne:.6f}")
    
    if erreur_moyenne < 1e-4:
        print("Le gradient est correctement implémenté !")
    else:
        print("Attention : le gradient pourrait être mal implémenté !")
    
    return erreur_moyenne

def descente_gradient(datax, datay, f_loss, f_grad, eps, iter):
    """
    Algorithme de descente de gradient
    
    Paramètres:
    datax : matrice des données d'entrée de dimension (n, d)
    datay : vecteur des labels de dimension (n, 1)
    f_loss : fonction de coût à minimiser
    f_grad : fonction calculant le gradient de f_loss
    eps : pas d'apprentissage (learning rate)
    iter : nombre d'itérations
    
    Retourne:
    w_opt : paramètres optimaux trouvés
    liste_w : historique des paramètres à chaque itération
    liste_loss : historique des valeurs de la fonction de coût
    """
    n, d = datax.shape
    
    # Initialisation aléatoire des poids
    w = np.random.randn(d, 1) * 0.1
    
    # Stockage de l'historique
    liste_w = [w.copy()]
    liste_loss = [f_loss(w, datax, datay).mean()]
    
    for i in range(iter):
        # Calcul du gradient (moyenne sur tous les exemples)
        gradient = f_grad(w, datax, datay).mean(axis=0).reshape(-1, 1)
        
        # Mise à jour des poids : w = w - ε * ∇f(w)
        w = w - eps * gradient
        
        # Sauvegarde des valeurs courantes
        liste_w.append(w.copy())
        perte_courante = f_loss(w, datax, datay).mean()
        liste_loss.append(perte_courante)
        
        # Affichage périodique de la progression
        if i % 100 == 0:
            print(f"Itération {i}: perte = {perte_courante:.6f}")
    
    w_opt = w
    
    return w_opt, liste_w, liste_loss

def check_fonctions():
    """
    Vérification des fonctions implémentées avec des valeurs de référence
    """
    # Fixation de la seed pour la reproductibilité
    np.random.seed(0)
    datax, datay = gen_arti(epsilon=0.1)
    wrandom = np.random.randn(datax.shape[1], 1)
    
    # Vérification de la MSE
    valeur_mse = mse(wrandom, datax, datay).mean()
    print(f"MSE : {valeur_mse:.5f}")
    assert np.isclose(valeur_mse, 0.54731, rtol=1e-4)
    
    # Vérification de la régression logistique
    valeur_reglog = reglog(wrandom, datax, datay).mean()
    print(f"Régression logistique : {valeur_reglog:.5f}")
    assert np.isclose(valeur_reglog, 0.57053, rtol=1e-4)
    
    # Vérification du gradient de la MSE
    valeur_mse_grad = mse_grad(wrandom, datax, datay).mean()
    print(f"Gradient MSE : {valeur_mse_grad:.5f}")
    assert np.isclose(valeur_mse_grad, -1.43120, rtol=1e-4)
    
    # Vérification du gradient de la régression logistique
    valeur_reglog_grad = reglog_grad(wrandom, datax, datay).mean()
    print(f"Gradient régression logistique : {valeur_reglog_grad:.5f}")
    assert np.isclose(valeur_reglog_grad, -0.42714, rtol=1e-4)
    
    print("Tous les tests sont passés avec succès !")
    np.random.seed()

def experimenter():
    """
    Fonction principale pour exécuter les expériences de descente de gradient
    """
    # Génération des données
    print("Génération des données...")
    datax, datay = gen_arti(nbex=1000, data_type=0, epsilon=0.1)
    
    # Vérification des gradients
    print("\nVérification des gradients :")
    print("Vérification du gradient de la MSE :")
    grad_check(mse, mse_grad)
    print("\nVérification du gradient de la régression logistique :")
    grad_check(reglog, reglog_grad)
    
    # Test de différents pas d'apprentissage
    pas_apprentissage = [0.01, 0.1, 0.5, 1.0]
    iterations = 500
    
    plt.figure(figsize=(15, 10))
    
    for i, eps in enumerate(pas_apprentissage):
        print(f"\n=== Régression MSE, pas d'apprentissage = {eps} ===")
        w_opt_mse, w_list_mse, loss_list_mse = descente_gradient(
            datax, datay, mse, mse_grad, eps, iterations
        )
        
        print(f"\n=== Régression logistique, pas d'apprentissage = {eps} ===")
        w_opt_log, w_list_log, loss_list_log = descente_gradient(
            datax, datay, reglog, reglog_grad, eps, iterations
        )
        
        # Visualisation de l'évolution de la perte
        plt.subplot(2, 2, i + 1)
        plt.plot(loss_list_mse, label=f'MSE (lr={eps})')
        plt.plot(loss_list_log, label=f'RégLog (lr={eps})')
        plt.xlabel('Itérations')
        plt.ylabel('Perte')
        plt.title(f'Pas d\'apprentissage = {eps}')
        plt.legend()
        plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('comparaison_pas_apprentissage.png')
    plt.show()
    
    # Visualisation des frontières de décision
    plt.figure(figsize=(12, 5))
    
    # Utilisation du meilleur pas d'apprentissage
    eps_optimal = 0.1
    w_opt_mse, _, _ = descente_gradient(datax, datay, mse, mse_grad, eps_optimal, 1000)
    w_opt_log, _, _ = descente_gradient(datax, datay, reglog, reglog_grad, eps_optimal, 1000)
    
    # Frontière de décision pour la MSE
    plt.subplot(1, 2, 1)
    plot_frontiere(datax, lambda x: np.sign(x.dot(w_opt_mse)), step=100)
    plot_data(datax, datay)
    plt.title('Frontière de décision - Régression MSE')
    
    # Frontière de décision pour la régression logistique
    plt.subplot(1, 2, 2)
    plot_frontiere(datax, lambda x: np.sign(x.dot(w_opt_log)), step=100)
    plot_data(datax, datay)
    plt.title('Frontière de décision - Régression logistique')
    
    plt.tight_layout()
    plt.savefig('frontieres_decision.png')
    plt.show()
    
    # Visualisation du paysage de perte et du chemin d'optimisation
    visualiser_paysage_perte(datax, datay, w_opt_log, w_list_log)
    
    # Expériences sur différents types de données
    experimenter_types_donnees()

def visualiser_paysage_perte(datax, datay, w_opt, w_list):
    """
    Visualisation du paysage de perte et du chemin suivi par l'optimisation
    
    Paramètres:
    datax : données d'entrée
    datay : labels
    w_opt : paramètres optimaux
    w_list : historique des paramètres pendant l'optimisation
    """
    # Création d'une grille pour l'évaluation
    grille, x_grille, y_grille = make_grid(xmin=-2, xmax=2, ymin=-2, ymax=2, step=50)
    
    # Calcul de la perte sur chaque point de la grille
    valeurs_perte = np.array([reglog(w.reshape(-1, 1), datax, datay).mean() 
                             for w in grille]).reshape(x_grille.shape)
    
    # Extraction du chemin d'optimisation
    chemin_x = [w[0] for w in w_list]
    chemin_y = [w[1] for w in w_list]
    
    plt.figure(figsize=(12, 5))
    
    # Visualisation en courbes de niveau
    plt.subplot(1, 2, 1)
    contour = plt.contourf(x_grille, y_grille, valeurs_perte, levels=50, cmap='viridis')
    plt.colorbar(contour)
    plt.plot(chemin_x, chemin_y, 'r-', linewidth=2, label='Chemin d\'optimisation')
    plt.scatter(chemin_x[0], chemin_y[0], c='yellow', s=100, label='Départ', zorder=5)
    plt.scatter(w_opt[0], w_opt[1], c='red', s=100, label='Optimum', zorder=5)
    plt.xlabel('w₁')
    plt.ylabel('w₂')
    plt.title('Paysage de perte avec chemin d\'optimisation')
    plt.legend()
    
    # Visualisation 3D
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.add_subplot(122, projection='3d')
    
    # Surface de perte
    ax.plot_surface(x_grille, y_grille, valeurs_perte, cmap='viridis', alpha=0.8)
    
    # Chemin d'optimisation en 3D
    perte_chemin = [reglog(w, datax, datay).mean() for w in w_list]
    ax.plot(chemin_x, chemin_y, perte_chemin, 'r-', linewidth=3, label='Chemin')
    ax.scatter(chemin_x[0], chemin_y[0], perte_chemin[0], c='yellow', s=100, label='Départ')
    ax.scatter(w_opt[0], w_opt[1], reglog(w_opt, datax, datay).mean(), 
               c='red', s=100, label='Optimum')
    
    ax.set_xlabel('w₁')
    ax.set_ylabel('w₂')
    ax.set_zlabel('Perte')
    ax.set_title('Paysage de perte 3D')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('paysage_perte.png')
    plt.show()

def experimenter_types_donnees():
    """
    Expérimentation sur différents types de données artificielles
    """
    types_donnees = [0, 1, 2]  # 2 gaussiennes, 4 gaussiennes, échiquier
    noms_donnees = ['2 Gaussiennes', '4 Gaussiennes', 'Échiquier']
    
    plt.figure(figsize=(15, 10))
    
    for idx, type_donnee in enumerate(types_donnees):
        print(f"\n=== Expérience sur : {noms_donnees[idx]} ===")
        
        # Génération des données
        datax, datay = gen_arti(nbex=1000, data_type=type_donnee, epsilon=0.1)
        
        # Entraînement des modèles
        eps = 0.1
        iterations = 1000
        
        # Régression MSE
        w_opt_mse, _, _ = descente_gradient(datax, datay, mse, mse_grad, eps, iterations)
        
        # Régression logistique
        w_opt_log, _, _ = descente_gradient(datax, datay, reglog, reglog_grad, eps, iterations)
        
        # Visualisation des résultats
        plt.subplot(3, 3, idx * 3 + 1)
        plot_data(datax, datay)
        plt.title(f'{noms_donnees[idx]} - Données')
        
        plt.subplot(3, 3, idx * 3 + 2)
        plot_frontiere(datax, lambda x: np.sign(x.dot(w_opt_mse)), step=100)
        plot_data(datax, datay)
        plt.title('Frontière MSE')
        
        plt.subplot(3, 3, idx * 3 + 3)
        plot_frontiere(datax, lambda x: np.sign(x.dot(w_opt_log)), step=100)
        plot_data(datax, datay)
        plt.title('Frontière Régression Logistique')
    
    plt.tight_layout()
    plt.savefig('different_types_donnees.png')
    plt.show()
    
    # Expérimentation avec différents niveaux de bruit
    print("\n=== Expérimentation avec différents niveaux de bruit ===")
    niveaux_bruit = [0.01, 0.1, 0.5, 1.0]
    
    for bruit in niveaux_bruit:
        print(f"\nNiveau de bruit : {bruit}")
        datax, datay = gen_arti(nbex=1000, data_type=0, epsilon=bruit)
        
        eps = 0.1
        iterations = 1000
        
        # Entraînement de la régression logistique
        w_opt_log, _, liste_perte = descente_gradient(
            datax, datay, reglog, reglog_grad, eps, iterations
        )
        
        # Calcul de la précision
        predictions = np.sign(datax.dot(w_opt_log))
        precision = np.mean(predictions == datay)
        print(f"Précision : {precision:.4f}")
        
        # Visualisation
        plt.figure(figsize=(6, 5))
        plot_frontiere(datax, lambda x: np.sign(x.dot(w_opt_log)), step=100)
        plot_data(datax, datay)
        plt.title(f'Bruit = {bruit}, Précision = {precision:.4f}')
        plt.show()

if __name__ == "__main__":
    # Vérification des fonctions implémentées
    check_fonctions()
    
    # Exécution des expériences
    experimenter()
    
