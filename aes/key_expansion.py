"""AES-128 key expansion: 16-byte key -> 11 round keys."""

from aes.constants import RCON
from aes.sbox import SBOX


def xor_words(a: list[int], b: list[int]) -> list[int]:
    return [x ^ y for x, y in zip(a, b)]


def rot_word(word: list[int]) -> list[int]:
    return word[1:] + word[:1]


def sub_word(word: list[int]) -> list[int]:
    return [SBOX[byte] for byte in word]


def expand_key(key: bytes) -> list[list[int]]:
    if len(key) != 16:
        raise ValueError("AES-128 requires a 16-byte (32-hex-character) key.")

    words = [list(key[i:i + 4]) for i in range(0, 16, 4)]

    for i in range(4, 44):
        temp = words[i - 1].copy()
        if i % 4 == 0:
            temp = sub_word(rot_word(temp))
            temp[0] ^= RCON[i // 4]
        words.append(xor_words(words[i - 4], temp))

    return [
        sum(words[round_index * 4:(round_index + 1) * 4], [])
        for round_index in range(11)
    ]
