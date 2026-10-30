"""Generate the standard AES S-box and inverse S-box mathematically."""

from aes.constants import IRREDUCIBLE_POLYNOMIAL


def gf_multiply(a: int, b: int) -> int:
    """Multiply two bytes in GF(2^8), reducing with polynomial 0x11B."""
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        if a & 0x100:
            a ^= IRREDUCIBLE_POLYNOMIAL
        b >>= 1
    return result & 0xFF


def gf_power(value: int, exponent: int) -> int:
    """Exponentiation in GF(2^8), using square-and-multiply."""
    result = 1
    while exponent:
        if exponent & 1:
            result = gf_multiply(result, value)
        value = gf_multiply(value, value)
        exponent >>= 1
    return result


def multiplicative_inverse(value: int) -> int:
    """Return the multiplicative inverse; zero maps to zero for AES."""
    return 0 if value == 0 else gf_power(value, 254)


def rotate_byte_left(value: int, shift: int) -> int:
    return ((value << shift) | (value >> (8 - shift))) & 0xFF


def affine_transform(value: int) -> int:
    """Apply the AES affine transformation to a GF(2^8) byte."""
    return (
        value
        ^ rotate_byte_left(value, 1)
        ^ rotate_byte_left(value, 2)
        ^ rotate_byte_left(value, 3)
        ^ rotate_byte_left(value, 4)
        ^ 0x63
    )


def generate_sbox() -> list[int]:
    """Generate all 256 entries of the standard AES substitution box."""
    return [
        affine_transform(multiplicative_inverse(byte))
        for byte in range(256)
    ]


SBOX = generate_sbox()
INV_SBOX = [0] * 256
for index, value in enumerate(SBOX):
    INV_SBOX[value] = index
