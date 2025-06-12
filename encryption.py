from cryptography.fernet import Fernet
import os

KEY_FILE = "data/secret.key"
OTP_STORE = {}

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

def encode(msg):
    return fernet.encrypt(msg.encode()).decode()

def decode(token):
    return fernet.decrypt(token.encode()).decode()
