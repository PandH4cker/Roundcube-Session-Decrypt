# tripledes_decryptor.py

from typing import Optional
from Crypto.Cipher import DES3
from Crypto.Util.Padding import unpad
import binascii

class TripleDESDecryptionError(Exception):
    """Raised when TripleDES decryption fails."""


class TripleDESDecryptor:
    """Decrypts data using TripleDES (3DES) algorithm in CBC mode."""

    def __init__(self, key: str, iv_hex: str, block_size: int = 8) -> None:
        """
        Initialize the decryptor.

        Args:
            key (str): Key string (must be 16 or 24 bytes when encoded).
            iv_hex (str): Initialization Vector in hex.
            block_size (int): Block size for padding (default is 8 for DES3).
        """
        self.block_size = block_size
        self.iv = bytes.fromhex(iv_hex)

        key_bytes = key.encode("utf-8")

        if len(key_bytes) not in (16, 24):
            raise ValueError("Key must be 16 or 24 bytes for TripleDES.")

        self.key = DES3.adjust_key_parity(key_bytes)

    def decrypt(self, secret_hex: str) -> str:
        """
        Decrypts a TripleDES-encrypted hex string.

        Args:
            secret_hex (str): The encrypted secret in hex format.

        Returns:
            str: Decrypted plaintext string.

        Raises:
            TripleDESDecryptionError: If decryption fails.
        """
        try:
            ciphertext = bytes.fromhex(secret_hex)
            cipher = DES3.new(self.key, DES3.MODE_CBC, self.iv)
            plaintext = unpad(cipher.decrypt(ciphertext), self.block_size)
            return plaintext.decode("utf-8")
        except Exception as e:
            raise TripleDESDecryptionError(str(e)) from e
