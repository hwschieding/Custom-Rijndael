# Main Rijndael Class

from galois_math import galois_mul, find_galois_inverse
from sbox import SBox

#Generates a 4x4 byte matrix from a 16 byte string using a list of bytearrays. May become its own class.
def byte_matrix16(str16: str) -> list[bytearray]:
    mx = []
    for idx in range(0, 16, 4):
        mx.append(bytearray(str16[idx: idx + 4], 'utf-8'))
    return mx

# Converts str into list of matrices that can be operated on by AES
def str_to_byte_matrices(text: str) -> list:
    remain = len(text) % 16
    sized_text = text + ('\x00' * remain) # size text to multiple of 16 bytes

    mxs = []
    for chunk16_idx in range(0, len(sized_text), 16): # convert 16 byte chunks to byte matrices
        text_chunk16 = sized_text[chunk16_idx : chunk16_idx + 16]
        mxs.append(byte_matrix16(text_chunk16))
    return mxs

class Rijndael:

    def __init__(self, plaintext: str):
        self.plaintext_bytes = str_to_byte_matrices(plaintext)

if __name__ == '__main__':
    print(str_to_byte_matrices('sixteen chars :)'))