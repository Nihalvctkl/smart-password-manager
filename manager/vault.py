from manager.crypto import encrypt, decrypt
from manager.storage import load_vault, save_vault

class Vault:
    def __init__(self, key: bytes):
        self._key = key
        self._credentials = load_vault()

    def add_entry(self, site: str, username: str, password: str) -> bool:
        for entry in self._credentials:
            if entry["site"] == site:
                return False

        encrypted_password = encrypt(password, self._key)

        self._credentials.append({
            "site": site,
            "username": username,
            "password": encrypted_password
        })

        save_vault(self._credentials)
        return True

    def get_entries(self):
        return [
            {
                "site": entry["site"],
                "username": entry["username"],
                "password": decrypt(entry["password"], self._key)
            }
            for entry in self._credentials
        ]

    def delete_entry_by_index(self, index: int) -> bool:
        if 0 <= index < len(self._credentials):
            self._credentials.pop(index)
            save_vault(self._credentials)
            return True
        return False

    # 🔥 ADVANCED PART
    def reencrypt_vault(self, old_key: bytes, new_key: bytes) -> None:
        """
        Re-encrypt all stored passwords using a new master key.
        """
        new_credentials = []

        for entry in self._credentials:
            decrypted_password = decrypt(entry["password"], old_key)
            reencrypted_password = encrypt(decrypted_password, new_key)

            new_credentials.append({
                "site": entry["site"],
                "username": entry["username"],
                "password": reencrypted_password
            })

        self._credentials = new_credentials
        save_vault(self._credentials)