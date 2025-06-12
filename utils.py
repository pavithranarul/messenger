import json
import os
import hashlib

USERS_FILE = "data/users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as file:
        return json.load(file)

def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(stored_hash, entered_password):
    return stored_hash == hash_password(entered_password)

def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return {}

def save_json(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def update_user_status(username, online=True):
    status = load_json("status.json")
    status[username] = "online" if online else "offline"
    save_json("status.json", status)

def show_users_with_status(current_user):
    users = load_users()
    status = load_json("status.json")
    for user in users:
        if user != current_user:
            state = status.get(user, "offline")
            print(f"{user} - {'🟢' if state == 'online' else '🔴'}")