from dlp import *

print("\n\n----------------------------------------------\n\n")

print("Test 6 : Ex2 DLog")

print("---------------------")

print("Test Exponentiation Modulaire")
assert exp(4364233264, 7343242432, 738264237) == 575772274
print("Test Exponentiation Modulaire : OK")

print("---------------------")

print("Test Factorisation")
assert set(factor(42)) == set([(2,1), (3,1), (7,1)])
assert set(factor(396576)) == set([(17, 1), (2, 5), (3, 6)])
print("Test Factorisation : OK")

print("---------------------")

print("Test Ordre")
assert order(2, 16847137, [(2, 5), (3, 3), (37, 1), (17, 1), (31, 1)]) == 271728
print("Test Ordre : OK")

print("---------------------")

print("Test Generateur")
g = find_generator(101, [(2, 2), (5, 2)])
assert g**(2 * 5**2) % 101 != 1
assert g**(2**2 * 5) % 101 != 1
print("Test Generateur : OK")

print("\n\n----------------------------------------------\n\n")
