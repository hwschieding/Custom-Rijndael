"""
Datatype for a 4x4 matrix of bytes in order to more easily perform matrix operations on bytes.
Stored internally as a simple 16 element bytearray for memory efficiency, with methods to handle
getting and setting rows/columns/elements.

AES converts the plaintext input into **COLUMN-MAJOR ORDER** matrices, in other words:
'0123456789abcdef' ->
    0 4 8 c
    1 5 9 d
    2 6 a e
    3 7 b f

This does have an effect on how some AES functions operate in Python, so row/column based
functions have to be "backwards" to accommodate this behavior.
"""
class ByteMatrix16:

    _debug_show_chars = False

    def __init__(self, text_bytes: bytearray):
        self.data = text_bytes
        # Ensure text is 16 bytes
        bytes_len = len(self.data)
        if bytes_len > 16:
            raise ValueError(f'{type(self).__name__}: Input must be 16 bytes or less')
        elif bytes_len < 16:
            self._size_text(16 - bytes_len)

    def __getitem__(self, item) -> bytearray:
        return self.get_row(item)

    def __repr__(self) -> str:
        out = ''.join(f'{" " if i % 4 == 0 else ""}{n:02x}' for i, n in enumerate(self.data))
        return f'{type(self)},{out}, {self.data=}'

    def get_row(self, idx: int) -> bytearray:
        return bytearray((self.data[idx],
                          self.data[idx + 4],
                          self.data[idx + 8],
                          self.data[idx + 12]))

    def get_column(self, idx: int) -> bytearray:
        row_idx = idx * 4
        return self.data[row_idx : row_idx + 4]

    def set_row(self, idx: int, new_row: bytearray | str) -> None:
        if isinstance(new_row, str):
            new_row = bytearray(new_row, 'utf-8')
        for i in range(4):
            self.data[idx + (i * 4)] = new_row[i]

    def set_column(self, idx: int, new_col: bytearray | str) -> None:
        if isinstance(new_col, str):
            new_col = bytearray(new_col, 'utf-8')
        row_idx = idx * 4
        self.data[row_idx : row_idx + 4] = new_col

    def str_long(self):
        out = 'Matrix contents: '
        for i in range(4):
            row = ' '.join([chr(n) if self._debug_show_chars else f'{n:02x}' for n in self.get_row(i)])
            out += row + '\n'
        return out

    def _size_text(self, remain: int):
        self.data.extend(('\x00' * remain).encode('utf-8'))
