import json
import os

# ------------------ Caesar Cipher ------------------
def encode(message, shift):
    result = ""
    for char in message:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            result += chr((ord(char) - offset + shift) % 26 + offset)
        else:
            result += char
    return result

def decode(message, shift):
    return encode(message, -shift)

# ------------------ Message Storage ------------------
MESSAGES_FILE = "messages.json"

def load_messages():
    if not os.path.exists(MESSAGES_FILE):
        return []
    with open(MESSAGES_FILE, "r") as file:
        return json.load(file)

def save_messages(messages):
    with open(MESSAGES_FILE, "w") as file:
        json.dump(messages, file, indent=2)

# ------------------ Main Messenger ------------------
def send_message(username, shift):
    text = input("Enter your message: ")
    encrypted = encode(text, shift)
    message = {
        "sender": username,
        "message": encrypted,
        "shift": shift
    }
    messages = load_messages()
    messages.append(message)
    save_messages(messages)
    print("✅ Message sent and encrypted!")

def view_messages(decrypted=False):
    messages = load_messages()
    print("\n📨 Message History:")
    for msg in messages:
        sender = msg['sender']
        text = msg['message']
        shift = msg['shift']
        if decrypted:
            text = decode(text, shift)
        print(f"{sender}: {text}")
    print()

# ------------------ Run App ------------------
def main():
    print("🔐 Welcome to the Encrypted Messenger")
    username = input("Enter your name: ")
    try:
        shift = int(input("Enter your encryption shift value (e.g., 3): "))
    except ValueError:
        print("❌ Invalid shift. Must be a number.")
        return

    while True:
        print("\nOptions:")
        print("1. Send a message")
        print("2. View encrypted messages")
        print("3. View decrypted messages")
        print("4. Exit")
        choice = input("Choose an option (1–4): ")

        if choice == "1":
            send_message(username, shift)
        elif choice == "2":
            view_messages(decrypted=False)
        elif choice == "3":
            view_messages(decrypted=True)
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❗ Invalid choice.")

if __name__ == "__main__":
    main()