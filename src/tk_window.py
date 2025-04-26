from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from ctypes import windll
import os
from src.key_schedule import _KEY_ROUND_SIZES
from src.rijndael import Rijndael

OUT_DIR = os.path.dirname(__file__)
ENCRYPT_OUT = os.path.join(OUT_DIR, 'encrypt_out.txt')
DECRYPT_OUT = os.path.join(OUT_DIR, 'decrypt_out.txt')

def validate_extension(ext):
    if ext == '':
        return False
    else:
        return True if ext[0] == '.' else False

class ActionInput:
    def __init__(self, master, func, label_txt, button_txt):
        self.main_frame = ttk.Frame(master, padding=(10, 10, 10, 10))
        ttk.Label(self.main_frame, text=label_txt).grid(row=0, column=0, sticky=W)
        self.input_frame = ttk.Frame(self.main_frame, padding=(0, 0, 0, 15))

        self.user_file = ""
        self.file_browse = ttk.Button(self.input_frame, text="Browse File", command=self.select_file)
        self.file_lbl = ttk.Label(self.input_frame, text=self._get_file_label())
        self.file_browse.grid(row=0, column=0, sticky=W)
        self.file_lbl.grid(row=0, column=1, sticky=W)

        self.action_frame = ttk.Frame(self.main_frame)
        extension_validate_command = self.action_frame.register(validate_extension)
        self.encrypt_button = ttk.Button(self.action_frame, text=button_txt, command=func)
        self.extension_options = ttk.Combobox(self.action_frame, values=(".txt", ".docx"), width=6, validate='key',
                                              validatecommand=(extension_validate_command, '%P'))
        self.extension_options.current(0)
        self.encrypt_button.grid(row=0, column=0)
        self.extension_options.grid(row=0, column=1)

        self.message = ttk.Label(self.main_frame, text="")

        self.input_frame.grid(row=1,column=0, sticky=W)
        self.action_frame.grid(row=2, column=0)
        self.message.grid(row=3, column=0)

    def grid(self, row=0, column=0):
        self.main_frame.grid(row=row, column=column, sticky=W)

    def select_file(self):
        self.user_file = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
        self.file_lbl.config(text=self._get_file_label())

    def _get_file_label(self) -> str:
        return "No file selected" if self.user_file == "" else os.path.basename(self.user_file)

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
        self.key_entry = ttk.Entry(self.input_frame, textvariable=self.user_entry, width=32)
        self.warning = ttk.Label(self.input_frame, text='', foreground='red')

        self.dropdown.grid(row=0, column=0, sticky=W)
        self.key_entry.grid(row=0, column=1, sticky=W)
        self.warning.grid(row=1, column=1, sticky=W)

        self.ready = True

        self.key = None
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
        us_bytes = bytearray(user_str.encode('utf-8'))

        if self.decoding.get() == "HEX":
            try:
                us_bytes = bytearray.fromhex(user_str)
            except ValueError:
                status(False, "Invalid hex bytes")
                return

        if len(us_bytes) in _KEY_ROUND_SIZES:
            status(True)
            self.key = us_bytes
        else:
            status(False, message=f'Invalid key length ({len(us_bytes)})')

class RijndaelGui:
    def __init__(self):
        self.root = Tk()
        windll.shcore.SetProcessDpiAwareness(1)
        self.main_frame = ttk.Frame(self.root, padding=(10, 10, 10, 10))
        self.main_frame.grid(row=0, column=0)
        ttk.Label(self.main_frame, text="AES Encryption Algorithm").grid(row=0, column=0, sticky=W)


        self.key_input = KeyInput(self.main_frame)
        self.key_input.grid(row=1, column=0)

        self.notebook = ttk.Notebook(self.main_frame)

        # Encrypt frame
        self.plaintext_input = ActionInput(self.notebook,
                                           func=lambda : self.start_AES(
                                                  'e',
                                                  self.plaintext_input,
                                                  ENCRYPT_OUT
                                              ),
                                           label_txt="Plaintext file (*.txt, etc)",
                                           button_txt='Encrypt'
                                           )

        self.plaintext_input.grid(row=0, column=0)

        # Decrypt frame
        self.ciphertext_input = ActionInput(self.notebook,
                                            lambda : self.start_AES(
                                                'd',
                                                self.ciphertext_input,
                                                DECRYPT_OUT
                                            ),
                                            label_txt="Ciphertext file (*.txt, etc)",
                                            button_txt="Decrypt"
                                            )

        self.ciphertext_input.grid(row=0, column=0)

        self.notebook.add(self.plaintext_input.main_frame, text="Encryption")
        self.notebook.add(self.ciphertext_input.main_frame, text="Decryption")
        self.notebook.grid(row=2, column=0, sticky=W)
        self.root.mainloop()

    def start_AES(self, mode: str, text_input, out_file):
        extension = text_input.extension_options.get()
        if len(extension) < 2 or (not extension[1:].isalnum()):
            text_input.message.config(text=f'Invalid extension ({extension})', foreground='red')
            return
        if not self.key_input.ready:
            text_input.message.config(text='Invalid key', foreground='red')
            return
        if not os.path.exists(text_input.user_file):
            text_input.message.config(text='Invalid file selected', foreground='red')
            return
        try:
            r = Rijndael(self.key_input.key)
            with open(text_input.user_file, 'rb') as f_in, open(out_file, 'wb') as f_out:
                input_bytes = bytearray(f_in.read())
                post_action_bytes = r.encrypt(input_bytes) if mode == 'e' else r.decrypt(input_bytes)
                f_out.write(post_action_bytes)
            text_input.message.config(text=f'{"Cipher" if mode == 'e' else "Plain"}text outputted to {out_file}',
                                      foreground='black'
                                      )
        except Exception as e:
            text_input.message.config(text=f'Something went wrong ({e})', foreground='red')


if __name__ == '__main__':
    RijndaelGui()
    # print(os.path.dirname(__file__))