import hashlib
import base64

def derive_key(master_password: str) -> bytes:
    """
    Derive a fixed-length key from the master password
    """
    return hashlib.sha256(master_password.encode()).digest()

def encrypt(text: str, key: bytes) -> str:
    """
    Encrypt text using XOR + Base64 encoding
    """
    encrypted_bytes = bytearray()

    for i, char in enumerate(text.encode()):
        encrypted_bytes.append(char ^ key[i % len(key)])

    return base64.b64encode(encrypted_bytes).decode()

def decrypt(cipher_text: str, key: bytes) -> str:
    """
    Decrypt text using XOR + Base64 decoding
    """
    encrypted_bytes = base64.b64decode(cipher_text)
    decrypted_bytes = bytearray()

    for i, char in enumerate(encrypted_bytes):
        decrypted_bytes.append(char ^ key[i % len(key)])

    return decrypted_bytes.decode()
