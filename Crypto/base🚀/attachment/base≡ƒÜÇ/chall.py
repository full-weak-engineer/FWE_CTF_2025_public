#!/usr/bin/env python🚀

with open('emoji.txt', 'r', encoding='utf-8') as f:
    emoji = list(f.read().strip())

table = {i: ch for i, ch in enumerate(emoji)}

def encode(data):
    bits = ''.join(f'{b:08b}' for b in data)
    pad = (-len(bits)) % 10
    bits += '0' * pad
    out = [table[int(bits[i:i+10], 2)] for i in range(0, len(bits), 10)]
    r = (-len(out)) % 4
    if r:
        out.extend('🚀' * r)
    return ''.join(out)

if __name__ == '__main__':
    msg = 'Hello!'
    enc = encode(msg.encode())
    print('msg:', msg)
    print('enc:', enc)
