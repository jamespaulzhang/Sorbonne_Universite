# prime.py
# author: Matthieu Lequesne
# date: 08/01/2016


def is_probable_prime(N, nbases=20):
    """
    True if N is a strong pseudoprime for nbases random bases b < N.
    Uses the Miller--Rabin primality test.

    >>> is_probable_prime(13)
    True
    >>> is_probable_prime(1293871928371928739182731111)
    False
    >>> is_probable_prime(1267650600228229401496703205653)
    True
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

    >>> b = 15
    >>> p = random_probable_prime(b)
    >>> is_probable_prime(p)
    True
    >>> (p>=2**b) and (p< 2**(b+1))
    True
    >>> b = 373
    >>> p = random_probable_prime(b)
    >>> is_probable_prime(p)
    True
    >>> (p>=2**b) and (p< 2**(b+1))
    True
    """
    n = 1 << bits
    import random
    p = random.randint(n, 2 * n - 1)
    while (not (is_probable_prime(p))):
        p = random.randint(n, 2 * n - 1)
    return p
