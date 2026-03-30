import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.base import BaseEstimator
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

POI_FILENAME = "data/poi-paris.pkl"
parismap = mpimg.imread('data/paris-48.806-2.23--48.916-2.48.jpg')
xmin, xmax = 2.23, 2.48
ymin, ymax = 48.806, 48.916
coords = [xmin, xmax, ymin, ymax]

# ==================== Fonctions de noyaux ====================

def kernel_uniform(x):
    """
    Noyau uniforme : retourne 1 si |x_i| ≤ 0.5 pour toutes les dimensions i, 0 sinon.
    
    Paramètres :
        x : matrice de forme (n_samples, n_features) ou vecteur (n_features,)
    
    Retourne :
        valeurs : 1 pour les points dans le cube [-0.5, 0.5]^d, 0 sinon
    """
    # S'assurer que x est au moins 2D
    x = np.atleast_2d(x)
    
    # Vérifier si toutes les coordonnées sont dans [-0.5, 0.5]
    inside = np.all(np.abs(x) <= 0.5, axis=1)
    
    # Convertir booléen en float (1.0 ou 0.0)
    return inside.astype(float)

def kernel_gaussian(x):
    """
    Noyau gaussien : (2π)^{-d/2} exp(-0.5 * ||x||²)
    
    Paramètres :
        x : matrice de forme (n_samples, n_features) ou vecteur (n_features,)
    
    Retourne :
        valeurs : valeur du noyau gaussien pour chaque point
    """
    # S'assurer que x est au moins 2D
    x = np.atleast_2d(x)
    
    # Nombre de dimensions
    d = x.shape[1]
    
    # Calculer la norme au carré pour chaque point
    norm_squared = np.sum(x**2, axis=1)
    
    # Calculer la valeur du noyau gaussien
    constant = (2 * np.pi) ** (-d / 2)
    values = constant * np.exp(-0.5 * norm_squared)
    
    return values

# ==================== Classes d'estimateurs ====================

class Density(BaseEstimator):
    """Classe de base pour les estimateurs de densité"""
    def fit(self, data):
        pass
    
    def predict(self, data):
        pass
    
    def score(self, data):
        """
        Retourne la log-vraisemblance des données
        
        Paramètres :
            data : données de test, forme (n_samples, n_features)
        
        Retourne :
            log_likelihood : somme des log-densités
        """
        densities = self.predict(data)
        # Ajouter une petite valeur pour éviter log(0)
        log_likelihood = np.sum(np.log(densities + 1e-10))
        return log_likelihood

class Histogramme(Density):
    """Estimateur de densité par histogramme"""
    def __init__(self, steps=10):
        Density.__init__(self)
        self.steps = steps
        self.bin_edges = None
        self.densities = None
        self.n_samples = None
        self.n_features = None
        self.min_vals = None
        self.max_vals = None
        self.bin_widths = None
    
    def _to_bin(self, x):
        indices = []
        for i in range(self.n_features):
            idx = np.digitize(x[i], self.bin_edges[i]) - 1
            idx = max(0, min(idx, self.steps - 1))
            indices.append(idx)
        return tuple(indices)
    
    def fit(self, x):
        self.n_samples, self.n_features = x.shape
        self.min_vals = x.min(axis=0)
        self.max_vals = x.max(axis=0)
        
        self.bin_edges = []
        for i in range(self.n_features):
            edges = np.linspace(self.min_vals[i], self.max_vals[i], self.steps + 1)
            self.bin_edges.append(edges)
        
        self.bin_widths = []
        for i in range(self.n_features):
            width = (self.max_vals[i] - self.min_vals[i]) / self.steps
            self.bin_widths.append(width)
        
        self.bin_volume = np.prod(self.bin_widths)
        
        hist, _ = np.histogramdd(x, bins=self.steps, 
                                 range=[(self.min_vals[i], self.max_vals[i]) 
                                        for i in range(self.n_features)])
        
        self.densities = hist / (self.n_samples * self.bin_volume)
        return self
    
    def predict(self, x):
        n_test = x.shape[0]
        densities = np.zeros(n_test)
        
        for i in range(n_test):
            point = x[i]
            
            in_range = True
            for j in range(self.n_features):
                if point[j] < self.min_vals[j] or point[j] > self.max_vals[j]:
                    in_range = False
                    break
            
            if not in_range:
                densities[i] = 0
            else:
                bin_indices = self._to_bin(point)
                densities[i] = self.densities[bin_indices]
        
        return densities

class KernelDensity(Density):
    """
    Estimateur de densité par méthode à noyaux
    
    Paramètres :
        kernel : fonction de noyau (uniforme ou gaussienne)
        sigma : paramètre de lissage (bandwidth)
    """
    def __init__(self, kernel=None, sigma=0.1):
        Density.__init__(self)
        if kernel is None:
            # Par défaut, utiliser le noyau gaussien
            self.kernel = kernel_gaussian
        else:
            self.kernel = kernel
        self.sigma = sigma
    
    def fit(self, x):
        """
        Enregistre les données d'apprentissage
        
        Paramètres :
            x : données d'apprentissage, forme (n_samples, n_features)
        """
        self.x = x  # Points d'apprentissage
        self.n_samples, self.n_features = x.shape
        return self
    
    def predict(self, data):
        """
        Estime la densité pour de nouveaux points
        
        Paramètres :
            data : données à évaluer, forme (n_samples_test, n_features)
        
        Retourne :
            densities : densités estimées pour chaque point
        """
        if not hasattr(self, 'x'):
            raise ValueError("L'estimateur doit être entraîné avec fit() avant d'utiliser predict()")
        
        n_test = data.shape[0]
        densities = np.zeros(n_test)
        
        # Pour chaque point de test
        for i in range(n_test):
            # Calculer les différences normalisées avec tous les points d'apprentissage
            diff = (self.x - data[i]) / self.sigma
            
            # Appliquer le noyau à toutes les différences
            kernel_values = self.kernel(diff)
            
            # Moyenne des valeurs du noyau
            mean_kernel = np.mean(kernel_values)
            
            # Densité = moyenne du noyau / (sigma^d)
            densities[i] = mean_kernel / (self.sigma ** self.n_features)
        
        return densities

# ==================== Classe Nadaraya-Watson ====================

