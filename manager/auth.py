import hashlib
import os

MASTER_FILE = "master.key"

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def master_exists() -> bool:
    return os.path.exists(MASTER_FILE)

def set_master_password(password: str) -> None:
    hashed = hash_password(password)
    with open(MASTER_FILE, "w") as f:
        f.write(hashed)
