from src.galois_math import g_mul
from src.byte_matrix import ByteMatrix16

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

# Applies permutation to column. Matrix constants from https://en.wikipedia.org/wiki/Rijndael_MixColumns#Matrix_representation
def _mix_column(col: bytearray, inv=False) -> bytearray:
    # Get matrix constant
    mix = MIX_INVERSE if inv else MIX_FORWARD
    new = bytearray(4)
    # Multiply column bytes as coordinate vector with matrix, using Galois field
    for mix_row in range(4):
        res = 0
        for mix_col in range(4):
            res ^= g_mul(col[mix_col], mix[mix_row][mix_col])
        new[mix_row] = res
    return new

# MixColumns step; applies permutation to all columns in the state
def _mix_columns(state: ByteMatrix16) -> ByteMatrix16:
    res = ByteMatrix16()
    for idx, col in enumerate(state.columns()):
        res.set_column(idx, _mix_column(col))
    return res

# ShiftRows step; cyclically shifts rows to the left by increasing offset
def _shift_rows(state: ByteMatrix16) -> ByteMatrix16:
    res = ByteMatrix16()
    res.set_row(0, state.get_row(0))
    for idx, row in enumerate(state.rows(start=1)):
        offset = idx + 1
        new: bytearray = row[offset : 4] + row[0 : offset]
        res.set_row(offset, new)
    return res

# Main Rijndael class
class Rijndael:
    def __init__(self, plaintext: str):
        self.plaintext_bytes = str_to_byte_matrices(plaintext)
        self.state: ByteMatrix16 = self.plaintext_bytes[0]


if __name__ == '__main__':
    b = ByteMatrix16(bytearray('sixteen chars :)', 'utf-8'))
    ByteMatrix16._debug_show_chars = True
    print(b.str_long())
    print(_shift_rows(b).str_long())