from dlp import *
from prime import *

print("\n\n----------------------------------------------\n\n")

print("Test 3 : Nombres premiers sûrs")

print("---------------------")

print("Test Generation premier sûr")
p = generate_safe_prime(32)
assert is_probable_prime(p)
assert is_probable_prime((p-1)//2)
print("Test Generation premier sûr : OK")


print("\n\n----------------------------------------------\n\n")

