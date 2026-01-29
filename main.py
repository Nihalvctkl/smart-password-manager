from manager.auth import (
    master_exists,
    set_master_password,
    verify_master_password
)
from manager.crypto import derive_key
from manager.vault import Vault
from manager.generator import generate_password

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

    while True:
        print("\nMenu:")
        print("1. Add new credential")
        print("2. View stored credentials")
        print("3. Generate strong password")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            site = input("Site: ")
            username = input("Username: ")
            secret = input("Password: ")

            vault.add_entry(site, username, secret)
            print("Credential stored securely 🔐")

        elif choice == "2":
            entries = vault.get_entries()
            if not entries:
                print("No credentials stored.")
            else:
                for entry in entries:
                    print(f"- {entry['site']} | {entry['username']} | {entry['password']}")

        elif choice == "3":
            length = input("Password length (default 12): ")
            length = int(length) if length.isdigit() else 12

            generated = generate_password(length)
            print(f"Generated password: {generated}")

            save = input("Save this password? (y/n): ").lower()
            if save == "y":
                site = input("Site: ")
                username = input("Username: ")
                vault.add_entry(site, username, generated)
                print("Generated password saved 🔐")

        elif choice == "4":
            print("Goodbye 👋")
            break

        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()