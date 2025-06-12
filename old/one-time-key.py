import os
from cryptography.fernet import Fernet

KEY_FILE = "secret.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as file:
        file.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as file:
        return file.read()

fernet = Fernet(load_key())
