from src.sbox import compute_forward_sbox
from src.byte_matrix import ByteMatrix16

_KEY_SIZES = {16, 24, 32}
_ROUND_COUNT = {
    16: 11,
    24: 13,
    32: 15
}

def _l_word_rot(word: bytearray) -> bytearray:
    out = word[1:]
    out.append(word[0])
    return out

def _get_words(key_bytes: bytearray) -> list[bytearray]:
    words = []
    for idx in range(0, len(key_bytes), 4):
        words.append(key_bytes[idx : idx + 4])
    return words

def _word_xor(a: bytearray, b: bytearray) -> bytearray:
    out = bytearray(4)
    for i in range(4):
        out[i] = a[i] ^ b[i]
    return out

class KeySchedule:
    _RCON = {
        1: bytearray(b'\x01\x00\x00\x00'),
        2: bytearray(b'\x02\x00\x00\x00'),
        3: bytearray(b'\x04\x00\x00\x00'),
        4: bytearray(b'\x08\x00\x00\x00'),
        5: bytearray(b'\x10\x00\x00\x00'),
        6: bytearray(b'\x20\x00\x00\x00'),
        7: bytearray(b'\x40\x00\x00\x00'),
        8: bytearray(b'\x80\x00\x00\x00'),
        9: bytearray(b'\x1b\x00\x00\x00'),
        10: bytearray(b'\x36\x00\x00\x00')
    }
    _SBOX: list = None

    def __init__(self, key: str, sbox=None):

        self._SBOX = compute_forward_sbox() if sbox is None else sbox

        self.key_str = key

        key_bytes = bytearray(self.key_str, 'utf-8')
        self.key_size = len(key_bytes)
        if self.key_size not in _KEY_SIZES:
            raise ValueError(f'{type(self).__name__}: Incompatible key length')

        self.rounds = _ROUND_COUNT[self.key_size]
        self.key_words = _get_words(key_bytes)
        self.round_keys = self._generate_round_keys()

    def _sub_word(self, word: bytearray):
        out = bytearray()
        for i in word:
            out.append(self._SBOX[i])
        return out

    def _generate_round_keys(self) -> list[ByteMatrix16]:
        key_word_count = len(self.key_words)
        sub2_check = 4 % key_word_count
        expanded_words: list[bytearray] = []
        round_keys: list[ByteMatrix16] = []
        for round_num in range(0, self.rounds * 4, 4):
            round_words: bytearray = bytearray()
            for i in range(round_num, round_num + 4):
                if i < key_word_count:
                    word = self.key_words[i]
                elif i % key_word_count == 0:
                    g_word = self._sub_word(_l_word_rot(expanded_words[i - 1]))
                    word = _word_xor(_word_xor(expanded_words[i - key_word_count], g_word), self._RCON[i // key_word_count])
                elif key_word_count > 6 and i % key_word_count == sub2_check:
                    word = _word_xor(expanded_words[i - key_word_count], self._sub_word(expanded_words[i - 1]))
                else:
                    word = _word_xor(expanded_words[i - key_word_count], expanded_words[i - 1])
                print(f'iter {i}: {word=}')
                expanded_words.append(word)
                round_words += word

            round_keys.append(ByteMatrix16(round_words))

        return round_keys

if __name__ == "__main__":
    s = compute_forward_sbox()
    k = KeySchedule('sixteen chars :)')
    print(k.key_size)
    print(k.key_words)
    print(k.round_keys)