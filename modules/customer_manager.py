import json
import os
from models.user import User

USER_FILE_PATH = "data/users.json"


class CustomerRepository:
    """Repository class for managing customer data"""
    
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
    
    def get_all_customers(self):
        """Get all users (both admin and regular users)"""
        return self.load_all()


class CustomerService:
    """Service class for customer management operations"""
    
    def __init__(self):
        self.customer_repo = CustomerRepository()
    
    def view_users(self):
        """Display all registered users to admin"""
        print("\n---- REGISTERED USERS ----\n")
        
        users = self.customer_repo.get_all_customers()
        
        if not users:
            print("⚠️  No registered users found.\n")
            return
        
        for user in users:
            print(f"Name: {user.name}")
            print(f"Phone: {user.phone}")
            print(f"Location: {user.location}")
            print(f"Role: {user.role}")
            print("-" * 30)


# Legacy function for backward compatibility
def load_users():
    """Load users from JSON (legacy function)"""
    repo = CustomerRepository()
    users = repo.load_all()
    return [user.to_dict() for user in users]


def view_users():
    """View users (legacy function)"""
    service = CustomerService()
    service.view_users()