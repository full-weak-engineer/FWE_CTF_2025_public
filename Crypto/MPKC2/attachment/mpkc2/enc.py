from core_lib import setup_secret_general, encrypt_to_hex_packed

SEED       = 20250829
M          = 8
PARTITION  = [7]
BLIST      = [3]
MODULI     = [[1,1,0,0,0,0,0,1]]
PLAINTEXT  = b"fwectf{uooooooooooooooooooooooooooooooo!!!!!!!!!!!!!!!!!!!}"

def main():
    S = setup_secret_general(SEED, M, PARTITION, MODULI, b_list=BLIST)
    ct_hex = encrypt_to_hex_packed(PLAINTEXT, S)
    print(ct_hex)

if __name__ == "__main__":
    main()