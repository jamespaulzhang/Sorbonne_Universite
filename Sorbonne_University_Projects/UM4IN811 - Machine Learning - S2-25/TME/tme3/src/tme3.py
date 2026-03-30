import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from functools import partial

# Yuxiang ZHANG & Kenan Alsafadi

# -------------------------------
# Fonctions de coût et gradient
# -------------------------------

def perceptron_loss(w, x, y):
    """
    Coût perceptron : somme des max(0, -y * <w, x>)
    x : (n_samples, n_features)
    y : (n_samples,) avec valeurs +1/-1
    """
    scores = np.dot(x, w)
    margins = -y * scores
    loss = np.maximum(0, margins)
    return np.sum(loss)

def perceptron_grad(w, x, y):
    """
    Gradient du coût perceptron (moyenné sur le batch)
    Retourne le gradient total (somme)
    """
    scores = np.dot(x, w)
    margins = -y * scores
    mask = (margins >= 0).astype(float)
    grad = - (mask * y)[:, np.newaxis] * x
    return np.sum(grad, axis=0)

def hinge_loss(w, x, y, alpha=1.0, lamb=0.01):
    """
    Coût hinge avec régularisation L2
    """
    scores = np.dot(x, w)
    margins = alpha - y * scores
    loss = np.maximum(0, margins)
    reg = lamb * np.dot(w, w)
    return np.sum(loss) + reg

def hinge_grad(w, x, y, alpha=1.0, lamb=0.01):
    """
    Gradient du coût hinge avec régularisation
    """
    scores = np.dot(x, w)
    margins = alpha - y * scores
    mask = (margins > 0).astype(float)
    grad_hinge = - (mask * y)[:, np.newaxis] * x
    grad_reg = 2 * lamb * w
    return np.sum(grad_hinge, axis=0) + grad_reg

# -------------------------------
# Fonctions de projection
# -------------------------------

def proj_biais(datax):
    """Ajoute une colonne de 1 en première position"""
    n = datax.shape[0]
    return np.hstack([np.ones((n, 1)), datax])

def proj_poly(datax, deg=2):
    """
    Projection polynomiale de degré 2 avec biais (1, x1, x2, ..., xd, x1^2, x1x2, ..., xd^2)
    Utilise PolynomialFeatures pour plus de robustesse.
    """
    from sklearn.preprocessing import PolynomialFeatures
    poly = PolynomialFeatures(degree=deg, include_bias=True)
    return poly.fit_transform(datax)

def proj_gauss(datax, base, sigma):
    """
    Projection gaussienne (RBF) sur des points de base.
    datax : (n_samples, n_features)
    base  : (n_bases, n_features)
    sigma : écart-type des gaussiennes
    Retourne : (n_samples, n_bases) avec exp(-||x-b||^2/(2 sigma^2))
    """
    n_samples = datax.shape[0]
    n_bases = base.shape[0]
    # Calcul des distances au carré : ||x-b||^2 = ||x||^2 + ||b||^2 - 2 x.b
    X2 = np.sum(datax**2, axis=1).reshape(-1, 1)
    B2 = np.sum(base**2, axis=1).reshape(1, -1)
    cross = np.dot(datax, base.T)
    dist2 = X2 + B2 - 2 * cross
    dist2 = np.maximum(dist2, 0)  # élimine les négligeables négatifs
    return np.exp(-dist2 / (2 * sigma**2))

# -------------------------------
# Classe Linéaire (descente de gradient)
# -------------------------------

