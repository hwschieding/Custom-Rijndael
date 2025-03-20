# Code for generating the Rijndael substitution box

# TODO: Inverse S-Box generation
# TODO: Add option to use precomputed S-Box from file instead of generating one

from galois_math import find_galois_inverse

def l_rot8(a, bits) -> int:  # Circular shift left for bytes
    return ((a << bits) | (a >> (8 - bits))) & 0xFF

def affine_transform(a: int) -> int:
    return a ^ l_rot8(a, 1) ^ l_rot8(a, 2) ^ l_rot8(a, 3) ^ l_rot8(a, 4) ^ 0x63

def compute_table() -> list:
    checked = set()
    table = [0] * 256
    table[0] = 0x63
    for i in range(1, 256):
        if i not in checked:
            inverse = find_galois_inverse(i) # Because inverse(inverse) = i, we have found the inverse of two elements
            table[i], table[inverse] = affine_transform(inverse), affine_transform(i)
            checked.add(i)
            checked.add(inverse)
    return table

class SBox:
    def __init__(self):
        self.table = compute_table()
    def __getitem__(self, index):
        return self.table[index]