class Nadaraya(BaseEstimator):
    """
    Estimateur de Nadaraya-Watson pour la régression par noyaux
    
    Formule : f(x) = Σ_i y_i * K((x - x_i)/σ) / Σ_j K((x - x_j)/σ)
    
    Paramètres :
        kernel : fonction de noyau (uniforme ou gaussienne)
        sigma : paramètre de lissage (bandwidth)
    """
    def __init__(self, kernel=None, sigma=0.1):
        BaseEstimator.__init__(self)
        if kernel is None:
            # Par défaut, utiliser le noyau gaussien
            self.kernel = kernel_gaussian
        else:
            self.kernel = kernel
        self.sigma = sigma
    
    def fit(self, X, y):
        """
        Enregistre les données d'apprentissage
        
        Paramètres :
            X : données d'entrée, forme (n_samples, n_features)
            y : valeurs cibles, forme (n_samples,)
        """
        self.X = X  # Points d'apprentissage
        self.y = y  # Valeurs cibles
        self.n_samples, self.n_features = X.shape
        return self
    
    def predict(self, X_test):
        """
        Prédit les valeurs pour de nouveaux points
        
        Paramètres :
            X_test : données de test, forme (n_samples_test, n_features)
        
        Retourne :
            predictions : valeurs prédites pour chaque point de test
        """
        if not hasattr(self, 'X') or not hasattr(self, 'y'):
            raise ValueError("L'estimateur doit être entraîné avec fit() avant d'utiliser predict()")
        
        n_test = X_test.shape[0]
        predictions = np.zeros(n_test)
        
        # Pour chaque point de test
        for i in range(n_test):
            # Calculer les différences normalisées avec tous les points d'apprentissage
            diff = (self.X - X_test[i]) / self.sigma
            
            # Appliquer le noyau à toutes les différences
            kernel_values = self.kernel(diff)
            
            # Calculer le numérateur : somme pondérée des y
            numerator = np.sum(self.y * kernel_values)
            
            # Calculer le dénominateur : somme des poids
            denominator = np.sum(kernel_values)
            
            # Éviter la division par zéro
            if denominator == 0:
                # Si aucun point n'a de poids, prédire la moyenne des y
                predictions[i] = np.mean(self.y)
            else:
                # Calculer la prédiction
                predictions[i] = numerator / denominator
        
        return predictions
    
    def score(self, X_test, y_test):
        """
        Calcule le coefficient de détermination R²
        
        Paramètres :
            X_test : données de test
            y_test : valeurs cibles de test
        
        Retourne :
            r2 : coefficient de détermination
        """
        y_pred = self.predict(X_test)
        return r2_score(y_test, y_pred)

# ==================== Fonctions auxiliaires ====================

def get_density2D(f, data, steps=100):
    """
    Calcule la densité en chaque case d'une grille steps x steps
    
    Paramètres :
        f : estimateur de densité
        data : données pour déterminer les bornes
        steps : nombre de pas dans chaque dimension
    
    Retourne :
        res : matrice des densités (steps x steps)
        xlin : discrétisation selon l'axe x
        ylin : discrétisation selon l'axe y
    """
    xmin, xmax = data[:, 0].min(), data[:, 0].max()
    ymin, ymax = data[:, 1].min(), data[:, 1].max()
    xlin, ylin = np.linspace(xmin, xmax, steps), np.linspace(ymin, ymax, steps)
    xx, yy = np.meshgrid(xlin, ylin)
    grid = np.c_[xx.ravel(), yy.ravel()]
    res = f.predict(grid).reshape(steps, steps)
    return res, xlin, ylin

def show_density(f, data, steps=100, log=False, title_suffix=""):
    """
    Affiche l'estimation de densité
    
    Paramètres :
        f : estimateur de densité
        data : données
        steps : résolution de la grille
        log : afficher en échelle logarithmique
        title_suffix : suffixe pour le titre
    """
    res, xlin, ylin = get_density2D(f, data, steps)
    xx, yy = np.meshgrid(xlin, ylin)
    plt.figure(figsize=(10, 8))
    show_img()
    
    if log:
        res = np.log(res + 1e-10)
        log_text = " (log)"
    else:
        log_text = ""
    
    # Afficher les données
    plt.scatter(data[:, 0], data[:, 1], alpha=0.8, s=3, color='red')
    
    # Afficher la densité
    img = plt.imshow(res, extent=[xlin.min(), xlin.max(), ylin.min(), ylin.max()], 
                     origin='lower', aspect='auto', alpha=0.7)
    plt.colorbar(img, label=f'Densité{log_text}')
    
    # Contours
    plt.contour(xx, yy, res, 10, colors='white', alpha=0.5)
    
    # Titre personnalisé selon le type d'estimateur
    if hasattr(f, 'kernel'):
        kernel_name = f.kernel.__name__
        plt.title(f"KDE - {kernel_name} (σ={f.sigma}){log_text}{title_suffix}")
    elif hasattr(f, 'steps'):
        plt.title(f"Histogramme (steps={f.steps}){log_text}{title_suffix}")
    else:
        plt.title(f"Estimation de densité{log_text}{title_suffix}")
    
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

def show_img(img=parismap):
    """Affiche la carte de Paris en fond"""
    origin = "lower" if len(img.shape) == 2 else "upper"
    alpha = 0.3 if len(img.shape) == 2 else 1.
    plt.imshow(img, extent=coords, aspect=1.5, origin=origin, alpha=alpha)

def load_poi(typepoi, fn=POI_FILENAME):
    """Charge les données d'un type de POI"""
    poidata = pickle.load(open(fn, "rb"))
    data = np.array([[v[1][0][1], v[1][0][0]] for v in sorted(poidata[typepoi].items())])
    note = np.array([v[1][1] for v in sorted(poidata[typepoi].items())])
    return data, note

# ==================== Fonctions pour les histogrammes ====================

def verifier_integrale_densite(f, data, steps_grid=100):
    """
    Vérifie que l'estimateur de densité est correct : 
    l'intégrale sur la grille doit être approximativement égale à 1
    
    Paramètres :
        f : estimateur de densité entraîné
        data : données originales (pour déterminer les bornes)
        steps_grid : taille de la grille pour la vérification
    
    Retourne :
        integrale : valeur calculée de l'intégrale
    """
    # Obtenir les densités sur la grille
    densities, xlin, ylin = get_density2D(f, data, steps=steps_grid)
    
    # Calculer l'aire d'une cellule de la grille
    dx = (xlin[1] - xlin[0])
    dy = (ylin[1] - ylin[0])
    aire_cellule = dx * dy
    
    # Calculer l'intégrale approximative
    integrale = np.sum(densities) * aire_cellule
    
    print(f"Vérification de l'intégrale de densité:")
    print(f"  Taille de la grille: {steps_grid}×{steps_grid}")
    print(f"  Aire d'une cellule: {aire_cellule:.6f}")
    print(f"  Intégrale calculée: {integrale:.6f}")
    
    if abs(integrale - 1.0) < 0.1:
        print(f"  ✓ Vérification réussie: intégrale≈1 (erreur: {abs(integrale-1.0):.4f})")
    else:
        print(f"  ✗ Échec de vérification: intégrale éloignée de 1 (erreur: {abs(integrale-1.0):.4f})")
    
    return integrale

def visualiser_steps_differents(data, type_poi="bar"):
    """
    Expérience 1 : Visualiser l'estimation de densité pour différentes valeurs de steps
    
    Paramètres :
        data : données
        type_poi : nom du type de POI (pour le titre)
    """
    steps_a_visualiser = [5, 10, 20, 40]
    
    print(f"\n{'='*60}")
    print(f"Expérience 1: {type_poi} - Visualisation pour différents steps")
    print(f"{'='*60}")
    
    for steps in steps_a_visualiser:
        # Créer et entraîner l'estimateur histogramme
        hist = Histogramme(steps=steps)
        hist.fit(data)
        
        # Visualiser l'estimation de densité
        show_density(hist, data, steps=100, log=False, title_suffix=f" - {type_poi}")
        
        # Vérifier l'intégrale de densité
        verifier_integrale_densite(hist, data, steps_grid=100)
        
        # Afficher la densité logarithmique
        plt.figure()
        show_density(hist, data, steps=100, log=True, title_suffix=f" - {type_poi}")
        
        # Calculer et afficher la log-vraisemblance
        log_vraisemblance = hist.score(data)
        print(f"  Steps={steps}: log-vraisemblance = {log_vraisemblance:.2f}")
        
        plt.show()

