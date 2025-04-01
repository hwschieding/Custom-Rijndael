# CSI 106 S25
# Hunter Schieding 3/31/25
# Independent Study Spring 2025

from sbox import compute_forward_sbox, compute_inverse_sbox
from galois_math import *
from byte_matrix import ByteMatrix16
from rijndael import Rijndael

if __name__ == "__main__":
    print(f'{'*' * 67}\nAES Implementation - Week 1 | Showcase of working functions/classes\n{'*' * 67}\n')
    print('Galois field arithmetic functions: Functions to do arithmetic in the finite field GF(2^8)')
    print(f'Multiply 0x57 and 0x83 in GF(2^8):\n\t{galois_mul(0x57, 0x13)=:#02X}')
    print(f'Find multiplicative inverse of 0x53 in GF(2^8):\n\t{find_galois_inverse(0x53)=:#02X}')
    print(f'\n{'*' * 67}\n')
    print("SBox table computation: Computation of Rijndael's static substitution box & it's inverse")
    print(f"Forward box:\n\t{compute_forward_sbox()=}")
    print(f"Inverse box:\n\t{compute_inverse_sbox()=}")
    print(f'\n{'*' * 67}\n')
    print('ByteMatrix16 class to convert bytearray input to column-major order matrix with several functions')
    print("\tb = ByteMatrix16(bytearray('sixteen chars :)', 'utf-8'))")
    b = ByteMatrix16(bytearray('sixteen chars :)', 'utf-8'))
    ByteMatrix16._debug_show_chars = True
    print(f'{b=}')
    print(f'\t{b.get_row(0)=}')
    print(f'\t{b.get_column(0)=}')
    print(f'\t{b.set_row(3, 'test')=}')
    print(f'\t{b.set_column(3, 'test')=}')
    print(f'\n{b=}')
    print(f'\n{'*' * 67}\n')
    print('Finally, small beginnings of the main Rijndael class. Converts input plaintext to list of byte matrices')
    print("\tr = Rijndael('Very long string with lots and lots of words')")
    r = Rijndael('Very long string with lots and lots of words')
    print(f'\t{r.plaintext_bytes=}')
    print('\nEnd')