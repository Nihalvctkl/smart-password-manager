from manager.auth import master_exists, set_master_password

def main():
    print("=== Smart Password Manager ===")

    if not master_exists():
        password = input("Set master password: ")
        set_master_password(password)
        print("Master password set successfully.")

if __name__ == "__main__":
    main()
