from sbox import SBox

if __name__ == "__main__":
    # Temp code for testing S-Box
    s = SBox()
    i_s = SBox(inverse=True)
    for i in range(0, 256, 16):
        print([f'{hex(n):4}' for n in s[i:i+16]])
    print()
    for i in range(0, 256, 16):
        print([f'{hex(n):4}' for n in i_s[i:i+16]])