import json
import os
from getpass import getpass

USER_FILE_PATH = "data/users.json"


def load_users():
    """Load users.json and return list, or empty list if file missing."""
    if os.path.exists(USER_FILE_PATH):
        with open(USER_FILE_PATH, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []


def save_users(users):
    """Write updated user list to users.json."""
    with open(USER_FILE_PATH, "w") as file:
        json.dump(users, file, indent=4)

def signup():
    print("\n----WELCOME TO SIGNUP PAGE----\n")
    name=input("Enter you name: ")
    dob=input("Enter you date of birth: ")
    phone=input("Enter your phone number: ")
    location=input("Enter your location: ")
    password=getpass("Enter your Password: ")
    print("Press Enter to sign up")

    users = load_users()
    for user in users:
        if user["phone"] == phone:
            print("\n Account already exists! Try logging in.\n")
            return
    new_user = {
        "name": name,
        "dob": dob,
        "phone": phone,
        "location": location,
        "password": password,
        "role": "user"
    }
    users.append(new_user)
    save_users(users)


def login():
    print("\n---- LOGIN ----\n")

    users = load_users()

    if not users:
        print("No registered users found. Please sign up first.\n")
        return None

    attempts = 3

    while attempts > 0:
        phone = input("Enter phone number: ")
        password = input("Enter password: ")

        for user in users:
            if user["phone"] == phone:
                if user["password"] == password:
                    print(f"\n Welcome {user['name']}! Login successful.\n")
                    return user  
                else:
                    print(" Incorrect password.\n")
                    attempts -= 1
                    break
        else:
            print(" Phone number not found.\n")
            attempts -= 1

        if attempts > 0:
            print(f"Try again... attempts left: {attempts}")

    print("\n Too many failed attempts. Login blocked.\n")
    return None

