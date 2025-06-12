import json
import os
from encryption import encode, decode
from utils import load_users, show_users_with_status

MESSAGES_FILE = "data/messages.json"

def load_messages():
    if not os.path.exists(MESSAGES_FILE):
        return []
    with open(MESSAGES_FILE, "r") as file:
        return json.load(file)

def save_messages(messages):
    with open(MESSAGES_FILE, "w") as file:
        json.dump(messages, file, indent=2)

def suggest_users(current_user):
    users = load_users()
    print("\n👥 Available Users to Chat With:")
    show_users_with_status(current_user) 
    available_users = [user for user in users if user != current_user]
    if not available_users:
        print("❌ No other users are registered yet.")
        return []
    for idx, user in enumerate(available_users, 1):
        print(f"{idx}. {user}")
    return available_users

def choose_chat_partner(current_user):
    available_users = suggest_users(current_user)
    if not available_users:
        return None
    try:
        choice = int(input("\nChoose a user to start a conversation with (enter number): "))
        if 1 <= choice <= len(available_users):
            return available_users[choice - 1]
        else:
            print("❌ Invalid choice.")
            return None
    except ValueError:
        print("❌ Invalid input.")
        return None

def send_message(sender, receiver):
    message = input(f"Enter your message for {receiver}: ")
    encrypted = encode(message)
    msg_data = {
        "from": sender,
        "to": receiver,
        "message": encrypted
    }
    messages = load_messages()
    messages.append(msg_data)
    save_messages(messages)
    print(f"✅ Message sent to {receiver} (encrypted).")

def view_inbox(user):
    messages = load_messages()
    inbox = [m for m in messages if m["to"] == user]
    if not inbox:
        print("📭 No messages.")
        return
    print("\n📥 Your Messages:")
    for msg in inbox:
        sender = msg["from"]
        try:
            decrypted = decode(msg["message"])
        except:
            decrypted = "[Error decrypting]"
        print(f"\nFrom: {sender}\nMessage: {decrypted}")
