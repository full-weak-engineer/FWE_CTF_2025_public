from dataclasses import dataclass
from typing import List, Tuple, Optional
import random
from Crypto.Util.number import bytes_to_long, long_to_bytes

def _bitdeg(p: int) -> int:
    return p.bit_length() - 1

class GF2m:
    def __init__(self, m: int, mod_poly: Optional[int]=None):
        self.m = m
        if mod_poly is None:
            presets = {
                1: 0b11,      # x + 1
                2: 0b111,     # x^2 + x + 1
                3: 0b1011,    # x^3 + x + 1
                4: 0b10011,   # x^4 + x + 1
                5: 0b100101,  # x^5 + x^2 + 1
                8: 0x11B,     # x^8 + x^4 + x^3 + x + 1
            }
            if m not in presets:
                raise ValueError("Please specify mod_poly for this m")
            mod_poly = presets[m]
        if _bitdeg(mod_poly) != m:
            raise ValueError("mod_poly degree must equal m")
        self.mod_poly = mod_poly
        self.mask = (1<<m) - 1
    def add(self, a: int, b: int) -> int:
        return (a ^ b) & self.mask
    def mul(self, a: int, b: int) -> int:
        a &= self.mask; b &= self.mask
        res = 0
        while b:
            if b & 1:
                res ^= a
            b >>= 1
            a <<= 1
            if a & (1 << self.m):
                a ^= self.mod_poly
        return res & self.mask
    def pow(self, a: int, e: int) -> int:
        res, base, ee = 1, a & self.mask, e
        while ee:
            if ee & 1:
                res = self.mul(res, base)
            base = self.mul(base, base)
            ee >>= 1
        return res
    def inv(self, a: int) -> int:
        if a == 0:
            raise ZeroDivisionError("no inverse for 0")
        return self.pow(a, (1<<self.m)-2)

def mat_inv_K(M: List[List[int]], K: GF2m) -> List[List[int]]:
    n = len(M)
    A = [row[:] + [0]*n for row in M]
    for i in range(n):
        A[i][n+i] = 1
    r = 0
    for c in range(n):
        piv = None
        for i in range(r, n):
            if A[i][c] != 0:
                piv = i; break
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        if A[r][c] != 1:
            invp = K.inv(A[r][c])
            A[r] = [K.mul(x, invp) for x in A[r]]
        for i in range(n):
            if i == r: continue
            if A[i][c] != 0:
                f = A[i][c]
                A[i] = [K.add(A[i][j], K.mul(f, A[r][j])) for j in range(2*n)]
        r += 1
    if r < n:
        raise ValueError("singular matrix over K")
    return [row[n:] for row in A]

def mat_apply_K(M: List[List[int]], v: List[int], K: GF2m) -> List[int]:
    n = len(M)
    out = [0]*n
    for i in range(n):
        s = 0
        for j in range(n):
            if M[i][j]:
                s = K.add(s, K.mul(M[i][j], v[j]))
        out[i] = s
    return out

def rand_affine_bijection(n: int, K: GF2m, rng: random.Random):
    while True:
        M = [[rng.randrange(0, 1<<K.m) for _ in range(n)] for _ in range(n)]
        try:
            _ = mat_inv_K(M, K)
            break
        except ValueError:
            continue
    b = [rng.randrange(0, 1<<K.m) for _ in range(n)]
    return (M, b)

def affine_apply(Mb, v: List[int], K: GF2m) -> List[int]:
    M, b = Mb
    y = mat_apply_K(M, v, K)
    return [K.add(y[i], b[i]) for i in range(len(v))]

@dataclass
class ExtFieldSpec:
    K: GF2m
    n: int
    modulus: List[int]

