# AES uses the Rijndael irreducible polynomial:
# x^8 + x^4 + x^3 + x + 1, represented as 0x11B.
IRREDUCIBLE_POLYNOMIAL = 0x11B

# Round constants used by the AES-128 key expansion.
RCON = [
    0x00, 0x01, 0x02, 0x04, 0x08,
    0x10, 0x20, 0x40, 0x80, 0x1B, 0x36
]
