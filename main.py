from manager.auth import (
    master_exists,
    set_master_password,
    verify_master_password,
    reset_master_password
)
from manager.crypto import derive_key
from manager.vault import Vault
from manager.generator import generate_password


def non_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty ❌")


def main():
    print("=== Smart Password Manager ===")

    # First-time setup
    if not master_exists():
        password = non_empty("Set master password: ")
        set_master_password(password)
        print("Master password set successfully ✅")
        return

    # Login
    password = non_empty("Enter master password: ")

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
        print("4. Delete credential")
        print("5. Reset master password")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        # 1️⃣ Add credential
        if choice == "1":
            site = non_empty("Site: ")
            username = non_empty("Username: ")
            secret = non_empty("Password: ")

            if vault.add_entry(site, username, secret):
                print("Credential stored securely 🔐")
            else:
                print("A credential for this site already exists ❌")

        # 2️⃣ View credentials
        elif choice == "2":
            entries = vault.get_entries()
            if not entries:
                print("No credentials stored.")
            else:
                print("\nStored credentials:")
                for i, entry in enumerate(entries, start=1):
                    print(f"{i}. {entry['site']} | {entry['username']} | {entry['password']}")

        # 3️⃣ Generate password
        elif choice == "3":
            length = input("Password length (default 12): ").strip()
            length = int(length) if length.isdigit() and int(length) >= 6 else 12

            generated = generate_password(length)
            print(f"Generated password: {generated}")

            save = input("Save this password? (y/n): ").lower()
            if save == "y":
                site = non_empty("Site: ")
                username = non_empty("Username: ")
                if vault.add_entry(site, username, generated):
                    print("Generated password saved 🔐")
                else:
                    print("A credential for this site already exists ❌")

        # 4️⃣ Delete credential (by number)
        elif choice == "4":
            entries = vault.get_entries()
            if not entries:
                print("No credentials to delete.")
                continue

            print("\nStored credentials:")
            for i, entry in enumerate(entries, start=1):
                print(f"{i}. {entry['site']} | {entry['username']}")

            choice_num = input("Enter number to delete: ").strip()
            if not choice_num.isdigit():
                print("Invalid input ❌")
                continue

            index = int(choice_num) - 1
            confirm = input("Are you sure? (y/n): ").lower()

            if confirm == "y":
                if vault.delete_entry_by_index(index):
                    print("Credential deleted ✅")
                else:
                    print("Invalid selection ❌")
            else:
                print("Deletion cancelled.")

        # 5️⃣ Reset master password (ADVANCED: re-encrypt vault)
        elif choice == "5":
            old = non_empty("Enter current master password: ")
            new = non_empty("Enter new master password: ")

            result = reset_master_password(old, new)

            if result is True:
                old_key = derive_key(old)
                new_key = derive_key(new)

                vault.reencrypt_vault(old_key, new_key)

                print("Master password reset successfully 🔑")
                print("All vault entries were securely re-encrypted.")
                print("Please restart the application.")
                break

            elif result is None:
                print("New password cannot be the same as the current password ❌")
            else:
                print("Incorrect current password ❌")

        # 6️⃣ Exit
        elif choice == "6":
            print("Goodbye 👋")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()