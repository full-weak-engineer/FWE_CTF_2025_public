from sage.all import *
from Crypto.Util.number import *
import gmpy2
import random
from sympy import nextprime

FLAG = b'fwectf{REDACTED_REDACTED_REDACTED}'
m = bytes_to_long(FLAG)
r = random.randint(5, 30)

p = getPrime(256)
q = getPrime(256)
if p < q:
    p, q = q, p
N = pow(p, r) * q
phi = pow(p, r - 1) * (p - 1) * (q - 1)

e = 65537

c = pow(m, e, N)
print(f'c = {c}')
print(f'e = {e}')
print(f'N = {N}')

d1 = getPrime(2000)
d2 = nextprime(d1 + getPrime(1000))
e1 = gmpy2.invert(d1, phi)
e2 = gmpy2.invert(d2, phi)
print(f'e1 = {e1}')
print(f'e2 = {e2}')