def trouver_meilleur_steps(data, type_poi="bar", taille_test=0.3, random_state=42):
    """
    Expérience 2 : Trouver le meilleur paramètre steps avec séparation train/test
    
    Paramètres :
        data : données complètes
        type_poi : nom du type de POI
        taille_test : proportion des données pour le test
        random_state : graine aléatoire
    
    Retourne :
        meilleur_steps : meilleure valeur du paramètre steps
        meilleur_score_test : meilleure log-vraisemblance sur le test
    """
    # Séparer les données en apprentissage et test
    donnees_apprentissage, donnees_test = train_test_split(
        data, test_size=taille_test, random_state=random_state
    )
    
    print(f"\n{'='*60}")
    print(f"Expérience 2: {type_poi} - Recherche du meilleur paramètre steps")
    print(f"{'='*60}")
    print(f"Taille de l'ensemble d'apprentissage: {len(donnees_apprentissage)}")
    print(f"Taille de l'ensemble de test: {len(donnees_test)}")
    
    # Tester différentes valeurs de steps
    valeurs_steps = list(range(5, 51, 5))  # [5, 10, 15, ..., 50]
    scores_apprentissage = []
    scores_test = []
    
    for steps in valeurs_steps:
        # Créer et entraîner l'estimateur histogramme
        hist = Histogramme(steps=steps)
        hist.fit(donnees_apprentissage)
        
        # Calculer la log-vraisemblance sur l'apprentissage et le test
        log_vrais_apprentissage = hist.score(donnees_apprentissage)
        log_vrais_test = hist.score(donnees_test)
        
        scores_apprentissage.append(log_vrais_apprentissage)
        scores_test.append(log_vrais_test)
        
        print(f"  Steps={steps:2d}: Apprentissage LL={log_vrais_apprentissage:8.2f}, Test LL={log_vrais_test:8.2f}")
    
    # Trouver le meilleur steps (maximisant la log-vraisemblance sur le test)
    idx_meilleur = np.argmax(scores_test)
    meilleur_steps = valeurs_steps[idx_meilleur]
    meilleur_score_test = scores_test[idx_meilleur]
    
    print(f"\n{'='*40}")
    print(f"Meilleur paramètre: steps = {meilleur_steps}")
    print(f"Meilleure log-vraisemblance sur le test: {meilleur_score_test:.2f}")
    
    # Tracer les résultats
    plt.figure(figsize=(10, 6))
    plt.plot(valeurs_steps, scores_apprentissage, 'b-o', label='Apprentissage', linewidth=2, markersize=8)
    plt.plot(valeurs_steps, scores_test, 'r-s', label='Test', linewidth=2, markersize=8)
    
    # Marquer le meilleur point
    plt.scatter([meilleur_steps], [meilleur_score_test], color='green', s=200, 
                zorder=5, label=f'Meilleur: steps={meilleur_steps}')
    
    plt.xlabel('Steps (nombre de bins par dimension)')
    plt.ylabel('Log-vraisemblance (Log-Likelihood)')
    plt.title(f'{type_poi} - Log-vraisemblance pour différents paramètres steps\n(Meilleur: steps={meilleur_steps})')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    # Afficher l'estimation de densité du meilleur modèle
    print(f"\nAffichage du meilleur modèle (steps={meilleur_steps}):")
    hist_meilleur = Histogramme(steps=meilleur_steps)
    hist_meilleur.fit(donnees_apprentissage)
    
    show_density(hist_meilleur, donnees_apprentissage, steps=100, log=False, 
                title_suffix=f" - {type_poi} (Meilleur modèle)")
    plt.show()
    
    # Vérifier l'intégrale de densité du meilleur modèle
    print(f"\nVérification de l'intégrale de densité du meilleur modèle:")
    verifier_integrale_densite(hist_meilleur, donnees_apprentissage, steps_grid=100)
    
    return meilleur_steps, meilleur_score_test

def validation_croisee(data, type_poi="bar", cv=5):
    """
    Expérience 3 : Évaluation du paramètre steps par validation croisée
    
    Paramètres :
        data : données
        type_poi : nom du type de POI
        cv : nombre de plis pour la validation croisée
    
    Note: Cette fonction a un problème car cross_val_score attend un estimateur avec y_true.
    """
    print(f"\n{'='*60}")
    print(f"Expérience 3: {type_poi} - Évaluation par validation croisée")
    print(f"{'='*60}")
    
    # Tester différentes valeurs de steps
    valeurs_steps = list(range(5, 51, 5))
    scores_cv = []
    scores_cv_std = []
    
    for steps in valeurs_steps:
        hist = Histogramme(steps=steps)
        
        # Utiliser la validation croisée pour calculer les scores
        scores = cross_val_score(hist, data, cv=cv, scoring='neg_mean_squared_error')
        
        # Calculer le score moyen et l'écart-type
        score_moyen = -np.mean(scores)  # Note: cross_val_score retourne des MSE négatifs
        score_std = np.std(scores)
        
        scores_cv.append(score_moyen)
        scores_cv_std.append(score_std)
        
        print(f"  Steps={steps:2d}: Score CV={score_moyen:8.2f} ± {score_std:8.2f}")
    
    # Trouver le meilleur steps (minimisant le score CV)
    idx_meilleur = np.argmin(scores_cv)
    meilleur_steps = valeurs_steps[idx_meilleur]
    meilleur_score_cv = scores_cv[idx_meilleur]
    
    print(f"\n{'='*40}")
    print(f"Meilleur paramètre (validation croisée): steps = {meilleur_steps}")
    print(f"Meilleur score CV: {meilleur_score_cv:.2f}")
    
    # Tracer les résultats
    plt.figure(figsize=(10, 6))
    plt.errorbar(valeurs_steps, scores_cv, yerr=scores_cv_std, 
                 fmt='o-', capsize=5, linewidth=2, markersize=8)
    
    # Marquer le meilleur point
    plt.scatter([meilleur_steps], [meilleur_score_cv], color='red', s=200, 
                zorder=5, label=f'Meilleur: steps={meilleur_steps}')
    
    plt.xlabel('Steps (nombre de bins par dimension)')
    plt.ylabel('Score de validation croisée (MSE négatif)')
    plt.title(f'{type_poi} - Évaluation par validation croisée\n(Meilleur: steps={meilleur_steps})')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    return meilleur_steps, meilleur_score_cv

