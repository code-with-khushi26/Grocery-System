from modules.auth import signup, login
from modules.admin import admin_menu
from modules.user import user_menu
from utils.file_handler import initialize_json_files 

def main():
    initialize_json_files()
    while True:
        print("\n=========== WELCOME TO GROCERY MANAGEMENT SYSTEM ===========")
        print("1. Login")
        print("2. Signup")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            user = login()  

            if user:  
                if user.get("role") == "admin":
                    print("\n--------- Welcome Admin ---------")
                    admin_menu()  
                else:
                    print("\n--------- Welcome User ---------")
                    user_menu(user)  

        elif choice == "2":
            signup()
            print("\n Signed Up Successfully")

        elif choice == "3":
            print("Thank you for using Grocery System!")
            break

        else:
            print("Invalid input. Please choose between 1-3.")


if __name__ == "__main__":
    main()
