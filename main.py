# CSI 106 S25
# Hunter Schieding 5/7/25
# Independent Study Spring 2025
from src.sbox import compute_forward_sbox, compute_inverse_sbox
from src.tk_window import RijndaelGui
from src.byte_matrix import ByteMatrix16
from ctypes import windll

if __name__ == "__main__":
    # EXTRA SETTINGS
    ByteMatrix16._debug_show_chars = False # Set to true to show character representations in debug text
    windll.shcore.SetProcessDpiAwareness(1) # Fixes blurriness of Tkinter window on high-res monitors; however sometimes
        # causes window to be too small.

    # GUI
    RijndaelGui(sbox=compute_forward_sbox(), i_sbox=compute_inverse_sbox())