# Sorbonne Université LU3IN024 2024-2025
# TME 5 : Cryptographie à base de courbes elliptiques
#
# Etudiant.e 1 : ZHANG Yuxiang 21202829
# Etudiant.e 2 : LECOMTE Antoine 21103457

from math import sqrt
import matplotlib.pyplot as plt
from random import randint

# Fonctions utiles

def exp(a, N, p):
    """Renvoie a**N % p par exponentiation rapide."""
    def binaire(N):
        L = list()
        while (N > 0):
            L.append(N % 2)
            N = N // 2
        L.reverse()
        return L
    res = 1
    for Ni in binaire(N):
        res = (res * res) % p
        if (Ni == 1):
            res = (res * a) % p
    return res


def factor(n):
    """ Return the list of couples (p, a_p) where p is a prime divisor of n and
    a_p is the p-adic valuation of n. """
    def factor_gen(n):
        j = 2
        while n > 1:
            for i in range(j, int(sqrt(n)) + 1):
                if n % i == 0:
                    n //= i
                    j = i
                    yield i
                    break
            else:
                if n > 1:
                    yield n
                    break

    factors_with_multiplicity = list(factor_gen(n))
    factors_set = set(factors_with_multiplicity)

    return [(p, factors_with_multiplicity.count(p)) for p in factors_set]


def inv_mod(x, p):
    """Renvoie l'inverse de x modulo p."""
    return exp(x, p-2, p)


