from modules.product_manager import add_product, view_products, update_product, delete_product
from modules.customer_manager import view_users
from modules.order_manager import order_management_menu
from modules.reporting import reporting_menu
from modules.supplier_manager import supplier_menu
from modules.inventory_manager import inventory_menu
from utils.file_handler import file_management_menu

def admin_menu():
    while True:
        print("\n===== ADMIN DASHBOARD =====")
        print("1. Add Product")
        print("2. View Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. View Users")
        print("6. Order Management")
        print("7. Reports & Analytics")
        print("8. Supplier Management")
        print("9. Inventory Management")
        print("10. File Management") 
        print("11. Logout")
        
        choice = input("Enter choice: ")

        if choice == "1":
            add_product()
        elif choice == "2":
            view_products()
        elif choice == "3":
            update_product()
        elif choice == "4":
            delete_product()
        elif choice == "5":
            view_users()
        elif choice == "6":
            order_management_menu()
        elif choice == "7":
            reporting_menu()
        elif choice == "8":
            supplier_menu()
        elif choice == "9":
            inventory_menu()
        elif choice == "10":
            file_management_menu()

        elif choice == "11":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")