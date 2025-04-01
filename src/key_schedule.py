from src.sbox import compute_forward_sbox

def _l_word_rot(word: bytearray) -> None:
    byte0 = word.pop(0)
    word.append(byte0)

def _get_words(key_bytes: bytearray) -> list[bytearray]:
    words = []
    for idx in range(0, len(key_bytes), 4):
        words.append(key_bytes[idx : idx + 4])
    return words

class KeySchedule:
    _RCON = {1: 0x01, 2: 0x02, 3:0x04, 4: 0x08, 5: 0x10, 6: 0x20, 7: 0x40, 8: 0x80, 9: 0x1b, 10: 0x36}
    _KEY_SIZES = {128, 192, 256}
    _SBOX = None

    def __init__(self, key: str):
        self.key_str = key
        key_bytes = bytearray(self.key_str, 'utf-8')
        if len(key_bytes) not in self._KEY_SIZES:
            raise ValueError(f'{type(self).__name__}: Incompatible key length')
        self.words = _get_words(key_bytes)