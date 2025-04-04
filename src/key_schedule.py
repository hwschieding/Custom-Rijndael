from src.sbox import compute_forward_sbox
from src.byte_matrix import ByteMatrix16

# Constants for acceptable key sizes and round keys
_KEY_ROUND_SIZES = {
    16: 11,
    24: 13,
    32: 15
}
_RCON = {
    1: 0x01000000,
    2: 0x02000000,
    3: 0x04000000,
    4: 0x08000000,
    5: 0x10000000,
    6: 0x20000000,
    7: 0x40000000,
    8: 0x80000000,
    9: 0x1b000000,
    10: 0x36000000
}

# One byte left circular shift for int32s
def _l_rot32(x: int) -> int:
    return ((x << 8) | (x >> 24)) & 0xFFFFFFFF

# Converts 4 element bytearray to int32
def _array_to_num32(x: bytearray) -> int:
    out = 0
    for n in x: # Add byte then shift result by one byte
        out += n
        out <<= 8
    return out >> 8 # Reverse last shift from the loop

# Converts int32 to 4 element bytearray
def _num32_to_array(x: int) -> bytearray:
    out = bytearray()
    mask = 0xFF000000
    for i in range(3, -1, -1):
        # Use mask to get each byte from num, then shift to be byte sized
        out.append((x & mask) >> (i * 8))
        mask >>= 8 # Shift mask to next byte
    return out

class KeySchedule:
    _SBOX: list = None

    def __init__(self, key: str | bytearray, sbox=None):

        # Get precalculated S-Box from user if needed & provided
        if self._SBOX is None:
            self._SBOX = compute_forward_sbox() if sbox is None else sbox

        self.key_bytes: bytearray = bytearray(key, 'utf-8') if isinstance(key, str) else key

        self.key_size = len(self.key_bytes)
        if self.key_size not in _KEY_ROUND_SIZES:
            # Key must be 16, 24, or 32 bytes
            raise ValueError(f'{type(self).__name__}: Incompatible key length')

        self.rounds = _KEY_ROUND_SIZES[self.key_size]
        self.key_words = self._get_words()

        # Key expansion
        self.round_keys = self._generate_round_keys()

    def __getitem__(self, idx):
        return self.round_keys[idx]

    def __repr__(self):
        return f"{type(self)}, {self.key_size=}, {self.key_bytes}"

    def print_keys(self):
        print(f'{self}\nRound keys: ')
        for i, n in enumerate(self.round_keys):
            print(f"Round {i}: {n}")

    # Converts array to list of int32s that key expansion can operate on
    def _get_words(self) -> list[int]:
        words = []
        for idx in range(0, len(self.key_bytes), 4):
            words.append(_array_to_num32(self.key_bytes[idx: idx + 4]))
        return words

    # Applies S-Box to each byte of an int32
    def _sub_word(self, word: int) -> int:
        out = 0
        for i in range(4):
            shift = i * 8
            mask = 0xFF << shift
            out += self._SBOX[(word & mask) >> shift] << shift
        return out

    # Performs key expansion; can use 128, 192 and 256-bit keys
    def _generate_round_keys(self) -> list[ByteMatrix16]:
        k_word_num = len(self.key_words)
        sub2_check = 4 % k_word_num
        words: list[int] = [] # "Words" are int32s
        round_keys: list[ByteMatrix16] = [] # Round keys stored as byte matrices
        # 4 words for each round, creating 16 byte keys
        for round_num in range(0, self.rounds * 4, 4):
            round_words: bytearray = bytearray()
            for i in range(round_num, round_num + 4):
                # Operation derived from https://en.wikipedia.org/wiki/AES_key_schedule#The_key_schedule
                if i < k_word_num:
                    word = self.key_words[i]
                elif i % k_word_num == 0:
                    g_word = self._sub_word(_l_rot32(words[i - 1]))
                    word = words[i - k_word_num] ^ g_word ^ _RCON[i // k_word_num]
                elif k_word_num > 6 and i % k_word_num == sub2_check:
                    word = words[i - k_word_num] ^ self._sub_word(words[i - 1])
                else:
                    word = words[i - k_word_num] ^ words[i - 1]
                # print(f'iter {i}: {word=}, {hex(word)=}')
                words.append(word)
                round_words += _num32_to_array(word)

            #Every 4 words generated, create new 16 byte round key
            round_keys.append(ByteMatrix16(round_words))

        return round_keys

if __name__ == '__main__':
    k = KeySchedule(bytearray(16))
    ByteMatrix16._debug_show_chars = True
    k.print_keys()