def racine_carree(a, p):
    """Renvoie une racine carrée de a mod p si p = 3 mod 4."""
    assert p % 4 == 3, "erreur: p != 3 mod 4"

    return exp(a, (p + 1) // 4, p)


# Fonctions demandées dans le TME

def est_elliptique(E):
    """
    Renvoie True si la courbe E est elliptique et False sinon.

    E : un triplet (p, a, b) représentant la courbe d'équation
    y^2 = x^3 + ax + b sur F_p, p > 3
    """
    p, a, b = E
    delta = -16 * (4 * (a ** 3) + 27 * (b ** 2)) % p
    return delta != 0


def point_sur_courbe(P, E):
    """
    Renvoie True si le point P appartient à la courbe E et False sinon.

    P : un couple (x, y) représentant le point ou le tuple vide () pour le point à l'infini
    E : un triplet (p, a, b) représentant la courbe d'équation
    y^2 = x^3 + ax + b sur F_p
    """
    p, a, b = E
    if P == ():
        return True
    x, y = P
    return (y ** 2) % p == (x ** 3 + a * x + b) % p


def symbole_legendre(a, p):
    """
    Renvoie le symbole de Legendre de a mod p.

    a : un entier
    p : un nombre premier
    """
    if a % p == 0:
        return 0
    result = exp(a, (p - 1) // 2, p)
    return result if result == p - 1 else result


def cardinal(E):
    """
    Renvoie le cardinal du groupe de points de la courbe E.

    E : un triplet (p, a, b) représentant la courbe d'équation
    y^2 = x^3 + ax + b sur F_p
    """
    p, a, b = E
    count = 1

    for x in range(p):
        rhs = (x ** 3 + a * x + b) % p
        legendre_symbol = symbole_legendre(rhs, p)
        if legendre_symbol == 1:
            count += 2
        elif legendre_symbol == 0:
            count += 1

    return count


def liste_points(E):
    """
    Renvoie la liste des points de la courbe elliptique E.

    E : un triplet (p, a, b) représentant la courbe d'équation
    y^2 = x^3 + ax + b sur F_p
    """
    p, a, b = E

    assert p % 4 == 3, "erreur: p n'est pas congru à 3 mod 4."

    points = [()]

    for x in range(p):
        rhs = (x ** 3 + a * x + b) % p
        if symbole_legendre(rhs, p) == 1:
            y = racine_carree(rhs, p)
            points.append((x, y))
            points.append((x, (-y) % p))
        elif symbole_legendre(rhs, p) == 0:
            points.append((x, 0))

    return points


def cardinaux_courbes(p):
    """
    Renvoie la distribution des cardinaux des courbes elliptiques définies sur F_p.

    Renvoie un dictionnaire D où D[i] contient le nombre de courbes elliptiques
    de cardinal i sur F_p.
    """
    D = {}
    for a in range(p):
        for b in range(p):
            E = (p, a, b)
            if est_elliptique(E):
                c = cardinal(E)
                D[c] = D.get(c, 0) + 1
    return D


def dessine_graphe(p):
    """Dessine le graphe de répartition des cardinaux des courbes elliptiques définies sur F_p."""
    bound = int(2 * sqrt(p))
    C = [c for c in range(p + 1 - bound, p + 1 + bound + 1)]
    D = cardinaux_courbes(p)

    plt.bar(C, [D[c] for c in C], color='b')
    plt.show()


def moins(P, p):
    """Retourne l'opposé du point P mod p."""
    if est_zero(P):
        return P
    x, y = P
    return (x, (-y) % p)


def est_egal(P1, P2, p):
    """Teste l'égalité de deux points mod p."""
    if est_zero(P1) and est_zero(P2):
        return True
    if est_zero(P1) or est_zero(P2):
        return False
    x1, y1 = P1
    x2, y2 = P2
    return x1 % p == x2 % p and y1 % p == y2 % p


def est_zero(P):
    """Teste si un point est égal au point à l'infini."""
    return P == ()


def addition(P1, P2, E):
    """Renvoie P1 + P2 sur la courbe E."""
    p, a, b = E

    if est_zero(P1):
        return P2
    if est_zero(P2):
        return P1

    x1, y1 = P1
    x2, y2 = P2

    if est_egal(P1, moins(P2, p), p):
        return ()

    if est_egal(P1, P2, p):
        if y1 == 0:
            return ()
        lambda_ = ((3 * x1 ** 2 + a) * inv_mod(2 * y1, p)) % p
    else:
        if x1 == x2:
            return ()
        lambda_ = ((y2 - y1) * inv_mod(x2 - x1, p)) % p

    x3 = (lambda_ ** 2 - x1 - x2) % p
    y3 = (lambda_ * (x1 - x3) - y1) % p

    return (x3, y3)


def multiplication_scalaire(k, P, E):
    """Renvoie la multiplication scalaire k*P sur la courbe E."""
    if k < 0:
        return multiplication_scalaire(-k, moins(P, E[0]), E)

    R = ()
    Q = P
    while k > 0:
        if k % 2 == 1:
            R = addition(R, Q, E)
        Q = addition(Q, Q, E)
        k //= 2
    return R


def ordre(N, factors_N, P, E):
    """
    Renvoie l'ordre du point P dans les points de la courbe E mod p. 
    N est le nombre de points de E sur Fp.
    factors_N est la factorisation de N en liste [(p1, a1), (p2, a2), ...]
    """
    ordre_P = N
    for (q, _) in factors_N:
        while ordre_P % q == 0:
            m = ordre_P // q
            if est_zero(multiplication_scalaire(m, P, E)):
                ordre_P = m
            else:
                break
    return ordre_P


def point_aleatoire_naif(E):
    """Renvoie un point (x, y) aléatoire appartenant à la courbe E."""
    p, _, _ = E
    while True:
        x = randint(0, p - 1)
        y = randint(0, p - 1)
        if point_sur_courbe((x, y), E):
            return (x, y)
 

def point_aleatoire(E):
    """Renvoie un point (x, y) aléatoire sur E, optimisé pour p ≡ 3 mod 4."""
    p, a, b = E
    assert p % 4 == 3, "Cette méthode suppose que p ≡ 3 mod 4"
    
    while True:
        x = randint(0, p - 1)
        rhs = (x**3 + a*x + b) % p
        if symbole_legendre(rhs, p) == 1:
            y = racine_carree(rhs, p)
            return (x, y)
        elif rhs == 0:
            return (x, 0)


def point_ordre(E, N, factors_N, n):
    """Renvoie un point aléatoire d'ordre exact n."""
    assert N % n == 0
    while True:
        P = point_aleatoire(E)
        Q = multiplication_scalaire(N // n, P, E)
        if not est_zero(Q) and ordre(N, factors_N, Q, E) == n:
            return Q


def keygen_DH(P, E, n):
    """Génère une clé publique et une clé privée pour un échange Diffie-Hellman.
    P est un point d'ordre n sur la courbe E.
    """
    sec = randint(1, n - 1)
    pub = multiplication_scalaire(sec, P, E)
    return (sec, pub)

def echange_DH(sec_A, pub_B, E):
    """Renvoie la clé commune à l'issue d'un échange Diffie-Hellman.
    sec_A est l'entier secret d'Alice et pub_b est l'entier public de Bob."""
    return multiplication_scalaire(sec_A, pub_B, E)
