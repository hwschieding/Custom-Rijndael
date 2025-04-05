from src.galois_math import galois_mul
from src.byte_matrix import ByteMatrix16

# Converts str into list of 4x4 byte matrices that can be operated on by AES
def str_to_byte_matrices(text: str) -> list:
    text_bytes = bytearray(text, 'utf-8')
    mxs = []
    for chunk16_idx in range(0, len(text_bytes), 16): # Split plaintext to 16 byte blocks
        # Final block may be <16 bytes, remainder will be sized with null bytes on instantiation
        mx = ByteMatrix16(text_bytes[chunk16_idx : chunk16_idx + 16])
        mxs.append(mx)
    return mxs

# Main Rijndael class
class Rijndael:
    def __init__(self, plaintext: str):
        self.plaintext_bytes = str_to_byte_matrices(plaintext)

if __name__ == '__main__':
    txt = 'sixteen chars :)'
    print(str_to_byte_matrices(txt))