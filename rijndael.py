def galois_mul(a:int, b:int) -> int:
    product = 0
    while a and b:
        print(f'{a=}, {bin(a)}')
        print(f'{b=}, {bin(b)}')
        if b & 1:
            product ^= a # Polynomial addition
        b >>= 1 # Discard 0th term
        carry = a & 128
        a <<= 1 # Multiply polynomial by x
        if carry:
            print('executed')
            a ^= 0x11b # Irreducible polynomial constant
    return product

def find_g_inverse(a):
    for i in range(1, 256):
        if galois_mul(a, i) == 1:
            return i

if __name__ == "__main__":

    print(galois_mul(0xf3, 0xba))

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