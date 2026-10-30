# AES-128 Encryption and Decryption (From Scratch)

A Python implementation of **AES-128** for learning and experimentation. The project implements AES directly, including mathematical generation of the standard AES S-box and inverse S-box. It does not use a third-party cryptography package.

> **Educational scope:** This project encrypts and decrypts one 128-bit block (16 bytes) using a 128-bit key. It is a learning implementation, not a production-ready encryption tool.

## 1. Features

- AES-128 encryption and decryption.
- Standard AES S-box generated from the GF(2^8) multiplicative inverse and affine transformation.
- Inverse S-box generated from the forward S-box.
- AES-128 key expansion (44 words / 11 round keys).
- Separate modules for the AES core, S-box, key schedule, transformations, and file handling.
- Reads the key and plaintext from one input file.
- Writes the latest ciphertext and decryption result to an output file.
- Verifies that decryption recovers the original plaintext.
- Includes a command to test the generated S-box.

## 2. Project structure

```text
AES_Project/
├── main.py                     # Runs encryption, decryption, and verification
├── input/
│   └── input.txt               # Your AES key and plaintext (hexadecimal)
├── aes/
│   ├── __init__.py
│   ├── aes_core.py             # AES-128 block encryption and decryption
│   ├── constants.py            # Field polynomial and round constants
│   ├── key_expansion.py        # Generates the 11 round keys
│   ├── sbox.py                 # Generates S-box and inverse S-box
│   └── transformations.py      # AES round transformations
├── utils/
│   ├── __init__.py
│   └── file_handler.py         # Reads input.txt and writes output.txt
├── output/
│   └── .gitkeep                # Keeps the output directory in Git
├── requirements.txt
└── README.md
```

### What each important file does

| File | Purpose |
|---|---|
| `main.py` | Reads input, calls AES encryption and decryption, prints results, and saves them |
| `input/input.txt` | The only file you need to edit to provide your own key and plaintext |
| `aes/sbox.py` | Generates the standard AES S-box and inverse S-box |
| `aes/key_expansion.py` | Expands the 16-byte key into 11 round keys |
| `aes/transformations.py` | Implements SubBytes, ShiftRows, MixColumns, and inverse transformations |
| `aes/aes_core.py` | Combines the transformations into AES-128 encryption and decryption |
| `utils/file_handler.py` | Parses the input file and writes the output file |
| `output/output.txt` | Automatically generated results from the most recent run |

## 3. Requirements and setup

- Python 3.9 or later
- No third-party Python packages are required.

Check your Python version:

```bash
python --version
```

Download or clone the repository, open the project root folder in a terminal, and run the program from that folder. For example:

```bash
cd AES_Project
python main.py
```

**Important:** Run `python main.py` from the project root (`AES_Project`), not from inside the `aes`, `utils`, `input`, or `output` folders. This ensures Python can resolve the package imports.

## 4. How to enter your own key and plaintext

Open `input/input.txt`. It contains two fields:

```text
KEY=000102030405060708090A0B0C0D0E0F
PLAINTEXT=00112233445566778899AABBCCDDEEFF
```

Replace the hexadecimal values after `=` with your own values:

```text
KEY=YOUR_32_HEXADECIMAL_CHARACTERS
PLAINTEXT=YOUR_32_HEXADECIMAL_CHARACTERS
```

The placeholders above are explanatory only; replace them with actual hexadecimal digits before running the program.

### Input rules

- `KEY` must be exactly **32 hexadecimal characters** (16 bytes / 128 bits).
- `PLAINTEXT` must be exactly **32 hexadecimal characters** (16 bytes / 128 bits).
- Allowed characters are `0–9`, `A–F`, and `a–f`.
- Do not include `0x` before the value.
- Do not put quotation marks around the values.
- The field names must be `KEY` and `PLAINTEXT`.
- Blank lines and lines starting with `#` are ignored.
- The program accepts one plaintext block at a time.

For example, this is a valid input file:

```text
# My AES-128 test
KEY=2B7E151628AED2A6ABF7158809CF4F3C
PLAINTEXT=6BC1BEE22E409F96E93D7E117393172A
```

Save `input/input.txt` after editing it.

**Key safety:** Use test keys only. Do not put passwords, production encryption keys, or confidential plaintext in a public GitHub repository. The included sample values are public test data.

## 5. How the output file works

You do not need to create or edit `output/output.txt` manually. When you run:

```bash
python main.py
```

the program:

1. Reads the current `KEY` and `PLAINTEXT` from `input/input.txt`.
2. Expands the key into 11 AES-128 round keys.
3. Encrypts the plaintext and calculates the ciphertext.
4. Decrypts that ciphertext using the same key.
5. Compares the decrypted plaintext with the original plaintext.
6. Prints the results in the terminal.
7. Writes the same results to `output/output.txt`.

### Does the output change every time?

**Yes. `output/output.txt` is overwritten on every successful run.** It contains the results of the most recent execution, not a history of previous executions.

- If you change the plaintext, the ciphertext will normally change.
- If you change the key, the ciphertext will normally change.
- If you keep both key and plaintext unchanged, this implementation produces the same ciphertext again because it encrypts a single block deterministically.
- The decrypted plaintext should match the input plaintext when encryption and decryption work correctly.

