import json
import os
import hashlib
import getpass
import os
from cryptography.fernet import Fernet
import smtplib
import random
from email.mime.text import MIMEText

OTP_STORE = {}

def send_and_verify_otp(email):
    otp = str(random.randint(100000, 999999))
    OTP_STORE[email] = otp
    msg = MIMEText(f"Your OTP for Messenger App is: {otp}")
    msg['Subject'] = "Messenger App OTP Verification"
    msg['From'] = "pavithranarul7@gmail.com"
    msg['To'] = email
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("pavithranarul7@gmail.com", "uirm bfkn wmyl olrd")
        server.sendmail(msg['From'], [msg['To']], msg.as_string())
        server.quit()
        print("📧 OTP sent to your email.")
    except Exception as e:
        print("❌ Failed to send email:", e)
        return False
    # 🔐 Verification step
    entered_otp = input("Enter the OTP sent to your email: ").strip()
    if entered_otp == OTP_STORE[email]:
        print("✅ Email verified!")
        return True
    else:
        print("❌ Incorrect OTP.")
        return False

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

USERS_FILE = "users.json"

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

def register_user():
    users = load_users()
    email = input("Enter your email address: ").strip()
    # Check if the email is already used
    for user_data in users.values():
        if user_data.get("email") == email:
            print("❌ Email already registered.")
            return None
    # Send OTP, verify it (you already have this logic)
    if not send_and_verify_otp(email):
        print("❌ Email verification failed.")
        return None
    username = input("Choose a username: ")
    if username in users:
        print("❌ Username already exists.")
        return None
    password = getpass.getpass("Choose a password: ")
    # Save the user with username as key
    users[username] = {
        "password": hash_password(password),
        "email": email
    }
    save_users(users)
    print("✅ Registration successful!")
    return username


def login_user():
    users = load_users()
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    if username in users and check_password(users[username]['password'], password):
        print(f"✅ Welcome {username}!")
        # Call the function to suggest users
        suggest_users(username)
        return username
    else:
        print("❌ Invalid username or password.")
        return None

def suggest_users(current_user):
    users = load_users()
    print("\n👥 Available Users to Chat With:")
    # List users except the logged-in user
    available_users = [user for user in users if user != current_user]
    if not available_users:
        print("❌ No other users are registered yet.")
        return
    for idx, user in enumerate(available_users, 1):
        print(f"{idx}. {user}")
    # Allow the user to select another user
    choice = int(input("\nChoose a user to start a conversation with (enter number): "))
    if 1 <= choice <= len(available_users):
        selected_user = available_users[choice - 1]
        print(f"✅ You can now chat with {selected_user}.")
        # You can call your messaging function to start the conversation
        send_message(current_user, selected_user)
    else:
        print("❌ Invalid choice.")

    
def encode(msg):
    return fernet.encrypt(msg.encode()).decode()

def decode(token):
    return fernet.decrypt(token.encode()).decode()


# Message handling
MESSAGES_FILE = "messages.json"

def load_messages():
    if not os.path.exists(MESSAGES_FILE):
        return []
    with open(MESSAGES_FILE, "r") as file:
        return json.load(file)

def save_messages(messages):
    with open(MESSAGES_FILE, "w") as file:
        json.dump(messages, file, indent=2)

def send_message(sender, receiver):
    message = input(f"Enter your message for {receiver}: ")
    encrypted_message = encode(message)
    msg_data = {
        "from": sender,
        "to": receiver,
        "message": encrypted_message
    }
    messages = load_messages()
    messages.append(msg_data)
    save_messages(messages)
    print(f"✅ Message sent to {receiver} (encrypted).")


def view_inbox(user):
    messages = load_messages()
    inbox = [m for m in messages if m.get("to") == user]
    if not inbox:
        print("📭 No messages.")
        return
    print("\n📥 Your Messages:")
    for msg in inbox:
        sender = msg["from"]
        encrypted = msg["message"]
        try:
            decrypted = decode(encrypted)
        except Exception as e:
            decrypted = "[Error decrypting]"
        print(f"\nFrom: {user} \nMessage: {decrypted}")


# --- Demo Entry Point ---
def auth_menu():
    print("\n🔐 Welcome to Encrypted Messenger")
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose option: ")
        if choice == "1":
            user = register_user()
            if user:
                return user
        elif choice == "2":
            user = login_user()
            if user:
                return user
        elif choice == "3":
            print("👋 Exiting.")
            return None
        else:
            print("❗ Invalid choice.")


if __name__ == "__main__":
    current_user = auth_menu()
    if current_user:
        while True:
            print("\n📲 What do you want to do?")
            print("1. Send Message")
            print("2. View Inbox")
            print("3. Logout")
            action = input("Choose option: ")
            if action == "1":
                send_message(current_user)
            elif action == "2":
                view_inbox(current_user)
            elif action == "3":
                print("👋 Logged out.")
                break
            else:
                print("❗ Invalid choice.")

