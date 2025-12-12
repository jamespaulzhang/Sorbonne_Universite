from prime import is_probable_prime
from math import sqrt
import random


#Exercice 1
#Q1
def bezout(a, b):
    if b==0: 
        return a, 1, 0
    pgcd, u1, v1 = bezout(b, a % b)
    u = v1
    v = u1 - (a // b) * v1
    return pgcd, u, v

#Q2
def inv_mod(a, n):
    _, u, _ = bezout(a, n)
    return u % n


def invertibles(N):
    return [x for x in range(1, N) if bezout(x, N)[0] == 1]


#Q3
def phi(N):
    return sum(1 for x in range(1, N) if bezout(x, N)[0] == 1)


#Exercice 2
#Q1
def exp(a, n, p):
    result = 1
    a = a % p
    while n > 0:
        if n % 2 == 1:
            result = (result * a) % p
        a = (a * a) % p
        n //= 2
    return result


#Q2
def factor(n):
    factors = []
    i = 2
    while i * i <= n:
        count = 0
        while n % i == 0:
            count += 1
            n //= i
        if count > 0:
            factors.append((i, count))
        i += 1
    if n > 1:
        factors.append((n, 1))
    return factors


#Q3
def order(a, p, factors_p_minus1):
    phi_p = p - 1

    def get_divisors(n):
        divisors = {1}
        for prime, exponent in factors_p_minus1:
            new_divisors = set()
            for d in divisors:
                for i in range(exponent + 1):
                    new_divisors.add(d * (prime ** i))
            divisors |= new_divisors
        return sorted(divisors)

    divisors = get_divisors(phi_p)

    for k in divisors:
        if exp(a, k, p) == 1:
            return k
    return phi_p


#Q4
def find_generator(p, factors_p_minus1):
    for g in range(2, p):
        if all(exp(g, (p - 1) // factor[0], p) != 1 for factor in factors_p_minus1):  
            return g
    return None


#Q5
def generate_safe_prime(k):
    while True:
        q = random.getrandbits(k - 1) | 1
        while not is_probable_prime(q):
            q = random.getrandbits(k - 1) | 1
        
        p = 2 * q + 1
        if is_probable_prime(p):
            return p


#Q6
def bsgs(n, g, p):
    m = int(sqrt(p)) + 1
    baby_steps = {exp(g, i, p): i for i in range(m)}
    
    factor = inv_mod(exp(g, m, p), p)
    gamma = n
    
    for j in range(m):
        if gamma in baby_steps:
            return j * m + baby_steps[gamma]
        gamma = (gamma * factor) % p
    
    return None