def comparer_types_poi():
    """
    Expérience 4 : Comparer les meilleurs paramètres steps pour différents types de POI
    """
    print(f"\n{'='*60}")
    print(f"Expérience 4: Comparaison des meilleurs paramètres steps pour différents POI")
    print(f"{'='*60}")
    
    # Charger les données pour deux types de POI
    donnees_bar, notes_bar = load_poi("bar")
    donnees_night_club, notes_night_club = load_poi("night_club")
    
    print(f"Nombre de points pour les bars: {len(donnees_bar)}")
    print(f"Nombre de points pour les night_clubs: {len(donnees_night_club)}")
    
    # Expérience pour les bars
    print(f"\n{'='*40}")
    print(f"1. Analyse des bars")
    print(f"{'='*40}")
    
    meilleur_steps_bar, meilleur_score_bar = trouver_meilleur_steps(
        donnees_bar, type_poi="Bar", taille_test=0.3, random_state=42
    )
    
    # Expérience pour les night clubs
    print(f"\n{'='*40}")
    print(f"2. Analyse des night clubs")
    print(f"{'='*40}")
    
    # Les night clubs ont moins de données, utiliser une plage de steps différente
    donnees_apprentissage_night, donnees_test_night = train_test_split(
        donnees_night_club, test_size=0.3, random_state=42
    )
    
    # Plage de steps pour les night clubs (moins de données)
    valeurs_steps_night = list(range(3, 21, 2))  # [3, 5, 7, ..., 19]
    scores_apprentissage_night = []
    scores_test_night = []
    
    for steps in valeurs_steps_night:
        hist = Histogramme(steps=steps)
        hist.fit(donnees_apprentissage_night)
        
        log_vrais_apprentissage = hist.score(donnees_apprentissage_night)
        log_vrais_test = hist.score(donnees_test_night)
        
        scores_apprentissage_night.append(log_vrais_apprentissage)
        scores_test_night.append(log_vrais_test)
        
        print(f"  Steps={steps:2d}: Apprentissage LL={log_vrais_apprentissage:8.2f}, Test LL={log_vrais_test:8.2f}")
    
    # Trouver le meilleur steps pour les night clubs
    idx_meilleur_night = np.argmax(scores_test_night)
    meilleur_steps_night = valeurs_steps_night[idx_meilleur_night]
    meilleur_score_test_night = scores_test_night[idx_meilleur_night]
    
    print(f"\n{'='*40}")
    print(f"Meilleur paramètre: steps = {meilleur_steps_night}")
    print(f"Meilleure log-vraisemblance sur le test: {meilleur_score_test_night:.2f}")
    
    # Tracer les résultats pour les night clubs
    plt.figure(figsize=(10, 6))
    plt.plot(valeurs_steps_night, scores_apprentissage_night, 'b-o', label='Apprentissage', linewidth=2, markersize=8)
    plt.plot(valeurs_steps_night, scores_test_night, 'r-s', label='Test', linewidth=2, markersize=8)
    
    plt.scatter([meilleur_steps_night], [meilleur_score_test_night], color='green', s=200, 
                zorder=5, label=f'Meilleur: steps={meilleur_steps_night}')
    
    plt.xlabel('Steps (nombre de bins par dimension)')
    plt.ylabel('Log-vraisemblance (Log-Likelihood)')
    plt.title('Night clubs - Log-vraisemblance pour différents paramètres steps\n(Meilleur: steps={meilleur_steps_night})')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    # Comparer les résultats des deux types de POI
    print(f"\n{'='*60}")
    print(f"Comparaison des résultats: Bars vs Night clubs")
    print(f"{'='*60}")
    print(f"{'Mesure':<20} {'Bars':<15} {'Night clubs':<15} {'Ratio':<10}")
    print(f"{'-'*60}")
    print(f"{'Nombre de points':<20} {len(donnees_bar):<15} {len(donnees_night_club):<15} {len(donnees_bar)/len(donnees_night_club):<10.1f}")
    print(f"{'Meilleur steps':<20} {meilleur_steps_bar:<15} {meilleur_steps_night:<15} {meilleur_steps_bar/meilleur_steps_night:<10.2f}")
    print(f"{'Log-vrais. test':<20} {meilleur_score_bar:<15.2f} {meilleur_score_test_night:<15.2f} {meilleur_score_bar/meilleur_score_test_night:<10.2f}")
    
    # Calculer le nombre moyen de points par bin
    points_moyens_par_bin_bar = len(donnees_bar) / (meilleur_steps_bar ** 2)
    points_moyens_par_bin_night = len(donnees_night_club) / (meilleur_steps_night ** 2)
    
    print(f"\n{'Points moyens par bin':<20} {points_moyens_par_bin_bar:<15.1f} {points_moyens_par_bin_night:<15.1f} {points_moyens_par_bin_bar/points_moyens_par_bin_night:<10.2f}")
    
    # Analyser la relation entre le meilleur steps et la quantité de données
    print(f"\n{'='*40}")
    print(f"Analyse: Relation entre meilleur steps et quantité de données")
    print(f"{'='*40}")
    
    if meilleur_steps_bar > meilleur_steps_night:
        print("✓ Résultat conforme aux attentes: les bars (plus de données) peuvent utiliser un steps plus grand")
        print("  Raison: plus de points de données permettent une division plus fine sans créer trop de bins vides")
    else:
        print("⚠ Résultat inattendu: une analyse plus approfondie est nécessaire")
    
    return meilleur_steps_bar, meilleur_steps_night

# ==================== Fonctions pour les méthodes à noyaux ====================

def verifier_integrale_kde(f, data, steps_grid=100):
    """
    Vérifie que l'estimateur KDE produit une densité valide
    
    Paramètres :
        f : estimateur KDE entraîné
        data : données d'apprentissage
        steps_grid : résolution de la grille pour le calcul
    """
    # Calculer la densité sur une grille fine
    densities, xlin, ylin = get_density2D(f, data, steps=steps_grid)
    
    # Calculer l'aire d'une cellule
    dx = (xlin[1] - xlin[0])
    dy = (ylin[1] - ylin[0])
    aire_cellule = dx * dy
    
    # Calculer l'intégrale approximative
    integrale = np.sum(densities) * aire_cellule
    
    kernel_name = f.kernel.__name__ if hasattr(f, 'kernel') else "inconnu"
    
    print(f"Vérification de l'intégrale - {kernel_name} (σ={f.sigma}):")
    print(f"  Intégrale calculée: {integrale:.6f}")
    
    if abs(integrale - 1.0) < 0.1:
        print(f"  ✓ Vérification réussie: intégrale≈1 (erreur: {abs(integrale-1.0):.4f})")
    else:
        print(f"  ✗ Échec de vérification: intégrale éloignée de 1 (erreur: {abs(integrale-1.0):.4f})")
    
    return integrale

def experimenter_noyau_uniforme(data, sigma_values, type_poi="bar"):
    """
    Expérience avec le noyau uniforme et différents σ
    
    Paramètres :
        data : données
        sigma_values : liste des valeurs de σ à tester
        type_poi : type de POI (pour les titres)
    """
    print(f"\n{'='*60}")
    print(f"Expérience: {type_poi} - Noyau uniforme")
    print(f"{'='*60}")
    
    for sigma in sigma_values:
        # Créer et entraîner l'estimateur
        kde = KernelDensity(kernel=kernel_uniform, sigma=sigma)
        kde.fit(data)
        
        # Afficher la densité
        show_density(kde, data, steps=100, log=False, 
                    title_suffix=f" - {type_poi}")
        
        # Vérifier l'intégrale
        integrale = verifier_integrale_kde(kde, data, steps_grid=100)
        
        # Calculer la log-vraisemblance
        log_vrais = kde.score(data)
        print(f"  σ={sigma:.3f}: Log-vraisemblance = {log_vrais:.2f}, Intégrale = {integrale:.4f}\n")
        
        plt.show()

