import random
from math import gcd

def rsa_chiffrement(x, N, e):
    return pow(x, e, N)

def rsa_dechiffrement(y, p, q, d):
    N = p * q
    return pow(y, d, N)

def bezout(a, b):
    if b==0: 
        return a, 1, 0
    pgcd, u1, v1 = bezout(b, a % b)
    u = v1
    v = u1 - (a // b) * v1
    return pgcd, u, v

def inv_mod(a, n):
    _, u, _ = bezout(a, n)
    return u % n

def crt2(a1, a2, n1, n2):
    m1 = inv_mod(n1, n2)
    m2 = inv_mod(n2, n1)
    s = (a1 * n2 * m2 + a2 * n1 * m1) % (n1 * n2)
    return s, None

def rsa_dechiffrement_crt(y, p, q, up, uq, dp, dq, N):
    mp = pow(y, dp, p)
    mq = pow(y, dq, q)
    return crt2(mp, mq, p, q)

def cfrac(a, b):
    fractions = []
    while b:
        fractions.append(a // b)
        a, b = b, a % b
    return fractions

def reduite(L):
    num, denom = 1, 0
    for x in reversed(L):
        num, denom = denom + x * num, num
    return num, denom

def isqrt(n):
    """Compute the integer square root of n using the Newton-Raphson method."""
    if n < 0:
        raise ValueError("Cannot compute square root of negative number.")
    if n == 0 or n == 1:
        return n
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x

def is_perfect_square(n):
    """Check if n is a perfect square using integer square root."""
    root = isqrt(n)
    return root * root == n

def Wiener(m, c, N, e):
    L = cfrac(e, N)
    for i in range(1, len(L)):
        k, d = reduite(L[:i])
        if k == 0:
            continue
        phi_N = (e * d - 1) // k
        if (N - phi_N + 1) % 2 == 0:
            p_q = (N - phi_N + 1) // 2
            disc = p_q ** 2 - N
            if disc >= 0 and is_perfect_square(disc):
                return d
    return None

### Generation de premiers
def is_probable_prime(N, nbases=20):
    """
    True if N is a strong pseudoprime for nbases random bases b < N.
    Uses the Miller--Rabin primality test.
    """

    def miller(a, n):
        """
        Returns True if a proves that n is composite, False if n is probably prime in base n
        """

        def decompose(i, k=0):
            """
            decompose(n) returns (s,d) st. n = 2**s * d, d odd
            """
            if i % 2 == 0:
                return decompose(i // 2, k + 1)
            else:
                return (k, i)

        (s, d) = decompose(n - 1)
        x = pow(a, d, n)
        if (x == 1) or (x == n - 1):
            return False
        while s > 1:
            x = pow(x, 2, n)
            if x == n - 1:
                return False
            s -= 1
        return True

    if N == 2:
        return True
    for i in range(nbases):
        import random
        a = random.randint(2, N - 1)
        if miller(a, N):
            return False
    return True

def random_probable_prime(bits):
    """
    Returns a probable prime number with the given number of bits.
    Remarque : on est sur qu'un premier existe par le postulat de Bertrand
    """
    n = 1 << bits
    import random
    p = random.randint(n, 2 * n - 1)
    while (not (is_probable_prime(p))):
        p = random.randint(n, 2 * n - 1)
    return p
