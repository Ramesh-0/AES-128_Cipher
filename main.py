from aes.aes_core import encrypt_block, decrypt_block
from utils.file_handler import read_input, write_output


def main():
    try:
        key, plaintext = read_input("input/input.txt")

        ciphertext = encrypt_block(plaintext, key)
        decrypted = decrypt_block(ciphertext, key)

        result = (
            "========== AES-128 ENCRYPTION ==========\n"
            f"Key:        {key.hex().upper()}\n"
            f"Plaintext:  {plaintext.hex().upper()}\n"
            f"Ciphertext: {ciphertext.hex().upper()}\n\n"
            "========== AES-128 DECRYPTION ==========\n"
            f"Ciphertext:          {ciphertext.hex().upper()}\n"
            f"Decrypted plaintext: {decrypted.hex().upper()}\n\n"
            f"Verification: {'SUCCESS' if decrypted == plaintext else 'FAILED'}\n"
        )

        print(result)
        write_output("output/output.txt", result)

    except (ValueError, FileNotFoundError) as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
