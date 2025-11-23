from modules.auth import signup, login

def main():
    while True:
        print("\n=========== WELOCOME TO GROCERY MANAGEMENT SYSTEM ===========")
        print("1. Login")
        print("2. Signup")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            user = login()  

            if user:  
                if user.get("role") == "admin":
                    print("\n--------- Welcome Admin ---------")
                    # admin_menu()  # call later
                else:
                    print("\n--------- Welcome User ---------")
                    # user_menu()  # call later

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
