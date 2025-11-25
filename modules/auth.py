import json
import os
from getpass import getpass
from utils.validation import (
    get_validated_name,
    get_validated_date,
    get_validated_phone,
    get_validated_password,
    sanitize_input
)
from models.user import User

USER_FILE_PATH = "data/users.json"


class UserRepository:
    """Repository class for managing user data persistence"""
    
    def __init__(self, file_path=USER_FILE_PATH):
        self.file_path = file_path
    
    def load_all(self):
        """Load all users from JSON file"""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                try:
                    data = json.load(file)
                    return [User.from_dict(user_data) for user_data in data]
                except json.JSONDecodeError:
                    return []
        return []
    
    def save_all(self, users):
        """Save all users to JSON file"""
        with open(self.file_path, "w") as file:
            user_dicts = [user.to_dict() for user in users]
            json.dump(user_dicts, file, indent=4)
    
    def find_by_phone(self, phone):
        """Find a user by phone number"""
        users = self.load_all()
        for user in users:
            if user.phone == phone:
                return user
        return None
    
    def add_user(self, user):
        """Add a new user"""
        users = self.load_all()
        users.append(user)
        self.save_all(users)
        return True
    
    def user_exists(self, phone):
        """Check if user with given phone exists"""
        return self.find_by_phone(phone) is not None


class AuthService:
    """Service class for authentication operations"""
    
    def __init__(self):
        self.user_repo = UserRepository()
    
    def signup(self):
        """Handle user signup"""
        print("\n----WELCOME TO SIGNUP PAGE----\n")
        
        name = get_validated_name("your name")
        dob = get_validated_date("your date of birth")
        phone = get_validated_phone()
        location = sanitize_input(input("Enter your location: "))
        password = get_validated_password()
        print("Press Enter to sign up")
        
        # Check if user already exists
        if self.user_repo.user_exists(phone):
            print("\n Account already exists! Try logging in.\n")
            return None
        
        # Create new user object
        new_user = User(name, dob, phone, location, password, role="user")
        
        # Save user
        self.user_repo.add_user(new_user)
        print("\n✅ Account created successfully!\n")
        return new_user
    
    def login(self):
        """Handle user login"""
        print("\n---- LOGIN ----\n")
        
        users = self.user_repo.load_all()
        
        if not users:
            print("No registered users found. Please sign up first.\n")
            return None
        
        attempts = 3
        
        while attempts > 0:
            phone = input("Enter phone number: ")
            password = input("Enter password: ")
            
            # Find user by phone
            user = self.user_repo.find_by_phone(phone)
            
            if user:
                if user.validate_password(password):
                    print(f"\n Welcome {user.name}! Login successful.\n")
                    return user
                else:
                    print(" Incorrect password.\n")
                    attempts -= 1
            else:
                print(" Phone number not found.\n")
                attempts -= 1
            
            if attempts > 0:
                print(f"Try again... attempts left: {attempts}")
        
        print("\n Too many failed attempts. Login blocked.\n")
        return None


# Legacy functions for backward compatibility
def load_users():
    """Load users from JSON (legacy function)"""
    repo = UserRepository()
    users = repo.load_all()
    return [user.to_dict() for user in users]


def save_users(users):
    """Save users to JSON (legacy function)"""
    repo = UserRepository()
    user_objects = [User.from_dict(u) if isinstance(u, dict) else u for u in users]
    repo.save_all(user_objects)


def signup():
    """Handle signup (legacy function)"""
    auth_service = AuthService()
    auth_service.signup()


def login():
    """Handle login (legacy function)"""
    auth_service = AuthService()
    return auth_service.login()