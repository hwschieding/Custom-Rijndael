import galois

GF = galois.GF(2**8)

print(GF(0x53) * GF(0xCA))
print(0x53 * 0xCA)