class Lineaire(object):
    def __init__(self, loss=perceptron_loss, loss_g=perceptron_grad, max_iter=100, eps=0.01,
                 projection=None, batch_size=None, random_state=None):
        self.max_iter = max_iter
        self.eps = eps
        self.loss = loss
        self.loss_g = loss_g
        self.projection = projection
        self.batch_size = batch_size
        self.random_state = random_state
        self.w = None
        self.loss_history = []          # coût moyen sur l'apprentissage
        self.train_score_history = []    # précision sur l'apprentissage
        self.test_score_history = []     # précision sur le test (si fourni)

    def _project(self, datax):
        """Applique la projection si définie"""
        if self.projection is not None:
            return self.projection(datax)
        return datax

    def fit(self, datax, datay, testx=None, testy=None, trace=False):
        """
        Entraîne le modèle par descente de gradient (batch, stochastique ou mini-batch)
        max_iter correspond au nombre d'époques.
        Si testx et testy sont fournis, calcule la précision à chaque époque.
        """
        X = self._project(datax)
        n_samples, n_features = X.shape

        if self.w is None:
            self.w = np.random.randn(n_features) * 0.01

        # Taille effective du batch
        if self.batch_size is None:
            batch_size = n_samples   # descente batch
        else:
            batch_size = self.batch_size

        rng = np.random.RandomState(self.random_state)

        # Réinitialisation des historiques
        self.loss_history = []
        self.train_score_history = []
        self.test_score_history = []

        for epoch in range(self.max_iter):
            indices = np.arange(n_samples)
            if batch_size < n_samples:
                rng.shuffle(indices)

            # Parcours par mini-batchs
            for start in range(0, n_samples, batch_size):
                end = min(start + batch_size, n_samples)
                idx = indices[start:end]
                X_batch = X[idx]
                y_batch = datay[idx]

                grad = self.loss_g(self.w, X_batch, y_batch)
                self.w -= self.eps * grad / len(idx)   # mise à jour avec gradient moyen

            # Calcul du coût moyen sur tout l'ensemble d'apprentissage
            loss_val = self.loss(self.w, X, datay) / n_samples
            self.loss_history.append(loss_val)

            # Précision sur l'apprentissage
            train_acc = self.score(datax, datay)
            self.train_score_history.append(train_acc)

            # Précision sur le test si fourni
            if testx is not None and testy is not None:
                test_acc = self.score(testx, testy)
                self.test_score_history.append(test_acc)

            if trace and (epoch % 10 == 0 or epoch == self.max_iter-1):
                print(f"Époque {epoch:3d} : loss = {loss_val:.4f}, train acc = {train_acc:.4f}" +
                      (f", test acc = {test_acc:.4f}" if testx is not None else ""))

        return self

    def predict(self, datax):
        """Prédit les classes (+1/-1) pour les données"""
        X = self._project(datax)
        scores = np.dot(X, self.w)
        return np.sign(scores)

    def score(self, datax, datay):
        """Calcule la précision (pourcentage de bonnes classifications)"""
        pred = self.predict(datax)
        return np.mean(pred == datay)

# -------------------------------
# Fonctions de chargement USPS (fournies dans l'énoncé)
# -------------------------------

def load_usps(fn):
    with open(fn, "r") as f:
        f.readline()
        data = [[float(x) for x in l.split()] for l in f if len(l.split()) > 2]
    tmp = np.array(data)
    return tmp[:, 1:], tmp[:, 0].astype(int)

def get_usps(l, datax, datay):
    if type(l) != list:
        resx = datax[datay == l, :]
        resy = datay[datay == l]
        return resx, resy
    tmp = list(zip(*[get_usps(i, datax, datay) for i in l]))
    tmpx, tmpy = np.vstack(tmp[0]), np.hstack(tmp[1])
    return tmpx, tmpy

def show_usps(data):
    plt.imshow(data.reshape((16, 16)), interpolation="nearest", cmap="gray")

# -------------------------------
# Générateur de données artificielles (simplifié, d'après TME2)
# -------------------------------

