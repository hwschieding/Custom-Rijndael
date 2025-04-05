# CSI 106 S25
# Hunter Schieding 3/31/25
# Independent Study Spring 2025

from src.key_schedule import KeySchedule

if __name__ == "__main__":
    print(f'{'*' * 67}\nAES Implementation - Week 2 | Showcase of new KeySchedule class\n{'*' * 67}\n')
    key_accepted = False
    while not key_accepted:
        user_key = input('Enter 16 / 24 / 32-*BYTE* string (leave blank for default): ')
        user_key = 'sixteen chars :)' if len(user_key) == 0 else user_key
        try:
            k = KeySchedule(user_key)
            print('k = KeySchedule(user_key)')
            key_accepted = True
        except ValueError as err:
            print(f'{err} -- Try again')
    print(f"{k.print_keys()}")