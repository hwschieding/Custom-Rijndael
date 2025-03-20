from sbox import SBox

if __name__ == "__main__":

    s = SBox()
    print()
    for i in range(0, 256, 16):
        print([hex(n) for n in s[i:i+16]])

