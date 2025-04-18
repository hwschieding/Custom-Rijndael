from src.byte_matrix import ByteMatrix16
from src.state import State
from src.key_schedule import KeySchedule
from src.sbox import compute_forward_sbox, compute_inverse_sbox

# Converts str into list of 4x4 byte matrices that can be operated on by AES
def str_to_byte_matrices(text: str) -> list[State]:
    text_bytes = bytearray(text, 'utf-8')
    mxs = []
    for chunk16_idx in range(0, len(text_bytes), 16): # Split plaintext to 16 byte blocks
        # Final block may be <16 bytes, remainder will be sized with null bytes on instantiation
        mx = State(text_bytes[chunk16_idx : chunk16_idx + 16])
        mxs.append(mx)
    return mxs

# Main Rijndael class
class Rijndael:
    _SBOX_FORWARD = None
    _SBOX_INVERSE = None
    def __init__(self, plaintext: str, key: str, sbox_f=None, sbox_i=None):
        self._SBOX_FORWARD = compute_forward_sbox() if sbox_f is None else sbox_f
        self._SBOX_INVERSE = compute_inverse_sbox() if sbox_i is None else sbox_i

        self.plaintext = plaintext
        self.key = key

        self.plaintext_bytes = str_to_byte_matrices(plaintext)
        self.round_keys = KeySchedule(key, self._SBOX_FORWARD)

    # Full AES encryption as described at https://en.wikipedia.org/wiki/Advanced_Encryption_Standard#High-level_description_of_the_algorithm
    def encrypt(self):
        encrypted_states = []
        # Operates on each 16 byte state "block" individually
        for plain_state in self.plaintext_bytes:
            # Initialize state with key addition
            state = plain_state ^ self.round_keys[0]
            # 10-14 rounds based on key length
            for key_idx in range(1, len(self.round_keys) - 1):
                state.sub_bytes(self._SBOX_FORWARD)
                state.shift_rows()
                state.mix_columns()
                state ^= self.round_keys[key_idx]
            # Final round (doesn't include MixColumns)
            state.sub_bytes(self._SBOX_FORWARD)
            state.shift_rows()
            state ^= self.round_keys[-1]
            encrypted_states.append(state)
        return encrypted_states

    # Full AES decryption; identical to encryption except reversed + using inverse methods
    def decrypt(self, encrypted_states):
        decrypted_states = []
        for e_state in encrypted_states:
            state = e_state ^ self.round_keys[-1]
            state.shift_rows_inv()
            state.sub_bytes(self._SBOX_INVERSE)
            for key_idx in range(len(self.round_keys) - 2, 0, -1):
                state ^= self.round_keys[key_idx]
                state.mix_columns_inv()
                state.shift_rows_inv()
                state.sub_bytes(self._SBOX_INVERSE)
            state ^= self.round_keys[0]
            decrypted_states.append(state)
        return decrypted_states

    def change_plaintext(self, new_plaintext):
        self.plaintext = new_plaintext
        self.plaintext_bytes = str_to_byte_matrices(new_plaintext)

    def change_key(self, new_key: str):
        self.key = new_key
        self.round_keys = KeySchedule(new_key, self._SBOX_FORWARD)


if __name__ == '__main__':
    sbox_f = compute_forward_sbox()
    sbox_i = compute_inverse_sbox()
    # '\x00\x00\x01\x01\x03\x03\x07\x07\x0f\x0f\x1f\x1f\x3f\x3f\x7f\x7f'
    r = Rijndael('sixteen bytes :)', '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', sbox_f, sbox_i)
    e_r = r.encrypt()
    print(e_r)
    print()
    print(r.decrypt(e_r))