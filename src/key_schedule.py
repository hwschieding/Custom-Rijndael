from src.sbox import compute_forward_sbox
from src.byte_matrix import ByteMatrix16

# Constants for acceptable key sizes and round keys
_KEY_SIZES = {16, 24, 32}
_ROUND_COUNT = {
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

# Converts array to list of int32s that key expansion can operate on
def _get_words(key_bytes: bytearray) -> list[int]:
    words = []
    for idx in range(0, len(key_bytes), 4):
        words.append(_array_to_num32(key_bytes[idx : idx + 4]))
    return words

class KeySchedule:
    _SBOX: list = None

    def __init__(self, key: str | bytearray, sbox=None):

        # Get precalculated S-Box from user if provided
        self._SBOX = compute_forward_sbox() if (self._SBOX is None) and (sbox is None) else sbox

        self.key_str = key.decode('utf-8') if isinstance(key, bytearray) else key
        key_bytes = bytearray(key, 'utf-8') if isinstance(key, str) else key

        self.key_size = len(key_bytes)
        if self.key_size not in _KEY_SIZES:
            # Key must be 16, 24, or 32 bytes
            raise ValueError(f'{type(self).__name__}: Incompatible key length')

        self.rounds = _ROUND_COUNT[self.key_size]
        self.key_words = _get_words(key_bytes)

        # Key expansion
        self.round_keys = self._generate_round_keys()

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
        key_word_count = len(self.key_words)
        sub2_check = 4 % key_word_count
        expanded_words: list[int] = [] # "Words" are int32s
        round_keys: list[ByteMatrix16] = [] # Round keys stored as byte matrices
        # 4 words for each round, creating 16 byte keys
        for round_num in range(0, self.rounds * 4, 4):
            round_words: bytearray = bytearray()
            for i in range(round_num, round_num + 4):
                # Operation derived from https://en.wikipedia.org/wiki/AES_key_schedule#The_key_schedule
                if i < key_word_count:
                    word = self.key_words[i]
                elif i % key_word_count == 0:
                    g_word = self._sub_word(_l_rot32(expanded_words[i - 1]))
                    word = expanded_words[i - key_word_count] ^ g_word ^ _RCON[i // key_word_count]
                elif key_word_count > 6 and i % key_word_count == sub2_check:
                    word = expanded_words[i - key_word_count] ^ self._sub_word(expanded_words[i - 1])
                else:
                    word = expanded_words[i - key_word_count] ^ expanded_words[i - 1]
                # print(f'iter {i}: {word=}, {hex(word)=}')
                expanded_words.append(word)
                round_words += _num32_to_array(word)

            #Every 4 words generated, create new 16 byte round key
            round_keys.append(ByteMatrix16(round_words))

        return round_keys
