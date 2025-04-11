from src.galois_math import g_mul
from src.byte_matrix import ByteMatrix16
from src.state import State

# Matrix constants for MixColumns
MIX_FORWARD = [[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]]
MIX_INVERSE = [[14, 11, 13, 9], [9, 14, 11, 13], [13, 9, 14, 11], [11, 13, 9, 14]]

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
        self.state = State(self.plaintext_bytes[0])


if __name__ == '__main__':
    b = State(bytearray('sixteen chars :)', 'utf-8'))
    ByteMatrix16._debug_show_chars = True
    print(b.str_long())
    b.shift_rows()
    print(b.str_long())