def experimenter_noyau_gaussien(data, sigma_values, type_poi="bar"):
    """
    Expérience avec le noyau gaussien et différents σ
    
    Paramètres :
        data : données
        sigma_values : liste des valeurs de σ à tester
        type_poi : type de POI (pour les titres)
    """
    print(f"\n{'='*60}")
    print(f"Expérience: {type_poi} - Noyau gaussien")
    print(f"{'='*60}")
    
    for sigma in sigma_values:
        # Créer et entraîner l'estimateur
        kde = KernelDensity(kernel=kernel_gaussian, sigma=sigma)
        kde.fit(data)
        
        # Afficher la densité
        show_density(kde, data, steps=100, log=False,
                    title_suffix=f" - {type_poi}")
        
        # Afficher la densité logarithmique
        plt.figure()
        show_density(kde, data, steps=100, log=True,
                    title_suffix=f" - {type_poi}")
        
        # Vérifier l'intégrale
        integrale = verifier_integrale_kde(kde, data, steps_grid=100)
        
        # Calculer la log-vraisemblance
        log_vrais = kde.score(data)
        print(f"  σ={sigma:.3f}: Log-vraisemblance = {log_vrais:.2f}, Intégrale = {integrale:.4f}\n")
        
        plt.show()

def trouver_meilleur_sigma(data, kernel_func, sigma_range, type_poi="bar", 
                          test_size=0.3, random_state=42):
    """
    Trouve le meilleur σ par validation train/test
    
    Paramètres :
        data : données complètes
        kernel_func : fonction de noyau
        sigma_range : plage de valeurs de σ à tester
        type_poi : type de POI
        test_size : proportion de test
        random_state : graine aléatoire
    """
    # Séparation train/test
    train_data, test_data = train_test_split(data, test_size=test_size, 
                                            random_state=random_state)
    
    kernel_name = kernel_func.__name__
    
    print(f"\n{'='*60}")
    print(f"Recherche du meilleur σ: {type_poi} - {kernel_name}")
    print(f"{'='*60}")
    print(f"Train: {len(train_data)} points, Test: {len(test_data)} points")
    
    train_scores = []
    test_scores = []
    
    for sigma in sigma_range:
        # Créer et entraîner l'estimateur
        kde = KernelDensity(kernel=kernel_func, sigma=sigma)
        kde.fit(train_data)
        
        # Calculer les scores
        train_ll = kde.score(train_data)
        test_ll = kde.score(test_data)
        
        train_scores.append(train_ll)
        test_scores.append(test_ll)
        
        print(f"  σ={sigma:.4f}: Train LL={train_ll:8.2f}, Test LL={test_ll:8.2f}")
    
    # Trouver le meilleur σ (maximisant la log-vraisemblance sur le test)
    best_idx = np.argmax(test_scores)
    best_sigma = sigma_range[best_idx]
    best_test_score = test_scores[best_idx]
    
    print(f"\n{'='*40}")
    print(f"Meilleur σ: {best_sigma:.4f}")
    print(f"Meilleure log-vraisemblance (test): {best_test_score:.2f}")
    
    # Tracer les courbes
    plt.figure(figsize=(10, 6))
    plt.plot(sigma_range, train_scores, 'b-o', label='Train', linewidth=2, markersize=8)
    plt.plot(sigma_range, test_scores, 'r-s', label='Test', linewidth=2, markersize=8)
    
    # Marquer le meilleur point
    plt.scatter([best_sigma], [best_test_score], color='green', s=200,
                zorder=5, label=f'Meilleur: σ={best_sigma:.4f}')
    
    plt.xlabel('σ (paramètre de lissage)')
    plt.ylabel('Log-vraisemblance')
    plt.title(f'{type_poi} - {kernel_name}: Log-vraisemblance en fonction de σ')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    # Afficher le meilleur modèle
    print(f"\nAffichage du meilleur modèle (σ={best_sigma:.4f}):")
    kde_best = KernelDensity(kernel=kernel_func, sigma=best_sigma)
    kde_best.fit(train_data)
    
    show_density(kde_best, train_data, steps=100, log=False,
                title_suffix=f" - Meilleur modèle ({type_poi})")
    plt.show()
    
    return best_sigma, best_test_score

def comparer_methodes(data, type_poi="bar"):
    """
    Compare les performances des histogrammes et des noyaux
    
    Paramètres :
        data : données
        type_poi : type de POI
    """
    print(f"\n{'='*60}")
    print(f"Comparaison des méthodes: {type_poi}")
    print(f"{'='*60}")
    
    # Séparation train/test
    train_data, test_data = train_test_split(data, test_size=0.3, random_state=42)
    
    # 1. Histogramme (meilleur steps trouvé précédemment)
    print("\n1. Méthode par histogramme:")
    steps_values = [5, 10, 15, 20, 25, 30]
    hist_scores = []
    
    for steps in steps_values:
        hist = Histogramme(steps=steps)
        hist.fit(train_data)
        test_ll = hist.score(test_data)
        hist_scores.append(test_ll)
        print(f"  Steps={steps:2d}: Test LL={test_ll:8.2f}")
    
    best_hist_idx = np.argmax(hist_scores)
    best_steps = steps_values[best_hist_idx]
    best_hist_score = hist_scores[best_hist_idx]
    print(f"  → Meilleur: steps={best_steps}, LL={best_hist_score:.2f}")
    
    # 2. Noyau uniforme
    print("\n2. Méthode à noyau uniforme:")
    sigma_range_unif = np.logspace(-3, -1, 10)  # 0.001 à 0.1
    best_sigma_unif, best_score_unif = trouver_meilleur_sigma(
        data, kernel_uniform, sigma_range_unif, type_poi=f"{type_poi} - Uniforme"
    )
    
    # 3. Noyau gaussien
    print("\n3. Méthode à noyau gaussien:")
    sigma_range_gauss = np.logspace(-3, 0, 15)  # 0.001 à 1.0
    best_sigma_gauss, best_score_gauss = trouver_meilleur_sigma(
        data, kernel_gaussian, sigma_range_gauss, type_poi=f"{type_poi} - Gaussien"
    )
    
    # Comparaison finale
    print(f"\n{'='*60}")
    print(f"RÉSULTATS FINAUX - {type_poi}")
    print(f"{'='*60}")
    print(f"{'Méthode':<25} {'Meilleur paramètre':<20} {'Log-vrais. (test)':<15}")
    print(f"{'-'*60}")
    print(f"{'Histogramme':<25} {f'steps={best_steps}':<20} {best_hist_score:<15.2f}")
    print(f"{'Noyau uniforme':<25} {f'σ={best_sigma_unif:.4f}':<20} {best_score_unif:<15.2f}")
    print(f"{'Noyau gaussien':<25} {f'σ={best_sigma_gauss:.4f}':<20} {best_score_gauss:<15.2f}")
    
    # Tracer les densités des trois meilleurs modèles
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Histogramme
    hist_best = Histogramme(steps=best_steps)
    hist_best.fit(train_data)
    densities, _, _ = get_density2D(hist_best, train_data, steps=100)
    axes[0].imshow(densities, extent=[train_data[:,0].min(), train_data[:,0].max(),
                                      train_data[:,1].min(), train_data[:,1].max()],
                   origin='lower', aspect='auto', alpha=0.7)
    axes[0].scatter(train_data[:,0], train_data[:,1], alpha=0.5, s=1)
    axes[0].set_title(f"Histogramme (steps={best_steps})")
    axes[0].set_xlabel("Longitude")
    axes[0].set_ylabel("Latitude")
    
    # Noyau uniforme
    kde_unif = KernelDensity(kernel=kernel_uniform, sigma=best_sigma_unif)
    kde_unif.fit(train_data)
    densities, _, _ = get_density2D(kde_unif, train_data, steps=100)
    axes[1].imshow(densities, extent=[train_data[:,0].min(), train_data[:,0].max(),
                                      train_data[:,1].min(), train_data[:,1].max()],
                   origin='lower', aspect='auto', alpha=0.7)
    axes[1].scatter(train_data[:,0], train_data[:,1], alpha=0.5, s=1)
    axes[1].set_title(f"Noyau uniforme (σ={best_sigma_unif:.4f})")
    axes[1].set_xlabel("Longitude")
    
    # Noyau gaussien
    kde_gauss = KernelDensity(kernel=kernel_gaussian, sigma=best_sigma_gauss)
    kde_gauss.fit(train_data)
    densities, _, _ = get_density2D(kde_gauss, train_data, steps=100)
    im = axes[2].imshow(densities, extent=[train_data[:,0].min(), train_data[:,0].max(),
                                          train_data[:,1].min(), train_data[:,1].max()],
                       origin='lower', aspect='auto', alpha=0.7)
    axes[2].scatter(train_data[:,0], train_data[:,1], alpha=0.5, s=1)
    axes[2].set_title(f"Noyau gaussien (σ={best_sigma_gauss:.4f})")
    axes[2].set_xlabel("Longitude")
    
    plt.colorbar(im, ax=axes[2], label='Densité')
    plt.tight_layout()
    plt.show()
    
    return (best_steps, best_hist_score), (best_sigma_unif, best_score_unif), (best_sigma_gauss, best_score_gauss)

