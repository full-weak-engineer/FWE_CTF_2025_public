import random
from math import gcd

def superincreasing(n, rng):
    seq = []
    total = 0
    for _ in range(n):
        inc = (total + rng.randrange(1<<10, 1<<12)) if total>0 else rng.randrange(1<<10, 1<<12)
        nxt = total + inc + 1
        seq.append(nxt)
        total += nxt
    return seq

def bytes_to_bits_be(bb):
    bits=[]
    for b in bb:
        for k in range(8):
            bits.append( (b >> (7-k)) & 1 )
    return bits

rng = random.Random()
n = 64

w = superincreasing(n, rng)

M = (1<<128) + rng.getrandbits(8)
if M % 2 == 0:
    M += 1
a = 0
while True:
    a = (rng.getrandbits(127) | 1)
    if gcd(a, M) == 1:
        break

A = [ (a*wi) % M for wi in w ]

plaintext = b"fwectf{REDACTED_REDACTED_REDACT}"
print(len(plaintext) % 8 )
assert len(plaintext) % 8 == 0
C = []
for i in range(0, len(plaintext), 8):
    bits = bytes_to_bits_be(plaintext[i:i+8])
    S = sum(ai*xi for ai, xi in zip(A, bits))
    C.append(S)

print("")
print(f"P = {A}")
print(f"C = {C}")