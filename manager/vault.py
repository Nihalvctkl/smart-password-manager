from typing import List, Dict
from manager.storage import load_vault, save_vault
from manager.crypto import encrypt, decrypt

class Vault:
    def __init__(self, key: bytes):
        self._key = key
        self._credentials: List[Dict[str, str]] = load_vault()

    def add_entry(self, site: str, username: str, password: str) -> None:
        encrypted_password = encrypt(password, self._key)

        entry = {
            "site": site,
            "username": username,
            "password": encrypted_password
        }

        self._credentials.append(entry)
        save_vault(self._credentials)

    def get_entries(self) -> List[Dict[str, str]]:
        """
        Return decrypted credentials (in memory only)
        """
        decrypted_entries = []

        for entry in self._credentials:
            decrypted_entries.append({
                "site": entry["site"],
                "username": entry["username"],
                "password": decrypt(entry["password"], self._key)
            })

        return decrypted_entries

    def delete_entry(self, site: str) -> bool:
        for entry in self._credentials:
            if entry["site"] == site:
                self._credentials.remove(entry)
                save_vault(self._credentials)
                return True
        return False