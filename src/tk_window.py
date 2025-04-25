from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from os import path
from src.key_schedule import _KEY_ROUND_SIZES
from src.rijndael import Rijndael

class PlaintextInput:
    def __init__(self, master):
        self.main_frame = ttk.Frame(master, padding=(0, 10, 0, 10))
        ttk.Label(self.main_frame, text="Plaintext file (*.txt, etc)").grid(row=0, column=0, sticky=W)
        self.input_frame = ttk.Frame(self.main_frame)

        self.user_file = ""
        self.file_browse = ttk.Button(self.input_frame, text="Browse File", command=self.select_file)
        self.file_lbl = ttk.Label(self.input_frame, text=self._get_file_label())

        self.file_browse.grid(row=0, column=0, sticky=W)
        self.file_lbl.grid(row=0, column=1, sticky=W)
        self.input_frame.grid(row=1,column=0, sticky=W)

    def grid(self, row=0, column=0):
        self.main_frame.grid(row=row, column=column, sticky=W)

    def select_file(self):
        self.user_file = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
        self.file_lbl.config(text=self._get_file_label())

    def _get_file_label(self) -> str:
        return "No file selected" if self.user_file == "" else self.user_file

class KeyInput:
    def __init__(self, master):
        self.main_frame = ttk.Frame(master, padding=(0, 10, 0, 10))

        # Main Frame
        self.lbl = ttk.Label(self.main_frame, text="Encryption/Decryption Key")
        self.lbl.grid(row=0, column=0, sticky=W)
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.grid(row=1, column=0)

        # Input Frame
        self.decoding = StringVar()
        self.user_entry = StringVar()
        self.user_entry.trace('w', lambda name, index, mode, ue=self.user_entry: self.validate_entry(ue))

        decoding_options = ("UTF-8", "HEX")
        self.dropdown = ttk.OptionMenu(self.input_frame, self.decoding, decoding_options[0], *decoding_options,
                                       command=lambda d: self.validate_entry(self.user_entry))
        self.key_entry = ttk.Entry(self.input_frame, textvariable=self.user_entry)
        self.warning = ttk.Label(self.input_frame, text='', foreground='red')

        self.dropdown.grid(row=0, column=0, sticky=W)
        self.key_entry.grid(row=0, column=1, sticky=W)
        self.warning.grid(row=1, column=1, sticky=W)

        self.ready = True

        self.validate_entry(self.user_entry)

    def grid(self, row=0, column=0):
        self.main_frame.grid(row=row, column=column, sticky=W)

    def validate_entry(self, ue):
        # print('callback')
        # print(self.decoding.get())
        def status(s, message=''):
            self.warning.config(text=message)
            self.ready=s

        user_str = ue.get()
        us_bytes = bytes(user_str.encode('utf-8'))

        if self.decoding.get() == "HEX":
            try:
                us_bytes = bytes.fromhex(user_str)
            except ValueError:
                status(False, "Invalid hex bytes")
                return

        if len(us_bytes) in _KEY_ROUND_SIZES:
            status(True)
        else:
            status(False, message=f'Invalid key length ({len(us_bytes)})')

class RijndaelGui:
    def __init__(self):
        self.root = Tk()
        self.main_frame = ttk.Frame(self.root, padding=(10, 10, 10, 10))
        self.main_frame.grid(row=0, column=0)
        ttk.Label(self.main_frame, text="AES Encryption Algorithm").grid(row=0, column=0, sticky=W)

        self.plaintext_input = PlaintextInput(self.main_frame)
        self.key_input = KeyInput(self.main_frame)
        self.encrypt_button = ttk.Button(self.main_frame, text="Encrypt", command=self.encrypt_press)

        self.plaintext_input.grid(row=1, column=0)
        self.key_input.grid(row=2, column=0)
        self.encrypt_button.grid(row=3, column=0)
        self.root.mainloop()

    def encrypt_press(self):
        r = Rijndael(self.key_input.user_entry.get())
        with open(self.plaintext_input.user_file, 'rb') as f:
            file_bytes = bytearray(f.read())
            print(r.encrypt(file_bytes))

if __name__ == '__main__':
    RijndaelGui()