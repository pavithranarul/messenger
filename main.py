import json
import os
from auth import register_user, login_user
from messaging import suggest_users, send_message, view_inbox, choose_chat_partner
from utils import load_users, load_json, save_json, update_user_status

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

def search_users(current_user):
    users = load_users()
    available_users = [user for user in users if user != current_user]
    if not available_users:
        print("❌ No other users are registered yet.")
        return []

    keyword = input("🔍 Search for a user (press enter to show all): ").strip().lower()
    filtered = [user for user in available_users if keyword in user.lower()]

    if not filtered:
        print("⚠️ No users match your search.")
    else:
        for idx, user in enumerate(filtered, 1):
            print(f"{idx}. {user}")
    return filtered


if __name__ == "__main__":
    current_user = auth_menu()
    selected_receiver = None
    if current_user:
        search_users(current_user)  # This replaces suggest_users
        selected_receiver = input("✉️ Enter username to chat with: ").strip()
        while True:
            print("\n📲 What do you want to do?")
            print("1. Select Chat Partner")
            print("2. Send Message")
            print("3. View Inbox")
            print("4. Logout")
            action = input("Choose option: ")
            if action == "1":
                # selected_receiver = choose_chat_partner(current_user)
                if selected_receiver:
                    print(f"✅ You can now chat with {selected_receiver}.")
            elif action == "2":
                if selected_receiver:
                    send_message(current_user, selected_receiver)
                else:
                    print("🤔 Please select a chat partner first (Option 1).")
            elif action == "3":
                view_inbox(current_user)
            elif action == "4":  # Logout option
                update_user_status(current_user, online=False)  # Mark user as offline
                print("👋 Logged out.")
                break
            else:
                print("❗ Invalid choice.")
