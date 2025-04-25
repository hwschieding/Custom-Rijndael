# CSI 106 S25
# Hunter Schieding 4/21/25
# Independent Study Spring 2025

from src.rijndael import Rijndael
from src.byte_matrix import ByteMatrix16
from src.key_schedule import KeySchedule
from src.sbox import compute_forward_sbox, compute_inverse_sbox


if __name__ == "__main__":
    s_box_forward, s_box_inverse = compute_forward_sbox(), compute_inverse_sbox()
    border_line = '*' * 67
    print(f'{border_line}\nAES Implementation - Week 4 | AES Encryption and Decryption\n{border_line}\n')
    ByteMatrix16._debug_show_chars = input("Type 'y' to show UTF-8 character representations (hex otherwise): ") == 'y'
    print('\n*Note: text meant to be decrypted MUST be in hex format*')
    user_text = input("Enter text to be encrypted/decrypted: ")
    cipher_key = None
    while cipher_key is None:
        try:
            user_key = input('Enter key of byte length 16, 24, or 32: ')
            cipher_key = KeySchedule(user_key, s_box_forward)
        except Exception as e:
            print(f"{e}; try again")

    print(f'\nKey size: {cipher_key.key_size * 8}-bit')
    cipher = Rijndael(cipher_key, s_box_forward, s_box_inverse)
    user_choice = input("\nType 'e' for encryption, 'd' for decryption: ")
    if user_choice == 'e':
        cipher_text = cipher.encrypt(user_text)
        print(f'\nEncrypted ciphertext (hex format): {cipher_text}')
    if user_choice == 'd':
        plaintext = cipher.decrypt(user_text)
        print(f'\nDecrypted plaintext: {plaintext}')
    input()
