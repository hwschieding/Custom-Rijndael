# Handles mathematical operations in the Galois Finite Field ( GF(2^8) )

# Multiplication
# Algorithm found at https://en.wikipedia.org/wiki/Finite_field_arithmetic#Rijndael's_(AES)_finite_field
def g_mul(a:int, b:int) -> int:
    a &= 0xFF
    b &= 0xFF
    product = 0
    while a and b:
        if b & 1:
            product ^= a # Polynomial addition
        b >>= 1 # Discard 0th term
        carry = a & 0x80
        a = (a << 1) & 0xFF # Multiply polynomial by x, bitwise AND by 0b11111111 masking to 8 bits
        if carry:
            a ^= 0x1b # Irreducible polynomial constant
    return product

def find_galois_inverse(a: int) -> int: # Brute force method, checks every element in GF(2^8)
    for i in range(1, 256):
        if g_mul(a, i) == 1:
            return i
    # If there is no return, a is either 0 or outside GF(2^8).
    raise ValueError(f"{find_galois_inverse.__name__}: '{a}' out of range (1 - 255)")