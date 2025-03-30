from sbox import compute_forward_sbox, compute_inverse_sbox

if __name__ == "__main__":
    # Temp code for testing S-Box
    s = compute_forward_sbox()
    i_s = compute_inverse_sbox()
    print(s)
    print(i_s)