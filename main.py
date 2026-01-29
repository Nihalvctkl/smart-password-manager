from manager.auth import (
    master_exists,
    set_master_password,
    verify_master_password
)
from manager.crypto import derive_key
from manager.vault import Vault

def main():
    print("=== Smart Password Manager ===")

    if not master_exists():
        password = input("Set master password: ")
        set_master_password(password)
        print("Master password set successfully.")
        return

    password = input("Enter master password: ")

    if not verify_master_password(password):
        print("Access denied ❌")
        return

    print("Access granted ✅")

    key = derive_key(password)
    vault = Vault(key)

    print("\nAdd new credential")
    site = input("Site: ")
    username = input("Username: ")
    secret = input("Password: ")

    vault.add_entry(site, username, secret)
    print("Credential stored securely 🔐")

if __name__ == "__main__":
    main()