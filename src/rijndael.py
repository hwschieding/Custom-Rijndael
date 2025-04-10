from src.galois_math import g_mul
from src.byte_matrix import ByteMatrix16

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

def _mix_column(col: bytearray, inv=False) -> bytearray:
    mix = MIX_INVERSE if inv else MIX_FORWARD
    new = bytearray(4)
    for b in range(4):
        new[b] = g_mul(col[0], mix[b][0]) ^ g_mul(col[1], mix[b][1]) ^ g_mul(col[2], mix[b][2]) ^ g_mul(col[3], mix[b][3])
    return new

# Main Rijndael class
class Rijndael:
    def __init__(self, plaintext: str):
        self.plaintext_bytes = str_to_byte_matrices(plaintext)
        self.state: ByteMatrix16 = self.plaintext_bytes[0]

    def shift_rows(self):
        for row in range(1, 4):
            offset = row
            old = self.state.get_row(row)
            new: bytearray = old[offset : 4] + old[0 : offset]
            self.state.set_row(row, new)



if __name__ == '__main__':
    a = bytearray(b'\x63\x47\xa2\xf0')
    b = _mix_column(a)
    print(bytes(a).hex())
    print(bytes(b).hex())
    print(bytes(_mix_column(b, inv=True)).hex())