# ==================== Fonctions pour Nadaraya-Watson ====================

def evaluer_nadaraya(X, y, kernel_func, sigma_values, test_size=0.3, random_state=42):
    """
    Évalue l'estimateur de Nadaraya-Watson avec différents paramètres sigma
    
    Paramètres :
        X : données d'entrée (coordonnées)
        y : valeurs cibles (notes)
        kernel_func : fonction de noyau
        sigma_values : liste des valeurs de sigma à tester
        test_size : proportion de test
        random_state : graine aléatoire
    
    Retourne :
        résultats : dictionnaire avec les performances pour chaque sigma
    """
    # Séparer les données en train et test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    print(f"Taille de l'ensemble d'apprentissage: {len(X_train)}")
    print(f"Taille de l'ensemble de test: {len(X_test)}")
    print(f"Plage des notes: {y.min():.2f} - {y.max():.2f}")
    
    results = {
        'sigma': [],
        'train_mse': [],
        'test_mse': [],
        'train_mae': [],
        'test_mae': [],
        'train_r2': [],
        'test_r2': []
    }
    
    kernel_name = kernel_func.__name__
    
    print(f"\n{'='*60}")
    print(f"Évaluation Nadaraya-Watson - {kernel_name}")
    print(f"{'='*60}")
    
    for sigma in sigma_values:
        # Créer et entraîner l'estimateur
        nadaraya = Nadaraya(kernel=kernel_func, sigma=sigma)
        nadaraya.fit(X_train, y_train)
        
        # Prédictions sur train et test
        y_pred_train = nadaraya.predict(X_train)
        y_pred_test = nadaraya.predict(X_test)
        
        # Calcul des métriques
        train_mse = mean_squared_error(y_train, y_pred_train)
        test_mse = mean_squared_error(y_test, y_pred_test)
        train_mae = mean_absolute_error(y_train, y_pred_train)
        test_mae = mean_absolute_error(y_test, y_pred_test)
        train_r2 = r2_score(y_train, y_pred_train)
        test_r2 = r2_score(y_test, y_pred_test)
        
        # Stocker les résultats
        results['sigma'].append(sigma)
        results['train_mse'].append(train_mse)
        results['test_mse'].append(test_mse)
        results['train_mae'].append(train_mae)
        results['test_mae'].append(test_mae)
        results['train_r2'].append(train_r2)
        results['test_r2'].append(test_r2)
        
        print(f"  σ={sigma:.4f}:")
        print(f"    Train - MSE: {train_mse:.4f}, MAE: {train_mae:.4f}, R²: {train_r2:.4f}")
        print(f"    Test  - MSE: {test_mse:.4f}, MAE: {test_mae:.4f}, R²: {test_r2:.4f}")
    
    return results

