# 🔐 Smart Password Manager

A secure **Python-based password manager** that allows users to store, retrieve, generate, and manage passwords safely using a **master password**.  
The project supports both a **Command Line Interface (CLI)** and a **Graphical User Interface (GUI)** built with Tkinter.

All credentials are **encrypted at rest** using a key derived from the master password.

---

## 🎯 Project Objectives

- Learn secure password handling concepts
- Implement encryption and hashing in Python
- Design a modular, real-world project structure
- Practice Git & GitHub workflow with meaningful commits
- Provide both CLI and GUI access to the same logic

---

## ✨ Features

- 🔑 Master password setup and verification
- 🔒 Encrypted storage of credentials
- ➕ Add credentials (site, username, password)
- 👀 View stored credentials
- ❌ Delete credentials
- 🔁 Reset master password with vault re-encryption
- 🔐 Strong password generator
- 🖥️ Command Line Interface (CLI)
- 🪟 Graphical User Interface (GUI) using Tkinter

---

## 🧱 Project Structure

smart-password-manager/
│
├── main.py # Entry point for CLI version
├── gui.py # Entry point for GUI version (Tkinter)
│
├── manager/ # Core application logic
│ ├── init.py
│ ├── auth.py # Master password setup, verification & reset
│ ├── crypto.py # Key derivation, encryption & decryption
│ ├── vault.py # Credential management (add, view, delete)
│ ├── generator.py # Strong password generator
│ └── storage.py # Persistent storage handling (JSON)
│
├── data/ # Encrypted application data
│ └── vault.json # Encrypted credentials (ignored by Git)
│
├── master.key # Hashed master password (ignored by Git)
├── .gitignore # Ignores sensitive and generated files
└── README.md # Project documentation


## 🚀 How to Run the Project

> ⚠️ **Important:** Always run the application from the project root directory.

### ▶️ Run CLI Version
```bash
python main.py