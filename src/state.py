from src.byte_matrix import ByteMatrix16
from src.galois_math import g_mul

# Matrix constants for MixColumns
MIX_FORWARD = [[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]]
MIX_INVERSE = [[14, 11, 13, 9], [9, 14, 11, 13], [13, 9, 14, 11], [11, 13, 9, 14]]

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

# Byte matrix with methods for the AES state structure
class State(ByteMatrix16):
    def __init__(self, text_bytes:bytearray=bytearray(16)):
        super().__init__(text_bytes)

    def __xor__(self, other):
        res = bytearray(0)
        for i, n in enumerate(self.data):
            res.append(n ^ other.data[i])
        return State(res)

    def sub_bytes(self, sbox: list):
        for i in range(16):
            self.data[i] = sbox[self.data[i]]

    # MixColumns step; applies permutation to all columns in the state
    def mix_columns(self):
        for idx, col in enumerate(self.columns()):
            self.set_column(idx, _mix_column(col))

    # Inverse of MixColumns
    def mix_columns_inv(self):
        for idx, col in enumerate(self.columns()):
            self.set_column(idx, _mix_column(col, inv=True))

    # ShiftRows step; cyclically shifts rows to the left by increasing offset
    def shift_rows(self):
        for idx, row in enumerate(self.rows(start=1)):
            offset = idx + 1
            new: bytearray = row[offset:] + row[:offset]
            self.set_row(offset, new)

    # ShiftRows inverse
    def shift_rows_inv(self):
        for idx, row in enumerate(self.rows(start=1)):
            offset = 3 - idx
            new: bytearray = row[offset:] + row[:offset]
            self.set_row(idx + 1, new)
