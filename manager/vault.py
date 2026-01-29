from manager.crypto import encrypt, decrypt
from manager.storage import load_vault, save_vault

class Vault:
    def __init__(self, key: str):
        self._key = key
        self._credentials = load_vault()

    def add_entry(self, site: str, username: str, password: str) -> None:
        encrypted_password = encrypt(password, self._key)

        entry = {
            "site": site,
            "username": username,
            "password": encrypted_password
        }

        self._credentials.append(entry)
        save_vault(self._credentials)

    def get_entries(self):
        decrypted_entries = []

        for entry in self._credentials:
            decrypted_entries.append({
                "site": entry["site"],
                "username": entry["username"],
                "password": decrypt(entry["password"], self._key)
            })

        return decrypted_entries

    def delete_entry_by_index(self, index: int) -> bool:
        """
        Delete credential by index (0-based).
        """
        if 0 <= index < len(self._credentials):
            self._credentials.pop(index)
            save_vault(self._credentials)
            return True
        return False