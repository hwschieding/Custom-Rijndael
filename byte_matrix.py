"""
Datatype for a 4x4 matrix of bytes in order to more easily perform matrix operations on bytes.
Stored internally as a simple 16 element bytearray for memory efficiency, with methods to handle
getting and setting rows/columns/elements.
"""
class ByteMatrix16:
    def _size_text(self, remain: int):
        self.data.extend(('\x00' * remain).encode('utf-8'))

    def __init__(self, text_bytes: bytearray):
        self.data = text_bytes
        # Ensure text is 16 bytes
        bytes_len = len(self.data)
        if bytes_len > 16:
            raise ValueError(f'{type(self).__name__}: Input must be 16 bytes or less')
        elif bytes_len < 16:
            self._size_text(16 - bytes_len)


    def __repr__(self):
        out = f'{type(self)}, {self.data=}\n'
        for i in range(0, 16, 4):
            row = ' '.join([f'{n:02x}' for n in self.data[i : i + 4]])
            out += row + '\n'
        return out

    def get_row(self, idx: int) -> bytearray:
        row_idx = idx * 4
        return self.data[row_idx : row_idx + 4]

    def get_column(self, idx: int) -> bytearray:
        return bytearray((self.data[idx],
                          self.data[idx + 4],
                          self.data[idx + 8],
                          self.data[idx + 12]))

    def __getitem__(self, item) -> bytearray:
        return self.get_row(item)

    def set_row(self, idx: int, new_row: bytearray | str):
        if isinstance(new_row, str):
            new_row = bytearray(new_row, 'utf-8')
        row_idx = idx * 4
        self.data[row_idx : row_idx + 4] = new_row

    def set_column(self, idx: int, new_col: bytearray | str):
        if isinstance(new_col, str):
            new_col = bytearray(new_col, 'utf-8')
        for i in range(4):
            self.data[idx + (i * 4)] = new_col[i]