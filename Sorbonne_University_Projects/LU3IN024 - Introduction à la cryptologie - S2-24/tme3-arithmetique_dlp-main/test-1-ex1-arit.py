from dlp import *
print("\n\n----------------------------------------------\n\n")

print("Test 1 : Exercice 1 - Arithmétique")

print("---------------------")

print("Test bezout et PGCD")
d, u, v = bezout(13, 21)
assert d == 1
assert 13 * u + 21 * v == 1
d, u, v = bezout (105, 30)
assert d == 15
assert 105 * u + 30 * v == 15
print("Test bezout et PGCD : OK")

print("---------------------")

print("Test inverses")
assert (inv_mod(13, 101) * 13) % 101 == 1
assert (inv_mod(3, 8) * 3) % 8 == 1
assert (inv_mod(11,25) == 16)

assert set(invertibles(18)) == set([1, 5, 7, 11, 13, 17])
assert set(invertibles(7)) == set([1, 2, 3, 4, 5, 6])
print("Test inverses : OK")

print("---------------------")

print("Test Indicatrice Euler")
assert phi(18) == 6
assert phi(101) == 100
print("Test Indicatrice Euler : OK")

print("\n\n----------------------------------------------\n\n")
