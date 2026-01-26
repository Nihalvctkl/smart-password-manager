from typing import List, Dict

class Vault:
    def __init__(self):
        self._credentials: List[Dict[str, str]] = []

    def add_entry(self, site: str, username: str, password: str) -> None:
        entry = {
            "site": site,
            "username": username,
            "password": password
        }
        self._credentials.append(entry)

    def list_entries(self) -> List[Dict[str, str]]:
        return self._credentials

    def delete_entry(self, site: str) -> bool:
        for entry in self._credentials:
            if entry["site"] == site:
                self._credentials.remove(entry)
                return True
        return False