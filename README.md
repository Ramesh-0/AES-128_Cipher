# AES-128 Encryption and Decryption (From Scratch)

A Python implementation of **AES-128** for learning and experimentation. It implements the AES algorithm directly, including mathematical generation of the standard AES S-box and inverse S-box. It does not call a third-party cryptography package.

> **Educational scope:** this project encrypts and decrypts one 128-bit block (16 bytes) using a 128-bit key. It is a learning implementation, not a production-ready encryption tool.

## 1. Features

- AES-128 encryption and decryption.
- Standard AES S-box generated from the GF(2^8) multiplicative inverse and affine transformation.
- Inverse S-box generated from the forward S-box.
- AES-128 key expansion (44 words / 11 round keys).
- Separate modules for the AES core, S-box, key schedule, transformations, constants, and file handling.
- Reads the key and plaintext from one input file.
- Writes ciphertext and decrypted plaintext to an output file.
- Checks that decryption recovers the original plaintext.

## 2. Project structure

```text
AES_Project/
├── main.py
├── input/
│   └── input.txt
├── aes/
│   ├── __init__.py
│   ├── aes_core.py
│   ├── constants.py
│   ├── key_expansion.py
│   ├── sbox.py
│   └── transformations.py
├── utils/
│   ├── __init__.py
│   └── file_handler.py
├── output/
│   └── .gitkeep
├── requirements.txt
└── README.md
```

### File responsibilities

| File | Responsibility |
|---|---|
| `main.py` | Coordinates input, encryption, decryption, verification, and output |
| `input/input.txt` | Holds the AES key and plaintext in hexadecimal |
| `aes/sbox.py` | Generates the standard AES S-box and inverse S-box |
| `aes/key_expansion.py` | Generates the 11 AES-128 round keys |
| `aes/transformations.py` | Implements SubBytes, ShiftRows, MixColumns, and their inverses |
| `aes/aes_core.py` | Implements the complete AES-128 block encryption/decryption flow |
| `aes/constants.py` | Stores the field polynomial and round constants |
| `utils/file_handler.py` | Parses the input file and writes the output file |
| `output/output.txt` | Generated encryption/decryption results |

## 3. Requirements

- Python 3.9 or later
- No external Python packages

Check your Python installation:

```bash
python --version
```

## 4. Input format

Open `input/input.txt` and provide:

```text
KEY=000102030405060708090A0B0C0D0E0F
PLAINTEXT=00112233445566778899AABBCCDDEEFF
```

Rules:

- `KEY` must be exactly 32 hexadecimal characters (16 bytes).
- `PLAINTEXT` must be exactly 32 hexadecimal characters (16 bytes).
- Hexadecimal input is case-insensitive.
- Spaces around values are ignored; spaces within a hexadecimal value are also removed.
- Lines beginning with `#` are treated as comments.
- The current implementation accepts one block only.

The included values are the standard AES-128 known-answer test vector.

## 5. Run the project

From the project root directory (`AES_Project`), run:

```bash
python main.py
```

The program will:

1. Read `KEY` and `PLAINTEXT` from `input/input.txt`.
2. Expand the 128-bit key into 11 round keys.
3. Encrypt the 16-byte plaintext.
4. Decrypt the resulting ciphertext.
5. Compare the decrypted block with the original plaintext.
6. Print the result and save it to `output/output.txt`.

Do not run `main.py` from inside the `aes` or `utils` directory. Run it from the project root so the package imports resolve correctly.

## 6. Expected result

For the included test vector, the expected ciphertext is:

```text
69C4E0D86A7B0430D8CDB78070B4C55A
```

Expected console output:

```text
========== AES-128 ENCRYPTION ==========
Key:        000102030405060708090A0B0C0D0E0F
Plaintext:  00112233445566778899AABBCCDDEEFF
Ciphertext: 69C4E0D86A7B0430D8CDB78070B4C55A

========== AES-128 DECRYPTION ==========
Ciphertext:          69C4E0D86A7B0430D8CDB78070B4C55A
Decrypted plaintext: 00112233445566778899AABBCCDDEEFF

Verification: SUCCESS
```

