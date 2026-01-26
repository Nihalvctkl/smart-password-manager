from typing import List, Dict
from manager.storage import load_vault, save_vault

class Vault:
    def __init__(self):
        self._credentials: List[Dict[str, str]] = load_vault()

    def add_entry(self, site: str, username: str, password: str) -> None:
        entry = {
            "site": site,
            "username": username,
            "password": password
        }
        self._credentials.append(entry)
        save_vault(self._credentials)

    def list_entries(self) -> List[Dict[str, str]]:
        return self._credentials

    def delete_entry(self, site: str) -> bool:
        for entry in self._credentials:
            if entry["site"] == site:
                self._credentials.remove(entry)
                save_vault(self._credentials)
                return True
        return False