class ExtElem:
    def __init__(self, spec: ExtFieldSpec, coeffs: Optional[List[int]]=None):
        self.S = spec
        self.K = spec.K
        self.n = spec.n
        if coeffs is None:
            self.c = [0]*self.n
        else:
            assert len(coeffs) == self.n
            self.c = [x & ((1<<self.K.m)-1) for x in coeffs]
    @staticmethod
    def one(S: ExtFieldSpec):
        c = [0]*S.n; c[0] = 1
        return ExtElem(S, c)
    def copy(self): return ExtElem(self.S, self.c[:])
    def add(self, other): return ExtElem(self.S, [self.K.add(a,b) for a,b in zip(self.c, other.c)])
    def mul(self, other):
        K=self.K; n=self.n; mod=self.S.modulus
        tmp=[0]*(2*n-1)
        for i,a in enumerate(self.c):
            if a==0: continue
            for j,b in enumerate(other.c):
                if b==0: continue
                tmp[i+j] = K.add(tmp[i+j], K.mul(a,b))
        for d in range(2*n-2, n-1, -1):
            coef = tmp[d]
            if coef == 0: continue
            for j in range(n):
                aj = mod[j]
                if aj != 0:
                    tmp[d-n+j] = K.add(tmp[d-n+j], K.mul(coef, aj))
            tmp[d] = 0
        return ExtElem(self.S, tmp[:n])
    def pow(self, e: int):
        res = ExtElem.one(self.S)
        base = self.copy()
        ee = e
        while ee:
            if ee & 1:
                res = res.mul(base)
            base = base.mul(base)
            ee >>= 1
        return res

def phi_encode(vec: List[int], S: ExtFieldSpec) -> ExtElem:
    assert len(vec) == S.n
    return ExtElem(S, vec[:])

def phi_decode(z: ExtElem) -> List[int]:
    return z.c[:]

@dataclass
class SecretStructure:
    K: GF2m
    n: int
    blocks: List[ExtFieldSpec]
    partition: List[int]
    ell_list: List[int]
    r_list: List[int]
    theta_list: List[int]
    e_list: List[int]
    s_forward: Tuple[List[List[int]], List[int]]
    t_forward: Tuple[List[List[int]], List[int]]

def _decompose_as_2ell_plus1_times_power_of_two(n: int):
    if n < 3: raise ValueError("n must be >= 3")
    r=0; m=n
    while m % 2 == 0:
        m//=2; r+=1
    if m % 2 == 0: raise ValueError("n is not (2*ell+1)*2^r")
    ell = (m - 1) // 2
    if (2*ell + 1) != m or ell < 1:
        raise ValueError("n is not (2*ell+1)*2^r")
    return ell, r

