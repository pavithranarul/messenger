import getpass
import random
import smtplib
import json
import os
from email.mime.text import MIMEText
from utils import load_users, save_users, hash_password, check_password, update_user_status
from messaging import suggest_users
from encryption import OTP_STORE

def send_and_verify_otp(email):
    otp = str(random.randint(100000, 999999))
    OTP_STORE[email] = otp

    msg = MIMEText(f"Your OTP for Messenger App is: {otp}")
    msg['Subject'] = "Messenger App OTP Verification"
    msg['From'] = "pavithranarul7@gmail.com"
    msg['To'] = email

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("pavithranarul7@gmail.com", "**** **** ****") #replace with app code
        server.sendmail(msg['From'], [msg['To']], msg.as_string())
        server.quit()
        print("📧 OTP sent to your email.")
    except Exception as e:
        print("❌ Failed to send email:", e)
        return False

    entered_otp = input("Enter the OTP sent to your email: ").strip()
    if entered_otp == OTP_STORE[email]:
        print("✅ Email verified!")
        return True
    else:
        print("❌ Incorrect OTP.")
        return False

def register_user():
    users = load_users()
    email = input("Enter your email address: ").strip()

    for user_data in users.values():
        if user_data.get("email") == email:
            print("❌ Email already registered.")
            return None

    if not send_and_verify_otp(email):
        return None

    username = input("Choose a username: ")
    if username in users:
        print("❌ Username already exists.")
        return None

    password = getpass.getpass("Choose a password: ")
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
        suggest_users(username)
        update_user_status(username, online=True)  # Mark user as online
        return username
    else:
        print("❌ Invalid username or password.")
        return None
