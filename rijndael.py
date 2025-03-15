def l_rot8(a, bits): # Circular shift left for bytes
    return ((a << bits)|(a >> (8 - bits))) & 0xFF

def galois_mul(a:int, b:int) -> int:
    a &= 255
    b &= 255
    product = 0
    while a and b:
        # print(f'{a=}, {bin(a)}')
        # print(f'{b=}, {bin(b)}')
        if b & 1:
            product ^= a # Polynomial addition
        b >>= 1 # Discard 0th term
        carry = a & 128
        a = (a << 1) & 255 # Multiply polynomial by x, bitwise AND by 0b11111111 masking to 8 bits
        if carry:
            a ^= 0x1b # Irreducible polynomial constant
    return product

def find_galois_inverse(a: int) -> int: # Brute force method, checks every element in GF(2^8)
    for i in range(1, 256):
        if galois_mul(a, i) == 1:
            return i

def affine_transform(a: int) -> int:
    return a ^ l_rot8(a, 1) ^ l_rot8(a, 2) ^ l_rot8(a, 3) ^ l_rot8(a, 4) ^ 0x63

if __name__ == "__main__":

    #print(galois_mul(0x53, 0xCA))

    inv = find_galois_inverse(0x7a)
    print(bin(inv))
    affine = affine_transform(inv)
    print(hex(affine))
    print(bin(affine))
    
    '''
    checked = set()
    inverses = {1: 1}
    for i in range(2, 256):
        if i not in checked:
            print(f'checking {i}')
            inv = find_g_inverse(i)
            print(f'inverse found {inv}')
            checked.add(i)
            checked.add(inv)
            inverses[i], inverses[inv] = inv, i
    print(inverses)
    print(len(inverses))'
    '''