Example:

**First run — input**

```text
KEY=000102030405060708090A0B0C0D0E0F
PLAINTEXT=00112233445566778899AABBCCDDEEFF
```

**First run — output**

```text
Ciphertext: 69C4E0D86A7B0430D8CDB78070B4C55A
Decrypted plaintext: 00112233445566778899AABBCCDDEEFF
Verification: SUCCESS
```

**Second run — after changing the input**

```text
KEY=00000000000000000000000000000000
PLAINTEXT=00000000000000000000000000000000
```

**Second run — output**

```text
Ciphertext: 66E94BD4EF8A2C3B884CFA59CA342B2E
Decrypted plaintext: 00000000000000000000000000000000
Verification: SUCCESS
```

After the second run, `output/output.txt` contains the second run's results. The first run's output is replaced. Copy or rename the output file before running again if you want to preserve an earlier result.

## 6. Run the project

From the project root:

```bash
python main.py
```

The console displays the encryption and decryption results. The same report is saved to:

```text
output/output.txt
```

A successful run should end with:

```text
Verification: SUCCESS
```

If the input is missing or invalid, the program prints an error message explaining what needs to be corrected.

## 7. Test the AES S-box

The S-box is generated in `aes/sbox.py`; it is not loaded from a hard-coded lookup table. Run this command from the project root to inspect and validate it:

```bash
python -c "from aes.sbox import SBOX, INV_SBOX; print('S-box size:', len(SBOX)); print('First 16 S-box values:', ' '.join(f'{x:02X}' for x in SBOX[:16])); print('Inverse S-box size:', len(INV_SBOX)); print('Inverse mapping valid:', all(INV_SBOX[SBOX[i]] == i for i in range(256)))"
```

Expected output:

```text
S-box size: 256
First 16 S-box values: 63 7C 77 7B F2 6B 6F C5 30 01 67 2B FE D7 AB 76
Inverse S-box size: 256
Inverse mapping valid: True
```

What this test checks:

- The forward S-box has 256 entries, one for each possible byte.
- The first 16 values match the beginning of the standard AES S-box.
- The inverse S-box also has 256 entries.
- For every byte `i`, applying the forward S-box and then the inverse S-box returns the original byte: `INV_SBOX[SBOX[i]] == i`.

You can also open `aes/sbox.py` to study how the S-box is generated mathematically.

## 8. AES-128 algorithm overview

AES-128 operates on a 128-bit (16-byte) data block and a 128-bit key. The 16 input bytes are arranged into a 4 × 4 state matrix in column-major order.

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

## 9. How the original AES S-box is generated

The S-box is constructed for every possible byte value:

1. Find the multiplicative inverse in GF(2^8). Zero maps to zero for this construction.
2. Use the AES irreducible polynomial:

   `x^8 + x^4 + x^3 + x + 1`

   Its hexadecimal representation is `0x11B`.
3. Apply the AES affine transformation:

   `S(x) = b ^ ROTL1(b) ^ ROTL2(b) ^ ROTL3(b) ^ ROTL4(b) ^ 0x63`

   where `b` is the multiplicative inverse and `ROTLn` is an 8-bit left rotation by `n` positions.
4. Build the inverse S-box by reversing the mapping.

## 10. AES-128 key expansion

AES-128 expands the original 16-byte key into 44 words, each 4 bytes long. Every group of four words forms one 16-byte round key, giving 11 round keys in total (round 0 through round 10).

The key schedule uses:

- RotWord
- SubWord (using the generated AES S-box)
- Rcon
- XOR with the word four positions earlier

## 11. Validation and troubleshooting

| Problem | What to check |
|---|---|
| `Input file not found` | Run the program from the project root and confirm `input/input.txt` exists |
| Invalid hexadecimal input | Use only hexadecimal characters `0–9`, `A–F` |
| Key length error | Provide exactly 32 hexadecimal characters |
| Plaintext length error | Provide exactly 32 hexadecimal characters |
| Import error | Confirm `aes/` and `utils/` contain `__init__.py`; run `python main.py` from the root |
| S-box test import error | Run the S-box test command from the project root |

## 12. Important security limitations

This project is intended for education and cryptographic experimentation.

- It implements a single-block AES primitive, not a complete file-encryption system.
- It does not implement a mode of operation such as CBC or GCM.
- It does not use authenticated encryption or provide integrity protection.
- It does not implement padding.
- It is not designed to resist timing or other side-channel attacks.
- The example key is public test data and must never be used to protect real information.

For real applications, use a vetted cryptographic library and an authenticated encryption mode such as AES-GCM, with secure key generation and management.

## 13. Possible future extensions

- Support multiple blocks.
- Add PKCS#7 padding where an appropriate block mode requires it.
- Implement CBC and CTR modes for learning.
- Add AES-GCM through a vetted library for practical authenticated encryption.
- Add unit tests for each AES transformation and key expansion.
- Add round-by-round state tracing for cryptanalysis experiments.
- Compare the generated S-box and intermediate values against published AES test vectors.

## 14. Reference

- NIST, **FIPS 197: Advanced Encryption Standard (AES)**: https://doi.org/10.6028/NIST.FIPS.197
