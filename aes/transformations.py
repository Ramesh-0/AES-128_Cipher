"""AES state transformations. State is a 4x4 column-major matrix."""


def add_round_key(state: list[list[int]], round_key: list[int]) -> None:
    for column in range(4):
        for row in range(4):
            state[row][column] ^= round_key[column * 4 + row]


def sub_bytes(state: list[list[int]], sbox: list[int]) -> None:
    for row in range(4):
        for column in range(4):
            state[row][column] = sbox[state[row][column]]


def shift_rows(state: list[list[int]]) -> None:
    for row in range(1, 4):
        state[row] = state[row][row:] + state[row][:row]


def inv_shift_rows(state: list[list[int]]) -> None:
    for row in range(1, 4):
        state[row] = state[row][-row:] + state[row][:-row]


def xtime(value: int) -> int:
    value <<= 1
    if value & 0x100:
        value ^= 0x11B
    return value & 0xFF


def gf_multiply(a: int, b: int) -> int:
    result = 0
    while b:
        if b & 1:
            result ^= a
        a = xtime(a)
        b >>= 1
    return result


def mix_columns(state: list[list[int]]) -> None:
    for c in range(4):
        a0, a1, a2, a3 = (state[r][c] for r in range(4))
        state[0][c] = gf_multiply(a0, 2) ^ gf_multiply(a1, 3) ^ a2 ^ a3
        state[1][c] = a0 ^ gf_multiply(a1, 2) ^ gf_multiply(a2, 3) ^ a3
        state[2][c] = a0 ^ a1 ^ gf_multiply(a2, 2) ^ gf_multiply(a3, 3)
        state[3][c] = gf_multiply(a0, 3) ^ a1 ^ a2 ^ gf_multiply(a3, 2)


def inv_mix_columns(state: list[list[int]]) -> None:
    for c in range(4):
        a0, a1, a2, a3 = (state[r][c] for r in range(4))
        state[0][c] = (gf_multiply(a0, 14) ^ gf_multiply(a1, 11)
                       ^ gf_multiply(a2, 13) ^ gf_multiply(a3, 9))
        state[1][c] = (gf_multiply(a0, 9) ^ gf_multiply(a1, 14)
                       ^ gf_multiply(a2, 11) ^ gf_multiply(a3, 13))
        state[2][c] = (gf_multiply(a0, 13) ^ gf_multiply(a1, 9)
                       ^ gf_multiply(a2, 14) ^ gf_multiply(a3, 11))
        state[3][c] = (gf_multiply(a0, 11) ^ gf_multiply(a1, 13)
                       ^ gf_multiply(a2, 9) ^ gf_multiply(a3, 14))