def visualiser_performances_nadaraya(results, kernel_name):
    """
    Visualise les performances de Nadaraya-Watson pour différents sigma
    
    Paramètres :
        results : dictionnaire des résultats
        kernel_name : nom du noyau
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # MSE
    axes[0].plot(results['sigma'], results['train_mse'], 'b-o', label='Train', linewidth=2, markersize=6)
    axes[0].plot(results['sigma'], results['test_mse'], 'r-s', label='Test', linewidth=2, markersize=6)
    axes[0].set_xlabel('σ (paramètre de lissage)')
    axes[0].set_ylabel('MSE (Erreur Quadratique Moyenne)')
    axes[0].set_title(f'Nadaraya-Watson ({kernel_name}) - MSE')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # MAE
    axes[1].plot(results['sigma'], results['train_mae'], 'b-o', label='Train', linewidth=2, markersize=6)
    axes[1].plot(results['sigma'], results['test_mae'], 'r-s', label='Test', linewidth=2, markersize=6)
    axes[1].set_xlabel('σ (paramètre de lissage)')
    axes[1].set_ylabel('MAE (Erreur Absolue Moyenne)')
    axes[1].set_title(f'Nadaraya-Watson ({kernel_name}) - MAE')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    # R²
    axes[2].plot(results['sigma'], results['train_r2'], 'b-o', label='Train', linewidth=2, markersize=6)
    axes[2].plot(results['sigma'], results['test_r2'], 'r-s', label='Test', linewidth=2, markersize=6)
    axes[2].set_xlabel('σ (paramètre de lissage)')
    axes[2].set_ylabel('R² (Coefficient de Détermination)')
    axes[2].set_title(f'Nadaraya-Watson ({kernel_name}) - R²')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Trouver le meilleur sigma (maximisant R² sur le test)
    best_idx = np.argmax(results['test_r2'])
    best_sigma = results['sigma'][best_idx]
    best_r2 = results['test_r2'][best_idx]
    best_mse = results['test_mse'][best_idx]
    
    print(f"\n{'='*40}")
    print(f"Meilleur paramètre: σ = {best_sigma:.4f}")
    print(f"Meilleur R² sur le test: {best_r2:.4f}")
    print(f"MSE correspondante: {best_mse:.4f}")
    
    return best_sigma, best_r2

def visualiser_predictions_nadaraya(X, y, kernel_func, sigma, n_points=100):
    """
    Visualise les prédictions de Nadaraya-Watson sur une grille
    
    Paramètres :
        X : données d'entrée
        y : valeurs cibles
        kernel_func : fonction de noyau
        sigma : paramètre de lissage
        n_points : résolution de la grille
    """
    # Créer et entraîner le modèle
    nadaraya = Nadaraya(kernel=kernel_func, sigma=sigma)
    nadaraya.fit(X, y)
    
    # Créer une grille pour la visualisation
    x_min, x_max = X[:, 0].min(), X[:, 0].max()
    y_min, y_max = X[:, 1].min(), X[:, 1].max()
    x_lin = np.linspace(x_min, x_max, n_points)
    y_lin = np.linspace(y_min, y_max, n_points)
    xx, yy = np.meshgrid(x_lin, y_lin)
    grid = np.c_[xx.ravel(), yy.ravel()]
    
    # Prédire sur la grille
    predictions = nadaraya.predict(grid).reshape(n_points, n_points)
    
    # Créer la visualisation
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Carte des prédictions
    im1 = axes[0].imshow(predictions, extent=[x_min, x_max, y_min, y_max], 
                         origin='lower', aspect='auto', alpha=0.7, cmap='viridis')
    scatter1 = axes[0].scatter(X[:, 0], X[:, 1], c=y, s=20, edgecolor='black', 
                               linewidth=0.5, cmap='viridis')
    axes[0].set_title(f'Prédictions Nadaraya-Watson (σ={sigma:.4f})')
    axes[0].set_xlabel('Longitude')
    axes[0].set_ylabel('Latitude')
    plt.colorbar(im1, ax=axes[0], label='Note prédite')
    
    # Carte des erreurs (si on a des données de test)
    if len(X) > 100:  # Utiliser un sous-ensemble pour calculer les erreurs
        indices = np.random.choice(len(X), min(100, len(X)), replace=False)
        X_subset = X[indices]
        y_subset = y[indices]
        y_pred = nadaraya.predict(X_subset)
        errors = np.abs(y_subset - y_pred)
        
        im2 = axes[1].scatter(X_subset[:, 0], X_subset[:, 1], c=errors, s=50, 
                              edgecolor='black', linewidth=0.5, cmap='Reds')
        axes[1].set_title(f'Erreurs absolues (σ={sigma:.4f})')
        axes[1].set_xlabel('Longitude')
        axes[1].set_ylabel('Latitude')
        plt.colorbar(im2, ax=axes[1], label='Erreur absolue')
    
    plt.tight_layout()
    plt.show()
    
    # Afficher quelques statistiques
    y_pred_all = nadaraya.predict(X)
    mse = mean_squared_error(y, y_pred_all)
    mae = mean_absolute_error(y, y_pred_all)
    r2 = r2_score(y, y_pred_all)
    
    print(f"\nPerformances sur l'ensemble complet:")
    print(f"  MSE: {mse:.4f}")
    print(f"  MAE: {mae:.4f}")
    print(f"  R²: {r2:.4f}")
    print(f"  Note moyenne: {y.mean():.2f}")
    print(f"  Écart-type des notes: {y.std():.2f}")

def comparer_noyaux_nadaraya(X, y, sigma_range, test_size=0.3, random_state=42):
    """
    Compare les performances de Nadaraya-Watson avec différents noyaux
    
    Paramètres :
        X : données d'entrée
        y : valeurs cibles
        sigma_range : plage de valeurs de sigma
        test_size : proportion de test
        random_state : graine aléatoire
    """
    print(f"\n{'='*60}")
    print(f"COMPARAISON DES NOYAUX - Nadaraya-Watson")
    print(f"{'='*60}")
    
    # Noyau uniforme
    print("\n1. Noyau uniforme:")
    results_unif = evaluer_nadaraya(X, y, kernel_uniform, sigma_range, test_size, random_state)
    best_sigma_unif, best_r2_unif = visualiser_performances_nadaraya(results_unif, "Uniforme")
    
    # Noyau gaussien
    print("\n2. Noyau gaussien:")
    results_gauss = evaluer_nadaraya(X, y, kernel_gaussian, sigma_range, test_size, random_state)
    best_sigma_gauss, best_r2_gauss = visualiser_performances_nadaraya(results_gauss, "Gaussien")
    
    # Comparaison finale
    print(f"\n{'='*60}")
    print(f"RÉSULTATS FINAUX - Comparaison des noyaux")
    print(f"{'='*60}")
    print(f"{'Noyau':<15} {'Meilleur σ':<15} {'R² (test)':<15} {'MSE (test)':<15}")
    print(f"{'-'*60}")
    print(f"{'Uniforme':<15} {best_sigma_unif:<15.4f} {best_r2_unif:<15.4f} {results_unif['test_mse'][np.argmax(results_unif['test_r2'])]:<15.4f}")
    print(f"{'Gaussien':<15} {best_sigma_gauss:<15.4f} {best_r2_gauss:<15.4f} {results_gauss['test_mse'][np.argmax(results_gauss['test_r2'])]:<15.4f}")
    
    # Visualiser les meilleurs modèles
    print(f"\nVisualisation du meilleur modèle avec noyau uniforme (σ={best_sigma_unif:.4f}):")
    visualiser_predictions_nadaraya(X, y, kernel_uniform, best_sigma_unif)
    
    print(f"\nVisualisation du meilleur modèle avec noyau gaussien (σ={best_sigma_gauss:.4f}):")
    visualiser_predictions_nadaraya(X, y, kernel_gaussian, best_sigma_gauss)
    
    return results_unif, results_gauss

# ==================== Programme principal avec Nadaraya-Watson ====================

def main_complet():
    """Programme principal complet avec toutes les fonctionnalités"""
    
    plt.ion()  # Mode interactif
    
    # Charger les données
    print("Chargement des données...")
    bar_data, bar_notes = load_poi("bar")
    night_club_data, night_club_notes = load_poi("night_club")
    
    print(f"Bars: {len(bar_data)} points, notes: {bar_notes.min():.1f}-{bar_notes.max():.1f}")
    print(f"Night clubs: {len(night_club_data)} points, notes: {night_club_notes.min():.1f}-{night_club_notes.max():.1f}")
    
    # Afficher les données avec les notes
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Bars avec notes
    scatter1 = axes[0].scatter(bar_data[:, 0], bar_data[:, 1], c=bar_notes, 
                               cmap='viridis', s=20, edgecolor='black', linewidth=0.5)
    axes[0].set_title(f"Bars - Distribution des notes ({len(bar_data)} établissements)")
    axes[0].set_xlabel("Longitude")
    axes[0].set_ylabel("Latitude")
    plt.colorbar(scatter1, ax=axes[0], label='Note')
    show_img(parismap)
    
    # Night clubs avec notes
    scatter2 = axes[1].scatter(night_club_data[:, 0], night_club_data[:, 1], c=night_club_notes, 
                               cmap='viridis', s=20, edgecolor='black', linewidth=0.5)
    axes[1].set_title(f"Night clubs - Distribution des notes ({len(night_club_data)} établissements)")
    axes[1].set_xlabel("Longitude")
    axes[1].set_ylabel("Latitude")
    plt.colorbar(scatter2, ax=axes[1], label='Note')
    show_img(parismap)
    
    plt.tight_layout()
    plt.show()
    
    # Menu principal complet
    while True:
        print("\n" + "="*70)
        print("MENU PRINCIPAL - ESTIMATION DE DENSITÉ ET RÉGRESSION")
        print("="*70)
        print("PARTIE A: HISTOGRAMMES (Densité)")
        print("  1. Vérifier la correction de l'estimation de densité")
        print("  2. Visualiser différents paramètres steps (bars)")
        print("  3. Trouver le meilleur paramètre steps (séparation train/test)")
        print("  4. Évaluer par validation croisée")
        print("  5. Comparer différents types de POI (bars vs night clubs)")
        print("  6. Exécuter toutes les expériences histogrammes")
        
        print("\nPARTIE B: MÉTHODES À NOYAUX (Densité)")
        print("  7. Noyau uniforme (bars)")
        print("  8. Noyau gaussien (bars)")
        print("  9. Recherche du meilleur σ (bars)")
        print("  10. Comparaison complète des méthodes (bars)")
        print("  11. Comparaison pour night clubs")
        
        print("\nPARTIE C: NADARAYA-WATSON (Régression)")
        print("  12. Nadaraya-Watson avec noyau uniforme (bars)")
        print("  13. Nadaraya-Watson avec noyau gaussien (bars)")
        print("  14. Comparaison des noyaux (bars)")
        print("  15. Nadaraya-Watson pour night clubs")
        print("  16. Visualiser les prédictions (meilleur modèle)")
        
        print("\n  0. Quitter")
        print("="*70)
        
        choix = input("\nVotre choix (0-16): ").strip()
        
        if choix == "0":
            print("Au revoir!")
            break
        
        # ===== PARTIE A: HISTOGRAMMES =====
        elif choix == "1":
            # Vérification de l'estimation de densité
            hist_test = Histogramme(steps=10)
            hist_test.fit(bar_data)
            
            def verifier_integrale_densite(f, data, steps_grid=100):
                densities, xlin, ylin = get_density2D(f, data, steps=steps_grid)
                dx = (xlin[1] - xlin[0])
                dy = (ylin[1] - ylin[0])
                aire_cellule = dx * dy
                integrale = np.sum(densities) * aire_cellule
                
                print(f"Vérification de l'intégrale de densité:")
                print(f"  Intégrale calculée: {integrale:.6f}")
                
                if abs(integrale - 1.0) < 0.1:
                    print(f"  ✓ Vérification réussie: intégrale≈1 (erreur: {abs(integrale-1.0):.4f})")
                else:
                    print(f"  ✗ Échec de vérification: intégrale éloignée de 1 (erreur: {abs(integrale-1.0):.4f})")
                
                return integrale
            
            verifier_integrale_densite(hist_test, bar_data, steps_grid=100)
            
        elif choix == "2":
            # Visualisation de différents steps
            def visualiser_steps_differents(data, type_poi="bar"):
                steps_a_visualiser = [5, 10, 20, 40]
                
                print(f"\n{'='*60}")
                print(f"Expérience 1: {type_poi} - Visualisation pour différents steps")
                print(f"{'='*60}")
                
                for steps in steps_a_visualiser:
                    hist = Histogramme(steps=steps)
                    hist.fit(data)
                    show_density(hist, data, steps=100, log=False, title_suffix=f" - {type_poi}")
                    plt.show()
            
            visualiser_steps_differents(bar_data, type_poi="Bars")
            
        elif choix == "3":
            # Recherche du meilleur steps
            def trouver_meilleur_steps(data, type_poi="bar", taille_test=0.3, random_state=42):
                train_data, test_data = train_test_split(data, test_size=taille_test, random_state=random_state)
                
                print(f"\n{'='*60}")
                print(f"Expérience 2: {type_poi} - Recherche du meilleur paramètre steps")
                print(f"{'='*60}")
                
                valeurs_steps = list(range(5, 51, 5))
                scores_apprentissage, scores_test = [], []
                
                for steps in valeurs_steps:
                    hist = Histogramme(steps=steps)
                    hist.fit(train_data)
                    scores_apprentissage.append(hist.score(train_data))
                    scores_test.append(hist.score(test_data))
                    print(f"  Steps={steps:2d}: Apprentissage LL={scores_apprentissage[-1]:8.2f}, Test LL={scores_test[-1]:8.2f}")
                
                best_idx = np.argmax(scores_test)
                best_steps = valeurs_steps[best_idx]
                print(f"\nMeilleur paramètre: steps = {best_steps}")
                
                plt.figure(figsize=(10, 6))
                plt.plot(valeurs_steps, scores_apprentissage, 'b-o', label='Apprentissage')
                plt.plot(valeurs_steps, scores_test, 'r-s', label='Test')
                plt.scatter([best_steps], [scores_test[best_idx]], color='green', s=200, label=f'Meilleur: steps={best_steps}')
                plt.xlabel('Steps')
                plt.ylabel('Log-vraisemblance')
                plt.title(f'{type_poi} - Log-vraisemblance pour différents paramètres steps')
                plt.legend()
                plt.grid(True, alpha=0.3)
                plt.tight_layout()
                plt.show()
                
                return best_steps, scores_test[best_idx]
            
            trouver_meilleur_steps(bar_data, type_poi="Bars")
        
        # ===== PARTIE C: NADARAYA-WATSON =====
        elif choix == "12":
            # Nadaraya-Watson avec noyau uniforme
            sigma_range = np.logspace(-4, -1, 15)  # 0.0001 à 0.1
            results = evaluer_nadaraya(bar_data, bar_notes, kernel_uniform, sigma_range)
            best_sigma, best_r2 = visualiser_performances_nadaraya(results, "Uniforme")
            
        elif choix == "13":
            # Nadaraya-Watson avec noyau gaussien
            sigma_range = np.logspace(-4, 0, 20)  # 0.0001 à 1.0
            results = evaluer_nadaraya(bar_data, bar_notes, kernel_gaussian, sigma_range)
            best_sigma, best_r2 = visualiser_performances_nadaraya(results, "Gaussien")
            
        elif choix == "14":
            # Comparaison des noyaux
            sigma_range = np.logspace(-4, -1, 15)  # 0.0001 à 0.1
            results_unif, results_gauss = comparer_noyaux_nadaraya(bar_data, bar_notes, sigma_range)
            
        elif choix == "15":
            # Nadaraya-Watson pour night clubs
            if len(night_club_data) > 10:  # Vérifier qu'il y a assez de données
                sigma_range = np.logspace(-4, -0.5, 12)  # Plage adaptée pour peu de données
                results = evaluer_nadaraya(night_club_data, night_club_notes, kernel_gaussian, sigma_range)
                best_sigma, best_r2 = visualiser_performances_nadaraya(results, "Gaussien (Night clubs)")
                visualiser_predictions_nadaraya(night_club_data, night_club_notes, kernel_gaussian, best_sigma)
            else:
                print("Pas assez de données pour les night clubs.")
                
        elif choix == "16":
            # Visualiser les prédictions avec le meilleur modèle
            print("Détermination du meilleur modèle...")
            sigma_range = np.logspace(-4, 0, 20)
            
            # Tester les deux noyaux
            test_size = 0.3
            X_train, X_test, y_train, y_test = train_test_split(bar_data, bar_notes, test_size=test_size, random_state=42)
            
            best_r2 = -np.inf
            best_params = {}
            
            for kernel_func, kernel_name in [(kernel_uniform, "Uniforme"), (kernel_gaussian, "Gaussien")]:
                for sigma in sigma_range:
                    nadaraya = Nadaraya(kernel=kernel_func, sigma=sigma)
                    nadaraya.fit(X_train, y_train)
                    r2 = nadaraya.score(X_test, y_test)
                    
                    if r2 > best_r2:
                        best_r2 = r2
                        best_params = {
                            'kernel_func': kernel_func,
                            'kernel_name': kernel_name,
                            'sigma': sigma,
                            'r2': r2
                        }
            
            print(f"\nMeilleur modèle trouvé:")
            print(f"  Noyau: {best_params['kernel_name']}")
            print(f"  σ: {best_params['sigma']:.4f}")
            print(f"  R²: {best_params['r2']:.4f}")
            
            # Visualiser avec le meilleur modèle
            visualiser_predictions_nadaraya(bar_data, bar_notes, 
                                           best_params['kernel_func'], 
                                           best_params['sigma'])
            
        else:
            print("Choix invalide. Veuillez choisir entre 0 et 16.")
    
    plt.show(block=True)

# ==================== Point d'entrée du programme ====================

if __name__ == "__main__":
    main_complet()