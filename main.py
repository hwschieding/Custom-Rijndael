# CSI 106 S25
# Hunter Schieding 3/31/25
# Independent Study Spring 2025

from sbox import compute_forward_sbox, compute_inverse_sbox
from galois_math import *
from byte_matrix import ByteMatrix16
from rijndael import Rijndael

if __name__ == "__main__":
    print(f'{'*' * 67}\nAES Implementation - Week 1 | Showcase of working functions/classes\n{'*' * 67}\n')
    input('Press enter to continue...')
    print('Galois field arithmetic functions: Functions to do arithmetic in the finite field GF(2^8)')
    user_num1 = int(input('Enter an 8-bit integer (0-255): '))
    user_num2 = int(input('Enter another 8-bit integer (0-255): '))
    print(f'{user_num1} * {user_num2} in GF(2^8):\n\t{galois_mul(user_num1, user_num2)=:#04x}')
    user_num3 = int(input('Enter a non-zero 8-bit integer: (1-255): '))
    print(f'Find multiplicative inverse of {user_num3} in GF(2^8):\n\t{find_galois_inverse(user_num3)=:#04x}')
    input('Press enter to continue...')
    print(f'\n{'*' * 67}\n')
    print("SBox table computation: Computation of Rijndael's static substitution box & it's inverse")
    print(f"Forward box:\n\t{compute_forward_sbox()=}")
    print(f"Inverse box:\n\t{compute_inverse_sbox()=}")
    input('Press enter to continue...')
    print(f'\n{'*' * 67}\n')
    print('ByteMatrix16 class to convert bytearray input to column-major order matrix with several functions')
    user_str1 = input('Enter a *16 BYTE OR LESS* string (leave blank for default): ')
    if len(user_str1) == 0: user_str1 = 'sixteen chars :)'
    print(f"\tb = ByteMatrix16(bytearray('{user_str1}', 'utf-8'))")
    b = ByteMatrix16(bytearray(user_str1, 'utf-8'))
    ByteMatrix16._debug_show_chars = True
    print(f'{b=}')
    print(f'\t{b.get_row(0)=}')
    print(f'\t{b.get_column(0)=}')
    print(f'\t{b.set_row(3, 'test')=}')
    print(f'\t{b.set_column(3, 'test')=}')
    print(f'\n{b=}')
    input('Press enter to continue...')
    print(f'\n{'*' * 67}\n')
    print('Finally, small beginnings of the main Rijndael class. Converts input plaintext to list of byte matrices')
    user_str2 = input("Enter a string (leave blank for default): ")
    if len(user_str2) == 0: user_str2 = 'Very long string with lots and lots of words'
    print(f"\tr = Rijndael('{user_str2}')")
    r = Rijndael(user_str2)
    print(f'\t{r.plaintext_bytes=}')
    print('\nEnd')