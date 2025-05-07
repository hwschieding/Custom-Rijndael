from src.byte_matrix import ByteMatrix16
from src.state import State
from src.key_schedule import KeySchedule
from src.sbox import compute_forward_sbox, compute_inverse_sbox

# Converts str into list of 4x4 byte matrices that can be operated on by AES
def array_to_states(text_bytes: bytearray, padding: bool=True) -> list[State]:
    mxs = []
    if padding:
        print('Padding text...')
        # Padding text to 16 bytes
        padding = 16 - (len(text_bytes) % 16)
        text_bytes += (bytearray(padding.to_bytes(1)) * padding)
    for chunk16_idx in range(0, len(text_bytes), 16): # Split plaintext to 16 byte blocks
        # Final block may be <16 bytes, remainder will be sized with null bytes on instantiation
        mx = State(text_bytes[chunk16_idx : chunk16_idx + 16])
        mxs.append(mx)
    return mxs

def states_to_array(mxs: list, remove_padding: bool=False) -> bytearray:
    text_bytes = bytearray()
    for state in mxs:
        text_bytes += state.data
    if remove_padding:
        print('Removing padding...')
        padding = text_bytes[-1]
        text_bytes = text_bytes[:-padding]
    return text_bytes

# Main Rijndael class
class Rijndael:
    _SBOX_FORWARD = None
    _SBOX_INVERSE = None
    def __init__(self, key: str | bytearray, sbox_f=None, sbox_i=None):
        self._SBOX_FORWARD = compute_forward_sbox() if sbox_f is None else sbox_f
        self._SBOX_INVERSE = compute_inverse_sbox() if sbox_i is None else sbox_i

        self.key = bytearray(key, 'utf-8') if isinstance(key, str) else key

        self.round_keys = KeySchedule(self.key, self._SBOX_FORWARD)

    # Full AES encryption as described at https://en.wikipedia.org/wiki/Advanced_Encryption_Standard#High-level_description_of_the_algorithm
    def encrypt(self, plaintext: str | bytearray, add_padding=True) -> bytearray:
        print(f"Beginning encryption with plaintext '{plaintext}' and key '{self.key}'")
        plaintext_states = array_to_states(bytearray(plaintext, 'utf-8') if isinstance(plaintext, str) else plaintext, padding=add_padding)
        encrypted_states = []
        # Operates on each 16 byte state "block" individually
        for plain_state in plaintext_states:
            print(f'[Encryption] Encrypting state {plain_state}')
            # Initialize state with key addition
            state = plain_state ^ self.round_keys[0]
            # 10-14 rounds based on key length
            for key_idx in range(1, len(self.round_keys) - 1):
                state.sub_bytes(self._SBOX_FORWARD)
                state.shift_rows()
                state.mix_columns()
                state ^= self.round_keys[key_idx]
                print(f'[Encryption] Round {key_idx}: {state}')
            # Final round (doesn't include MixColumns)
            state.sub_bytes(self._SBOX_FORWARD)
            state.shift_rows()
            state ^= self.round_keys[-1]
            print(f'[Encryption] Final Round ({len(self.round_keys) - 1}): {state}')
            encrypted_states.append(state)
        return states_to_array(encrypted_states)

    # Full AES decryption; identical to encryption except reversed + using inverse methods
    def decrypt(self, ciphertext: str | bytearray, remove_padding=True) -> bytearray:
        print(f"Beginning decryption with ciphertext '{ciphertext}' and key '{self.key}'")
        encrypted_states = array_to_states(bytearray(ciphertext, 'utf-8') if isinstance(ciphertext, str) else ciphertext, padding=False)
        decrypted_states = []
        for e_state in encrypted_states:
            print(f'[Decryption] Decrypting state {e_state}')
            state = e_state ^ self.round_keys[-1]
            state.shift_rows_inv()
            state.sub_bytes(self._SBOX_INVERSE)
            print(f'[Decryption] Round {len(self.round_keys) - 1}: {state}')
            for key_idx in range(len(self.round_keys) - 2, 0, -1):
                state ^= self.round_keys[key_idx]
                state.mix_columns_inv()
                state.shift_rows_inv()
                state.sub_bytes(self._SBOX_INVERSE)
                print(f'[Decryption] Round {key_idx}: {state}')
            state ^= self.round_keys[0]
            decrypted_states.append(state)
        return states_to_array(decrypted_states, remove_padding=remove_padding)

    def change_key(self, new_key: bytearray | str):
        self.key = bytearray(new_key, 'utf-8') if isinstance(new_key, str) else new_key
        self.round_keys = KeySchedule(self.key, self._SBOX_FORWARD)

if __name__ == '__main__':
    r = Rijndael(bytearray("0123456789abcdef", 'utf-8'))
    b = bytearray('Test words to encrypt:)', 'utf-8')
    e = r.encrypt(b)
    print(e)
    print(r.decrypt(e))

    # sbox_f = compute_forward_sbox()
    # sbox_i = compute_inverse_sbox()
    # '\x00\x00\x01\x01\x03\x03\x07\x07\x0f\x0f\x1f\x1f\x3f\x3f\x7f\x7f'
    # r = Rijndael('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', sbox_f, sbox_i)
    # e_r = r.encrypt('sixteen bytes :)')
    # print(e_r)
    # print()
    # print(r.decrypt(e_r))