def gen_arti(center=0, sigma=0.1, n=100, type='poles'):
    """
    Génère des données 2D artificielles pour deux classes (+1/-1)
    type : 'poles' (deux clusters) ou 'xor'
    """
    if type == 'poles':
        datax1 = np.random.randn(n, 2) * sigma + center
        datax2 = np.random.randn(n, 2) * sigma + np.array([center, -center])
        datax = np.vstack([datax1, datax2])
        datay = np.hstack([np.ones(n), -np.ones(n)])
    elif type == 'xor':
        centers = np.array([[1, 1], [1, -1], [-1, 1], [-1, -1]])
        labels = [1, -1, -1, 1]
        datax_list = []
        datay_list = []
        for i in range(4):
            datax_list.append(np.random.randn(n//4, 2) * sigma + centers[i])
            datay_list.append([labels[i]] * (n//4))
        datax = np.vstack(datax_list)
        datay = np.hstack(datay_list)
    else:
        raise ValueError("type inconnu")
    return datax, datay

# -------------------------------
# Fonction de tracé de frontière (optionnelle, pour visualisation)
# -------------------------------

def plot_frontiere_proba(data, f, step=20):
    grid, x, y = make_grid(data=data, step=step)
    plt.contourf(x, y, f(grid).reshape(x.shape), 255, cmap=cm.RdBu, alpha=0.7)

def make_grid(data=None, xmin=-5, xmax=5, ymin=-5, ymax=5, step=20):
    if data is not None:
        xmin, xmax = data[:, 0].min() - 0.5, data[:, 0].max() + 0.5
        ymin, ymax = data[:, 1].min() - 0.5, data[:, 1].max() + 0.5
    x = np.linspace(xmin, xmax, step)
    y = np.linspace(ymin, ymax, step)
    X, Y = np.meshgrid(x, y)
    grid = np.c_[X.ravel(), Y.ravel()]
    return grid, X, Y

# -------------------------------
# Exemples d'utilisation
# -------------------------------

if __name__ == "__main__":
    # 1. Test sur données artificielles simples (perceptron sans projection)
    print("=== Test perceptron sur données artificielles (poles) ===")
    datax, datay = gen_arti(n=100, type='poles')
    # On s'assure que les labels sont ±1
    datay = np.where(datay == 0, -1, datay)  # normalement déjà ±1

    model = Lineaire(loss=perceptron_loss, loss_g=perceptron_grad, max_iter=50, eps=0.1)
    model.fit(datax, datay, trace=True)
    print("Précision finale :", model.score(datax, datay))

    # Visualisation (optionnelle)
    plt.figure()
    plot_frontiere_proba(datax, lambda x: model.predict(x), step=50)
    plt.scatter(datax[:, 0], datax[:, 1], c=datay, cmap=cm.RdBu, edgecolors='k')
    plt.title("Perceptron sans projection")
    plt.show()

    # 2. Test sur USPS (deux classes)
    print("\n=== Test perceptron sur USPS (6 vs 9) ===")
    usps_train = "../data/USPS_train.txt"
    usps_test  = "../data/USPS_test.txt"
    try:
        alltrainx, alltrainy = load_usps(usps_train)
        alltestx, alltesty = load_usps(usps_test)
    except FileNotFoundError:
        print("Fichiers USPS non trouvés, utilisation de données simulées.")
        # Simulation simple pour test
        alltrainx = np.random.randn(200, 256)
        alltrainy = np.random.randint(0, 10, 200)
        alltestx = np.random.randn(100, 256)
        alltesty = np.random.randint(0, 10, 100)

    # Sélection des classes 6 et 9 (conversion en ±1)
    neg, pos = 6, 9
    trainx, trainy = get_usps([neg, pos], alltrainx, alltrainy)
    testx, testy = get_usps([neg, pos], alltestx, alltesty)
    # Convertir les labels : neg -> -1, pos -> +1
    trainy = np.where(trainy == neg, -1, 1)
    testy = np.where(testy == neg, -1, 1)

    # Perceptron sans projection
    model_usps = Lineaire(loss=perceptron_loss, loss_g=perceptron_grad, max_iter=50, eps=0.01)
    model_usps.fit(trainx, trainy, testx, testy, trace=True)

    # Visualisation du poids (image 16x16)
    plt.figure()
    show_usps(model_usps.w)
    plt.title("Poids du perceptron (6 vs 9)")
    plt.colorbar()
    plt.show()

    # Courbes d'erreur
    plt.figure()
    plt.plot(model_usps.loss_history, label='Coût (train)')
    plt.plot(1 - np.array(model_usps.train_score_history), label='Erreur train')
    plt.plot(1 - np.array(model_usps.test_score_history), label='Erreur test')
    plt.xlabel('Époque')
    plt.ylabel('Erreur / Coût')
    plt.legend()
    plt.title("Évolution de l'erreur (perceptron USPS)")
    plt.show()

    # 3. Test avec projection polynomiale sur données XOR
    print("\n=== Test projection polynomiale sur XOR ===")
    datax, datay = gen_arti(n=200, type='xor', sigma=0.3)
    datay = np.where(datay == 0, -1, datay)

    # Sans projection (linéaire) - devrait échouer
    model_lin = Lineaire(max_iter=100, eps=0.1)
    model_lin.fit(datax, datay)
    print("Score linéaire sur XOR :", model_lin.score(datax, datay))

    # Avec projection polynomiale
    model_poly = Lineaire(projection=proj_poly, max_iter=100, eps=0.1)
    model_poly.fit(datax, datay)
    print("Score polynomial deg2 sur XOR :", model_poly.score(datax, datay))

    # 4. Test avec projection gaussienne sur données artificielles
    print("\n=== Test projection gaussienne sur poles ===")
    datax, datay = gen_arti(n=200, type='poles')
    datay = np.where(datay == 0, -1, datay)

    # Choisir une base de points (par exemple 10 points aléatoires)
    rng = np.random.RandomState(0)
    base = rng.randn(10, 2) * 2  # 10 points répartis
    sigma = 1.0
    proj = partial(proj_gauss, base=base, sigma=sigma)

    model_gauss = Lineaire(projection=proj, max_iter=100, eps=0.1)
    model_gauss.fit(datax, datay)
    print("Score avec projection gaussienne :", model_gauss.score(datax, datay))

    # 5. Test avec hinge loss et régularisation
    print("\n=== Test hinge loss avec régularisation ===")
    # On fixe alpha et lambda via partial
    hinge_loss_fixed = partial(hinge_loss, alpha=1.0, lamb=0.1)
    hinge_grad_fixed = partial(hinge_grad, alpha=1.0, lamb=0.1)

    model_hinge = Lineaire(loss=hinge_loss_fixed, loss_g=hinge_grad_fixed, max_iter=100, eps=0.1)
    model_hinge.fit(datax, datay)
    print("Score hinge :", model_hinge.score(datax, datay))