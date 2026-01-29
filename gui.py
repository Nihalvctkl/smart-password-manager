import tkinter as tk
from tkinter import messagebox, simpledialog

from manager.auth import (
    master_exists,
    set_master_password,
    verify_master_password,
    reset_master_password
)
from manager.crypto import derive_key
from manager.vault import Vault
from manager.generator import generate_password


class PasswordManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Password Manager")
        self.root.geometry("400x300")

        self.key = None
        self.vault = None

        self.show_login()

    # ---------- LOGIN ----------
    def show_login(self):
        self.clear()

        tk.Label(self.root, text="Smart Password Manager", font=("Arial", 14)).pack(pady=10)

        if not master_exists():
            pwd = simpledialog.askstring("Setup", "Set master password:", show="*")
            if pwd:
                set_master_password(pwd)
                messagebox.showinfo("Success", "Master password set. Restart app.")
                self.root.quit()
            return

        pwd = simpledialog.askstring("Login", "Enter master password:", show="*")
        if not pwd or not verify_master_password(pwd):
            messagebox.showerror("Error", "Access denied")
            self.root.quit()
            return

        self.key = derive_key(pwd)
        self.vault = Vault(self.key)
        self.show_menu()

    # ---------- MAIN MENU ----------
    def show_menu(self):
        self.clear()

        tk.Label(self.root, text="Main Menu", font=("Arial", 13)).pack(pady=10)

        tk.Button(self.root, text="Add Credential", command=self.add_credential).pack(fill="x", padx=40, pady=5)
        tk.Button(self.root, text="View Credentials", command=self.view_credentials).pack(fill="x", padx=40, pady=5)
        tk.Button(self.root, text="Generate Password", command=self.generate_pwd).pack(fill="x", padx=40, pady=5)
        tk.Button(self.root, text="Delete Credential", command=self.delete_credential).pack(fill="x", padx=40, pady=5)
        tk.Button(self.root, text="Reset Master Password", command=self.reset_master).pack(fill="x", padx=40, pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    # ---------- ACTIONS ----------
    def add_credential(self):
        site = simpledialog.askstring("Add", "Site:")
        user = simpledialog.askstring("Add", "Username:")
        pwd = simpledialog.askstring("Add", "Password:")

        if site and user and pwd:
            self.vault.add_entry(site, user, pwd)
            messagebox.showinfo("Saved", "Credential stored securely")

    def view_credentials(self):
        entries = self.vault.get_entries()
        if not entries:
            messagebox.showinfo("Empty", "No credentials stored")
            return

        text = ""
        for i, e in enumerate(entries, 1):
            text += f"{i}. {e['site']} | {e['username']} | {e['password']}\n"

        messagebox.showinfo("Stored Credentials", text)

    def generate_pwd(self):
        length = simpledialog.askinteger("Generate", "Password length:", initialvalue=12)
        if not length:
            return

        pwd = generate_password(length)
        save = messagebox.askyesno("Generated", f"{pwd}\n\nSave this password?")
        if save:
            site = simpledialog.askstring("Save", "Site:")
            user = simpledialog.askstring("Save", "Username:")
            if site and user:
                self.vault.add_entry(site, user, pwd)
                messagebox.showinfo("Saved", "Generated password saved")

    def delete_credential(self):
        entries = self.vault.get_entries()
        if not entries:
            messagebox.showinfo("Empty", "No credentials to delete")
            return

        choices = "\n".join([f"{i+1}. {e['site']}" for i, e in enumerate(entries)])
        idx = simpledialog.askinteger("Delete", f"Choose entry number:\n{choices}")

        if idx and 1 <= idx <= len(entries):
            self.vault.delete_entry_by_index(idx - 1)
            messagebox.showinfo("Deleted", "Credential removed")

    def reset_master(self):
        old = simpledialog.askstring("Reset", "Current master password:", show="*")
        new = simpledialog.askstring("Reset", "New master password:", show="*")

        result = reset_master_password(old, new)
        if result is True:
            messagebox.showinfo("Reset", "Master password reset.\nRestart app.")
            self.root.quit()
        elif result is None:
            messagebox.showerror("Error", "New password cannot be the same")
        else:
            messagebox.showerror("Error", "Incorrect current password")

    # ---------- UTIL ----------
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerGUI(root)
    root.mainloop()