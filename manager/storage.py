import json
import os
from typing import List, Dict

# Get absolute path to project root
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# data/vault.json relative to project root
VAULT_FILE = os.path.join(BASE_DIR, "data", "vault.json")

def load_vault() -> List[Dict[str, str]]:
    if not os.path.exists(VAULT_FILE):
        return []

    with open(VAULT_FILE, "r") as f:
        return json.load(f)

def save_vault(data: List[Dict[str, str]]) -> None:
    os.makedirs(os.path.dirname(VAULT_FILE), exist_ok=True)

    with open(VAULT_FILE, "w") as f:
        json.dump(data, f, indent=4)