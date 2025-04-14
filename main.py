# CSI 106 S25
# Hunter Schieding 4/14/25
# Independent Study Spring 2025

from src.state import State

if __name__ == "__main__":
    border_line = '*' * 67
    print(f'{border_line}\nAES Implementation - Week 3 | Showcase of new state class & ShiftRows and MixColumns funcs\n{border_line}\n')
    if input("Type 'y' to show unicode characters in matrix representations, leave blank for hex bytes: ").lower() == 'y':
        State._debug_show_chars = True
    print('\nState class - derived from ByteMatrix16 to handle more specific functions of the AES state')
    user_state = None
    while user_state is None:
        try:
            user_str = input('Enter 16-BYTE or less string to be used for state: (leave blank for default): ')
            user_str = 'sixteen chars :)' if user_str == "" else user_str
            user_state = State(bytearray(user_str, 'utf-8'))
        except ValueError as e:
            print(f'{e}. Try again')
    print(f'\nuser_state == {user_state}\n')
    print(f'ShiftRows & MixColumns - Functions that act as the main source of diffusion in AES')
    print(f'Starting state:\n{user_state.str_long()}')
    user_state.shift_rows()
    print(f'After user_state.shift_rows():\n{user_state.str_long()}')
    user_state.mix_columns()
    print(f'After user_state.mix_columns():\n{user_state.str_long()}')
    input('Press Enter to continue...')
    print('Reverse functions for ShiftRows & MixColumns exist for decryption')
    user_state.mix_columns_inv()
    print(f'After user_state.mix_columns_inv():\n{user_state.str_long()}')
    user_state.shift_rows_inv()
    print(f'After user_state.shift_rows_inv():\n{user_state.str_long()}')
    input('End')