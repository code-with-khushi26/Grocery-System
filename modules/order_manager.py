import json
import os
from datetime import datetime

ORDER_FILE_PATH = "data/orders.json"


def load_orders():
    """Load orders from JSON file."""
    if os.path.exists(ORDER_FILE_PATH):
        with open(ORDER_FILE_PATH, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []


def save_orders(orders):
    """Save updated orders to JSON."""
    with open(ORDER_FILE_PATH, "w") as file:
        json.dump(orders, file, indent=4)


def view_all_orders():
    """Display all orders in the system (Admin)."""
    print("\n---- ALL ORDERS ----")
    orders = load_orders()
    
    if not orders:
        print("📦 No orders found.")
        return
    
    for order in orders:
        print(f"\nOrder ID: {order['order_id']}")
        print(f"Customer: {order['customer_name']} | Phone: {order['customer_phone']}")
        print(f"Date: {order['order_date']}")
        print(f"Status: {order['status']}")
        print("Items:")
        for item in order['items']:
            print(f"  - {item['product_name']} × {item['quantity']} = ₹{item['subtotal']}")
        print(f"Total Amount: ₹{order['total_amount']}")
        print("-" * 50)


def view_order_by_id():
    """Search and display a specific order by ID."""
    orders = load_orders()
    
    if not orders:
        print("\n📦 No orders found.")
        return
    
    try:
        order_id = int(input("\nEnter Order ID: "))
        
        for order in orders:
            if order['order_id'] == order_id:
                print(f"\n---- ORDER DETAILS ----")
                print(f"Order ID: {order['order_id']}")
                print(f"Customer: {order['customer_name']}")
                print(f"Phone: {order['customer_phone']}")
                print(f"Date: {order['order_date']}")
                print(f"Status: {order['status']}")
                print("\nItems Ordered:")
                for item in order['items']:
                    print(f"  - {item['product_name']} × {item['quantity']} = ₹{item['subtotal']}")
                print(f"\nTotal Amount: ₹{order['total_amount']}")
                return
        
        print("❌ Order ID not found.")
    
    except ValueError:
        print("❌ Invalid input. Please enter a number.")


def update_order_status():
    """Update the status of an order."""
    orders = load_orders()
    
    if not orders:
        print("\n📦 No orders found.")
        return
    
    try:
        order_id = int(input("\nEnter Order ID to update: "))
        
        for order in orders:
            if order['order_id'] == order_id:
                print(f"\nCurrent Status: {order['status']}")
                print("\nAvailable Status Options:")
                print("1. Pending")
                print("2. Processing")
                print("3. Shipped")
                print("4. Delivered")
                print("5. Cancelled")
                
                choice = input("\nEnter new status (1-5): ")
                
                status_map = {
                    "1": "Pending",
                    "2": "Processing",
                    "3": "Shipped",
                    "4": "Delivered",
                    "5": "Cancelled"
                }
                
                if choice in status_map:
                    order['status'] = status_map[choice]
                    save_orders(orders)
                    print(f"✅ Order status updated to '{status_map[choice]}'")
                else:
                    print("❌ Invalid choice.")
                return
        
        print("❌ Order ID not found.")
    
    except ValueError:
        print("❌ Invalid input.")


def delete_order():
    """Delete an order from the system."""
    orders = load_orders()
    
    if not orders:
        print("\n📦 No orders found.")
        return
    
    try:
        order_id = int(input("\nEnter Order ID to delete: "))
        
        for order in orders:
            if order['order_id'] == order_id:
                print(f"\nOrder ID: {order['order_id']}")
                print(f"Customer: {order['customer_name']}")
                print(f"Total Amount: ₹{order['total_amount']}")
                
                confirm = input("\nAre you sure you want to delete this order? (yes/no): ").lower()
                
                if confirm == "yes":
                    orders.remove(order)
                    save_orders(orders)
                    print("🗑️ Order deleted successfully!")
                else:
                    print("❌ Deletion cancelled.")
                return
        
        print("❌ Order ID not found.")
    
    except ValueError:
        print("❌ Invalid input.")


def view_orders_by_customer():
    """View all orders from a specific customer."""
    phone = input("\nEnter customer phone number: ")
    
    orders = load_orders()
    customer_orders = [order for order in orders if order.get('customer_phone') == phone]
    
    if not customer_orders:
        print(f"\n📦 No orders found for phone number: {phone}")
        return
    
    print(f"\n---- ORDERS FOR {customer_orders[0]['customer_name']} ----")
    
    for order in customer_orders:
        print(f"\nOrder ID: {order['order_id']}")
        print(f"Date: {order['order_date']}")
        print(f"Status: {order['status']}")
        print(f"Total: ₹{order['total_amount']}")
        print("-" * 40)


def view_orders_by_status():
    """Filter and view orders by status."""
    print("\n---- FILTER BY STATUS ----")
    print("1. Pending")
    print("2. Processing")
    print("3. Shipped")
    print("4. Delivered")
    print("5. Cancelled")
    print("6. Completed")
    
    choice = input("\nEnter status choice (1-6): ")
    
    status_map = {
        "1": "Pending",
        "2": "Processing",
        "3": "Shipped",
        "4": "Delivered",
        "5": "Cancelled",
        "6": "Completed"
    }
    
    if choice not in status_map:
        print("❌ Invalid choice.")
        return
    
    selected_status = status_map[choice]
    orders = load_orders()
    filtered_orders = [order for order in orders if order.get('status') == selected_status]
    
    if not filtered_orders:
        print(f"\n📦 No orders with status '{selected_status}'.")
        return
    
    print(f"\n---- ORDERS WITH STATUS: {selected_status} ----")
    
    for order in filtered_orders:
        print(f"\nOrder ID: {order['order_id']}")
        print(f"Customer: {order['customer_name']} | Phone: {order['customer_phone']}")
        print(f"Date: {order['order_date']}")
        print(f"Total: ₹{order['total_amount']}")
        print("-" * 40)


def calculate_total_revenue():
    """Calculate total revenue from all completed orders."""
    orders = load_orders()
    
    if not orders:
        print("\n📦 No orders found.")
        return
    
    total_revenue = sum(order['total_amount'] for order in orders if order.get('status') in ['Completed', 'Delivered'])
    total_orders = len([order for order in orders if order.get('status') in ['Completed', 'Delivered']])
    
    print("\n---- REVENUE SUMMARY ----")
    print(f"Total Completed Orders: {total_orders}")
    print(f"Total Revenue: ₹{total_revenue}")
    
    if total_orders > 0:
        avg_order_value = total_revenue / total_orders
        print(f"Average Order Value: ₹{avg_order_value:.2f}")


def order_management_menu():
    """Sub-menu for order management operations."""
    while True:
        print("\n===== ORDER MANAGEMENT =====")
        print("1. View All Orders")
        print("2. View Order by ID")
        print("3. View Orders by Customer")
        print("4. View Orders by Status")
        print("5. Update Order Status")
        print("6. Delete Order")
        print("7. Calculate Revenue")
        print("8. Back to Admin Menu")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            view_all_orders()
        elif choice == "2":
            view_order_by_id()
        elif choice == "3":
            view_orders_by_customer()
        elif choice == "4":
            view_orders_by_status()
        elif choice == "5":
            update_order_status()
        elif choice == "6":
            delete_order()
        elif choice == "7":
            calculate_total_revenue()
        elif choice == "8":
            break
        else:
            print("Invalid choice. Try again.")