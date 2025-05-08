# Code for generating the Rijndael substitution box

from src.galois_math import find_galois_inverse

def l_rot8(a, bits) -> int:  # Circular shift left for bytes
    return ((a << bits) | (a >> (8 - bits))) & 0xFF

# Following two functions are derived from algorithms found at https://en.wikipedia.org/wiki/Rijndael_S-box
def affine_transform(a: int) -> int:
    return a ^ l_rot8(a, 1) ^ l_rot8(a, 2) ^ l_rot8(a, 3) ^ l_rot8(a, 4) ^ 0x63

def inverse_affine_transform(s: int) -> int:
    return l_rot8(s, 1) ^ l_rot8(s, 3) ^ l_rot8(s, 6) ^ 0x5

def compute_forward_sbox() -> list:
    checked = set()
    table = [0] * 256
    table[0] = 0x63 # Special case for 0 because it has no inverse
    for i in range(1, 256):
        if i not in checked:
            inverse = find_galois_inverse(i) # Because inverse(inverse) = i, we have found the inverse of two elements
            table[i], table[inverse] = affine_transform(inverse), affine_transform(i)
            checked.add(i)
            checked.add(inverse)
    return table

def compute_inverse_sbox() -> list:
    table = [0] * 256
    table[0x63] = 0 # Special case for 0, reversed
    for i in range(0, 256):
        if i != 0x63:
            inv_affine = inverse_affine_transform(i)
            table[i] = find_galois_inverse(inv_affine)
    return table