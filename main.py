from modules.auth import AuthService
from modules.admin import admin_menu
from modules.user import user_menu
from utils.file_handler import initialize_json_files
from models.user import User


class GroceryManagementSystem:
    """Main application class for Grocery Management System"""
    
    def __init__(self):
        """Initialize the system"""
        self.auth_service = AuthService()
        self.current_user = None
        initialize_json_files()
    
    def display_welcome_message(self):
        """Display welcome message"""
        print("\n=========== WELCOME TO GROCERY MANAGEMENT SYSTEM ===========")
    
    def display_main_menu(self):
        """Display main menu options"""
        print("1. Login")
        print("2. Signup")
        print("3. Exit")
    
    def handle_login(self):
        """Handle user login"""
        user = self.auth_service.login()
        
        if user:
            self.current_user = user
            
            if user.is_admin():
                print("\n--------- Welcome Admin ---------")
                admin_menu()
            else:
                print("\n--------- Welcome User ---------")
                # Convert User object to dict for backward compatibility
                user_dict = user.to_dict()
                user_menu(user_dict)
            
            # Clear current user after logout
            self.current_user = None
    
    def handle_signup(self):
        """Handle user signup"""
        user = self.auth_service.signup()
        if user:
            print("\n✅ Signed Up Successfully")
    
    def run(self):
        """Main application loop"""
        while True:
            self.display_welcome_message()
            self.display_main_menu()
            
            choice = input("Enter your choice: ")
            
            if choice == "1":
                self.handle_login()
            
            elif choice == "2":
                self.handle_signup()
            
            elif choice == "3":
                print("Thank you for using Grocery System!")
                break
            
            else:
                print("Invalid input. Please choose between 1-3.")


def main():
    """Entry point of the application"""
    app = GroceryManagementSystem()
    app.run()


if __name__ == "__main__":
    main()