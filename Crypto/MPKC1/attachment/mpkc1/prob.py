from core_lib import make_sample, make_flag, z_vector_from_t, ensure_full_rank, write_public_txt
import random

SEED         = 3141592
N            = 31

OUT_PATH     = "public.txt"

def load_plains_and_flag(path: str):
    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.rstrip("\n") for ln in f]
    items = [ln for ln in lines if ln.strip() != ""]
    if len(items) < 2:
        raise ValueError("Need at least one sample line and one flag line in plain.txt")
    flag = items[-1]
    plains = items[:-1]
    return plains, flag

def main():
    rng = random.Random(SEED)
    t_secret = [rng.getrandbits(1) for _ in range(N)]
    Z = z_vector_from_t(t_secret)
    plains, flag = load_plains_and_flag("plain.txt")
    samples = []
    for s in plains:
        print(s)
        samp = make_sample(s.encode("utf-8"), N, rng, Z)
        samples.append(samp)

    flag = make_flag(flag.encode("utf-8"), N, rng, Z)

    write_public_txt(OUT_PATH, N, samples, flag)
    print(f"[+] wrote {OUT_PATH}  (N={N}, samples={len(samples)})")

if __name__ == "__main__":
    main()