The output is also saved in `output/output.txt`.

## 7. AES-128 algorithm overview

AES-128 operates on a 128-bit (16-byte) data block and a 128-bit key. The 16-byte input is arranged into a 4 × 4 byte state matrix in column-major order.

### Encryption

1. **Initial AddRoundKey:** XOR the state with round key 0.
2. **Rounds 1–9:**
   - SubBytes: substitute each byte using the AES S-box.
   - ShiftRows: cyclically shift state rows by 0, 1, 2, and 3 bytes.
   - MixColumns: transform each column using matrix multiplication in GF(2^8).
   - AddRoundKey: XOR with the corresponding round key.
3. **Final round (round 10):** SubBytes, ShiftRows, and AddRoundKey. MixColumns is omitted.

### Decryption

Decryption applies the inverse transformations in reverse round order:

- InvShiftRows
- InvSubBytes
- AddRoundKey
- InvMixColumns

The final inverse round omits InvMixColumns.

## 8. How the original AES S-box is generated

The S-box is not loaded from a hard-coded lookup table. It is constructed for every possible byte value:

1. Find the multiplicative inverse in GF(2^8). The zero byte maps to zero for this construction.
2. Use the AES irreducible polynomial:

   `x^8 + x^4 + x^3 + x + 1`

   Its hexadecimal representation is `0x11B`.
3. Apply the AES affine transformation:

   `S(x) = b ^ ROTL1(b) ^ ROTL2(b) ^ ROTL3(b) ^ ROTL4(b) ^ 0x63`

   where `b` is the multiplicative inverse and `ROTLn` is an 8-bit left rotation by `n` positions.
4. Build the inverse S-box by reversing the mapping.

The generated S-box is the standard AES S-box. For a quick sanity check, its first entries are:

```text
63 7C 77 7B F2 6B 6F C5
30 01 67 2B FE D7 AB 76
```

## 9. AES-128 key expansion

AES-128 expands the original 16-byte key into 44 words, each 4 bytes long. Every group of four words forms one 16-byte round key, giving 11 round keys in total (round 0 through round 10).

The key schedule uses:

- RotWord
- SubWord (using the generated AES S-box)
- Rcon
- XOR with the word four positions earlier

## 10. Validation and troubleshooting

| Problem | What to check |
|---|---|
| `Input file not found` | Run the program from the project root and confirm `input/input.txt` exists |
| Invalid hexadecimal input | Use only hexadecimal characters `0–9`, `A–F` |
| Key length error | Provide exactly 32 hexadecimal characters |
| Plaintext length error | Provide exactly 32 hexadecimal characters |
| Import error | Confirm the `aes/` and `utils/` directories contain `__init__.py` and run `python main.py` from the root |

A successful run should print `Verification: SUCCESS`.

## 11. Important security limitations

This project is intended for education and cryptographic experimentation.

- It implements a single-block AES primitive, not a complete file-encryption system.
- It does not implement a mode of operation such as CBC or GCM.
- It does not use authenticated encryption or provide integrity protection.
- It does not implement padding.
- It is not designed to resist timing or other side-channel attacks.
- The example key is a public test vector and must never be used to protect real data.

For real applications, use a vetted cryptographic library and an authenticated encryption mode such as AES-GCM, with secure key generation and management.

## 12. Possible future extensions

- Support multiple blocks.
- Add PKCS#7 padding where an appropriate block mode requires it.
- Implement CBC and CTR modes for learning.
- Add AES-GCM through a vetted library for practical authenticated encryption.
- Add unit tests for each AES transformation and key expansion.
- Add round-by-round state tracing for cryptanalysis experiments.
- Compare the generated S-box and intermediate values against published AES test vectors.

## 13. Reference

- NIST, **FIPS 197: Advanced Encryption Standard (AES)**: https://doi.org/10.6028/NIST.FIPS.197
