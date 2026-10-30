"""AES-128 single-block encryption and decryption implementation."""

from aes.key_expansion import expand_key
from aes.sbox import SBOX, INV_SBOX
from aes.transformations import (
    add_round_key, sub_bytes, shift_rows, inv_shift_rows,
    mix_columns, inv_mix_columns,
)


def bytes_to_state(block: bytes) -> list[list[int]]:
    if len(block) != 16:
        raise ValueError("AES operates on exactly one 16-byte block.")
    return [[block[row + 4 * column] for column in range(4)]
            for row in range(4)]


def state_to_bytes(state: list[list[int]]) -> bytes:
    return bytes(state[row][column]
                 for column in range(4) for row in range(4))


def encrypt_block(plaintext: bytes, key: bytes) -> bytes:
    """Encrypt exactly one 16-byte block with a 16-byte AES-128 key."""
    round_keys = expand_key(key)
    state = bytes_to_state(plaintext)

    add_round_key(state, round_keys[0])

    for round_number in range(1, 10):
        sub_bytes(state, SBOX)
        shift_rows(state)
        mix_columns(state)
        add_round_key(state, round_keys[round_number])

    # Final round omits MixColumns.
    sub_bytes(state, SBOX)
    shift_rows(state)
    add_round_key(state, round_keys[10])

    return state_to_bytes(state)


def decrypt_block(ciphertext: bytes, key: bytes) -> bytes:
    """Decrypt exactly one 16-byte block with a 16-byte AES-128 key."""
    round_keys = expand_key(key)
    state = bytes_to_state(ciphertext)

    add_round_key(state, round_keys[10])

    for round_number in range(9, 0, -1):
        inv_shift_rows(state)
        sub_bytes(state, INV_SBOX)
        add_round_key(state, round_keys[round_number])
        inv_mix_columns(state)

    inv_shift_rows(state)
    sub_bytes(state, INV_SBOX)
    add_round_key(state, round_keys[0])

    return state_to_bytes(state)