def _egcd(a,b):
    if b == 0: return (a,1,0)
    g,x1,y1 = _egcd(b, a % b)
    return (g, y1, x1 - (a//b)*y1)

def _modinv_int(a,m):
    g,x,_ = _egcd(a,m)
    if g != 1:
        raise ValueError("no modular inverse")
    return x % m

def build_theta_e_h_for_partition(K: GF2m, partition: List[int], b_list: Optional[List[int]]=None):
    q = 1 << K.m
    ell_list=[]; r_list=[]; theta_list=[]; e_list=[]; h_list=[]
    for idx, n_i in enumerate(partition):
        ell_i, r_i = _decompose_as_2ell_plus1_times_power_of_two(n_i)
        b_i = (b_list[idx] if b_list is not None else 1)
        if not (1 <= b_i <= ell_i):
            raise ValueError(f"b[{idx}] must be in [1, {ell_i}]")
        theta_i = b_i * (1 << r_i)
        e_i = 1 + (q ** theta_i)
        order = (q ** n_i) - 1
        h_i = _modinv_int(e_i, order)
        ell_list.append(ell_i); r_list.append(r_i); theta_list.append(theta_i)
        e_list.append(e_i); h_list.append(h_i)
    return ell_list, r_list, theta_list, e_list, h_list

def split_blocks(v: List[int], part: List[int]) -> List[List[int]]:
    out=[]; pos=0
    for ni in part:
        out.append(v[pos:pos+ni]); pos+=ni
    return out

def concat_blocks(chunks: List[List[int]]) -> List[int]:
    out=[]
    for c in chunks: out.extend(c)
    return out

def encrypt_public_map_F(xi: List[int], S: SecretStructure) -> List[int]:
    K = S.K
    u = affine_apply(S.s_forward, xi, K)
    blocks = split_blocks(u, S.partition)
    y_chunks = []
    for i, vec in enumerate(blocks):
        z = phi_encode(vec, S.blocks[i])
        z_e = z.pow(S.e_list[i])
        y = phi_decode(z_e)
        y_chunks.append(y)
    v = concat_blocks(y_chunks)
    return affine_apply(S.t_forward, v, K)

def setup_secret_general(seed: int, m: int, partition: List[int], modulus_list: List[List[int]], b_list: Optional[List[int]]=None) -> SecretStructure:
    rng = random.Random(seed)
    K = GF2m(m)
    n = sum(partition)
    blocks=[]
    for ni, mod in zip(partition, modulus_list):
        if len(mod) != ni+1 or mod[-1] != 1:
            raise ValueError("Each modulus must have length n_i+1 and end with 1")
        blocks.append(ExtFieldSpec(K=K, n=ni, modulus=mod))
    ells, rs, thetas, es, _hs = build_theta_e_h_for_partition(K, partition, b_list=b_list)
    s_fwd = rand_affine_bijection(n, K, rng)
    t_fwd = rand_affine_bijection(n, K, rng)
    return SecretStructure(K, n, blocks, partition, ells, rs, thetas, es, s_fwd, t_fwd)

def _int_to_bits_fixed(x: int, Lbits: int) -> list[int]:
    return [ (x >> (Lbits-1-i)) & 1 for i in range(Lbits) ]

def _bits_to_int(bits: list[int]) -> int:
    x = 0
    for b in bits: x = (x<<1) | (b & 1)
    return x

def bytes_to_K_elems_general(bs: bytes, K: GF2m, n: int) -> tuple[list[int], int]:
    m = K.m
    total = 8 * len(bs)
    block_bits = m * n
    pad_bits = (-total) % block_bits
    Lbits = total + pad_bits
    x = bytes_to_long(bs)
    bits = _int_to_bits_fixed(x, total) + [0]*pad_bits
    elems = []
    for i in range(0, Lbits, m):
        val = 0
        for j in range(m):
            val = (val << 1) | bits[i+j]
        elems.append(val & ((1<<m)-1))
    return elems, pad_bits

def encrypt_bytes_general(plain: bytes, S: SecretStructure) -> tuple[list[int], int]:
    K = S.K; n = S.n
    elems, pad_bits = bytes_to_K_elems_general(plain, K, n)
    out = []
    for i in range(0, len(elems), n):
        xi = elems[i:i+n]
        eta = encrypt_public_map_F(xi, S)
        out.extend(eta)
    return out, pad_bits

def ct_elems_to_hex(ct_elems: list[int], pad_bits: int, K: GF2m) -> str:
    m = K.m
    elem_count = len(ct_elems)
    if not (0 <= pad_bits < (1 << 32)): raise ValueError("pad_bits out of range (32-bit)")
    if not (0 <= elem_count < (1 << 32)): raise ValueError("elem_count out of range (32-bit)")
    payload_bits = []
    for a in ct_elems:
        v = a & ((1<<m)-1)
        payload_bits.extend([ (v >> (m-1-j)) & 1 for j in range(m) ])
    Lbits = elem_count * m
    payload_int = _bits_to_int(payload_bits)
    Lbytes = (Lbits + 7)//8
    payload_bytes = long_to_bytes(payload_int, blocksize=Lbytes)
    header = (elem_count).to_bytes(4, "big") + (pad_bits).to_bytes(4, "big")
    return (header + payload_bytes).hex()

def encrypt_to_hex_packed(plain: bytes, S: SecretStructure) -> str:
    ct_elems, pad_bits = encrypt_bytes_general(plain, S)
    return ct_elems_to_hex(ct_elems, pad_bits, S.K)