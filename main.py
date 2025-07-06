import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import os

# ===== Key Management =====
KEY_FILE = "secret.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

# ===== File Encryption =====
def encrypt_file():
    file_path = filedialog.askopenfilename(title="Select File to Encrypt")
    if not file_path:
        return
    try:
        key = load_key()
        fernet = Fernet(key)
        with open(file_path, "rb") as f:
            data = f.read()
        encrypted = fernet.encrypt(data)

        encrypted_path = file_path + ".enc"
        with open(encrypted_path, "wb") as f:
            f.write(encrypted)

        messagebox.showinfo("Success", f"File encrypted:\n{encrypted_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Encryption failed:\n{e}")

# ===== File Decryption =====
def decrypt_file():
    file_path = filedialog.askopenfilename(title="Select File to Decrypt", filetypes=[("Encrypted files", "*.enc")])
    if not file_path:
        return
    try:
        key = load_key()
        fernet = Fernet(key)
        with open(file_path, "rb") as f:
            encrypted = f.read()
        decrypted = fernet.decrypt(encrypted)

        save_path = filedialog.asksaveasfilename(title="Save Decrypted File As")
        if not save_path:
            return

        with open(save_path, "wb") as f:
            f.write(decrypted)

        messagebox.showinfo("Success", f"File decrypted:\n{save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Decryption failed:\n{e}")

# ===== GUI Setup =====
root = tk.Tk()
root.title("File Encryptor & Decryptor")
root.geometry("400x200")
root.resizable(False, False)

tk.Label(root, text="Secure File Encryption & Decryption", font=("Arial", 14)).pack(pady=20)

tk.Button(root, text="Encrypt File", width=20, command=encrypt_file).pack(pady=10)
tk.Button(root, text="Decrypt File", width=20, command=decrypt_file).pack(pady=10)

root.mainloop()
