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
        a = (a << 1) & 255 # Multiply polynomial by x, bitwise AND by 11111111 masking to 8 bits
        if carry:
            a ^= 0x1b # Irreducible polynomial constant
    return product

def find_g_inverse(a):
    for i in range(1, 256):
        if galois_mul(a, i) == 1:
            return i

if __name__ == "__main__":

    print(galois_mul(0x53, 0xCA))
    
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
