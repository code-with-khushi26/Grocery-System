import json
import os

USER_FILE_PATH = "data/users.json"


def load_users():
    """Load users from JSON."""
    if os.path.exists(USER_FILE_PATH):
        with open(USER_FILE_PATH, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []


def view_users():
    """Display all registered users to admin."""
    print("\n---- REGISTERED USERS ----\n")

    users = load_users()

    if not users:
        print("⚠ No registered users found.\n")
        return

    for user in users:
        print(f"Name: {user['name']}")
        print(f"Phone: {user['phone']}")
        print(f"Location: {user['location']}")
        print(f"Role: {user['role']}")
        print("-" * 30)
