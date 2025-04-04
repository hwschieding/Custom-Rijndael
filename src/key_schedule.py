from src.sbox import compute_forward_sbox
from src.byte_matrix import ByteMatrix16

_KEY_SIZES = {16, 24, 32}
_ROUND_COUNT = {
    16: 11,
    24: 13,
    32: 15
}

def _l_rot32(x: int) -> int:
    return ((x << 8) | (x >> 24)) & 0xFFFFFFFF

def _array_to_num32(x: bytearray) -> int:
    out = 0
    for n in x:
        out += n
        out <<= 8
    return out >> 8

def _num32_to_array(x: int) -> bytearray:
    out = bytearray()
    mask = 0xFF000000
    for i in range(3, -1, -1):
        out.append((x & mask) >> (i * 8))
        mask >>= 8
    return out

def _get_words(key_bytes: bytearray) -> list[int]:
    words = []
    for idx in range(0, len(key_bytes), 4):
        words.append(_array_to_num32(key_bytes[idx : idx + 4]))
    return words

class KeySchedule:
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
    _SBOX: list = None

    def __init__(self, key: str | bytearray, sbox=None):

        self._SBOX = compute_forward_sbox() if sbox is None else sbox

        self.key_str = key
        key_bytes = bytearray(self.key_str, 'utf-8') if isinstance(key, str) else key

        self.key_size = len(key_bytes)
        if self.key_size not in _KEY_SIZES:
            raise ValueError(f'{type(self).__name__}: Incompatible key length')

        self.rounds = _ROUND_COUNT[self.key_size]
        self.key_words = _get_words(key_bytes)
        self.round_keys = self._generate_round_keys()

    def _sub_word(self, word: int) -> int:
        out = 0
        for i in range(4):
            shift = i * 8
            mask = 0xFF << shift
            out += self._SBOX[(word & mask) >> shift] << shift
        return out

    def _generate_round_keys(self) -> list[ByteMatrix16]:
        key_word_count = len(self.key_words)
        sub2_check = 4 % key_word_count
        expanded_words: list[int] = []
        round_keys: list[ByteMatrix16] = []
        for round_num in range(0, self.rounds * 4, 4):
            round_words: bytearray = bytearray()
            for i in range(round_num, round_num + 4):
                if i < key_word_count:
                    word = self.key_words[i]
                elif i % key_word_count == 0:
                    g_word = self._sub_word(_l_rot32(expanded_words[i - 1]))
                    word = expanded_words[i - key_word_count] ^ g_word ^ self._RCON[i // key_word_count]
                elif key_word_count > 6 and i % key_word_count == sub2_check:
                    word = expanded_words[i - key_word_count] ^ self._sub_word(expanded_words[i - 1])
                else:
                    word = expanded_words[i - key_word_count] ^ expanded_words[i - 1]
                print(f'iter {i}: {word=}, {hex(word)=}')
                expanded_words.append(word)
                round_words += _num32_to_array(word)

            round_keys.append(ByteMatrix16(round_words))

        return round_keys


if __name__ == "__main__":
    s = compute_forward_sbox()
    b = bytearray('sixteen chars :)', 'utf-8')
    k = KeySchedule(bytearray(32), sbox=s)
    for i in range(0, len(b), 4):
        for n in b[i : i + 4]:
            print(f'{n:02x}', end='')
        print(' ', end='')
