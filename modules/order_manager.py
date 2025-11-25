import json
import os
from datetime import datetime
from models.user import Order, OrderItem

ORDER_FILE_PATH = "data/orders.json"


class OrderRepository:
    """Repository class for managing order data persistence"""
    
    def __init__(self, file_path=ORDER_FILE_PATH):
        self.file_path = file_path
    
    def load_all(self):
        """Load all orders from JSON file"""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                try:
                    data = json.load(file)
                    return [Order.from_dict(order_data) for order_data in data]
                except json.JSONDecodeError:
                    return []
        return []
    
    def save_all(self, orders):
        """Save all orders to JSON file"""
        with open(self.file_path, "w") as file:
            order_dicts = [order.to_dict() for order in orders]
            json.dump(order_dicts, file, indent=4)
    
    def find_by_id(self, order_id):
        """Find an order by ID"""
        orders = self.load_all()
        for order in orders:
            if order.order_id == order_id:
                return order
        return None
    
    def find_by_customer_phone(self, phone):
        """Find all orders by customer phone"""
        orders = self.load_all()
        return [order for order in orders if order.customer_phone == phone]
    
    def find_by_status(self, status):
        """Find all orders by status"""
        orders = self.load_all()
        return [order for order in orders if order.status == status]
    
    def add_order(self, order):
        """Add a new order"""
        orders = self.load_all()
        orders.append(order)
        self.save_all(orders)
        return True
    
    def update_order(self, order):
        """Update an existing order"""
        orders = self.load_all()
        for i, o in enumerate(orders):
            if o.order_id == order.order_id:
                orders[i] = order
                self.save_all(orders)
                return True
        return False
    
    def delete_order(self, order_id):
        """Delete an order by ID"""
        orders = self.load_all()
        orders = [o for o in orders if o.order_id != order_id]
        self.save_all(orders)
        return True
    
    def get_next_id(self):
        """Get the next available order ID"""
        orders = self.load_all()
        if not orders:
            return 1
        return max(o.order_id for o in orders) + 1


class OrderService:
    """Service class for order management operations"""
    
    def __init__(self):
        self.order_repo = OrderRepository()
    
    def view_all_orders(self):
        """Display all orders in the system (Admin)"""
        print("\n---- ALL ORDERS ----")
        orders = self.order_repo.load_all()
        
        if not orders:
            print("📦 No orders found.")
            return
        
        for order in orders:
            print(f"\nOrder ID: {order.order_id}")
            print(f"Customer: {order.customer_name} | Phone: {order.customer_phone}")
            print(f"Date: {order.order_date}")
            print(f"Status: {order.status}")
            print("Items:")
            for item in order.items:
                print(f"  - {item.product_name} × {item.quantity} = ₹{item.get_subtotal()}")
            print(f"Total Amount: ₹{order.calculate_total()}")
            print("-" * 50)
    
    def view_order_by_id(self):
        """Search and display a specific order by ID"""
        orders = self.order_repo.load_all()
        
        if not orders:
            print("\n📦 No orders found.")
            return
        
        try:
            order_id = int(input("\nEnter Order ID: "))
            
            order = self.order_repo.find_by_id(order_id)
            
            if order:
                print(f"\n---- ORDER DETAILS ----")
                print(f"Order ID: {order.order_id}")
                print(f"Customer: {order.customer_name}")
                print(f"Phone: {order.customer_phone}")
                print(f"Date: {order.order_date}")
                print(f"Status: {order.status}")
                print("\nItems Ordered:")
                for item in order.items:
                    print(f"  - {item.product_name} × {item.quantity} = ₹{item.get_subtotal()}")
                print(f"\nTotal Amount: ₹{order.calculate_total()}")
            else:
                print("❌ Order ID not found.")
        
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
    
    def update_order_status(self):
        """Update the status of an order"""
        orders = self.order_repo.load_all()
        
        if not orders:
            print("\n📦 No orders found.")
            return
        
        try:
            order_id = int(input("\nEnter Order ID to update: "))
            
            order = self.order_repo.find_by_id(order_id)
            
            if order:
                print(f"\nCurrent Status: {order.status}")
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
                    if order.update_status(status_map[choice]):
                        self.order_repo.update_order(order)
                        print(f"✅ Order status updated to '{status_map[choice]}'")
                    else:
                        print("❌ Failed to update status.")
                else:
                    print("❌ Invalid choice.")
            else:
                print("❌ Order ID not found.")
        
        except ValueError:
            print("❌ Invalid input.")
    
    def delete_order(self):
        """Delete an order from the system"""
        orders = self.order_repo.load_all()
        
        if not orders:
            print("\n📦 No orders found.")
            return
        
        try:
            order_id = int(input("\nEnter Order ID to delete: "))
            
            order = self.order_repo.find_by_id(order_id)
            
            if order:
                print(f"\nOrder ID: {order.order_id}")
                print(f"Customer: {order.customer_name}")
                print(f"Total Amount: ₹{order.calculate_total()}")
                
                confirm = input("\nAre you sure you want to delete this order? (yes/no): ").lower()
                
                if confirm == "yes":
                    self.order_repo.delete_order(order_id)
                    print("🗑️ Order deleted successfully!")
                else:
                    print("❌ Deletion cancelled.")
            else:
                print("❌ Order ID not found.")
        
        except ValueError:
            print("❌ Invalid input.")
    
    def view_orders_by_customer(self):
        """View all orders from a specific customer"""
        phone = input("\nEnter customer phone number: ")
        
        customer_orders = self.order_repo.find_by_customer_phone(phone)
        
        if not customer_orders:
            print(f"\n📦 No orders found for phone number: {phone}")
            return
        
        print(f"\n---- ORDERS FOR {customer_orders[0].customer_name} ----")
        
        for order in customer_orders:
            print(f"\nOrder ID: {order.order_id}")
            print(f"Date: {order.order_date}")
            print(f"Status: {order.status}")
            print(f"Total: ₹{order.calculate_total()}")
            print("-" * 40)
    
    def view_orders_by_status(self):
        """Filter and view orders by status"""
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
        filtered_orders = self.order_repo.find_by_status(selected_status)
        
        if not filtered_orders:
            print(f"\n📦 No orders with status '{selected_status}'.")
            return
        
        print(f"\n---- ORDERS WITH STATUS: {selected_status} ----")
        
        for order in filtered_orders:
            print(f"\nOrder ID: {order.order_id}")
            print(f"Customer: {order.customer_name} | Phone: {order.customer_phone}")
            print(f"Date: {order.order_date}")
            print(f"Total: ₹{order.calculate_total()}")
            print("-" * 40)
    
    def calculate_total_revenue(self):
        """Calculate total revenue from all completed orders"""
        orders = self.order_repo.load_all()
        
        if not orders:
            print("\n📦 No orders found.")
            return
        
        completed_orders = [order for order in orders if order.is_completed()]
        total_revenue = sum(order.calculate_total() for order in completed_orders)
        total_orders = len(completed_orders)
        
        print("\n---- REVENUE SUMMARY ----")
        print(f"Total Completed Orders: {total_orders}")
        print(f"Total Revenue: ₹{total_revenue}")
        
        if total_orders > 0:
            avg_order_value = total_revenue / total_orders
            print(f"Average Order Value: ₹{avg_order_value:.2f}")


def order_management_menu():
    """Sub-menu for order management operations"""
    service = OrderService()
    
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
            service.view_all_orders()
        elif choice == "2":
            service.view_order_by_id()
        elif choice == "3":
            service.view_orders_by_customer()
        elif choice == "4":
            service.view_orders_by_status()
        elif choice == "5":
            service.update_order_status()
        elif choice == "6":
            service.delete_order()
        elif choice == "7":
            service.calculate_total_revenue()
        elif choice == "8":
            break
        else:
            print("Invalid choice. Try again.")


# Legacy functions for backward compatibility
def load_orders():
    """Load orders from JSON (legacy function)"""
    repo = OrderRepository()
    orders = repo.load_all()
    return [order.to_dict() for order in orders]


def save_orders(orders):
    """Save orders to JSON (legacy function)"""
    repo = OrderRepository()
    order_objects = [Order.from_dict(o) if isinstance(o, dict) else o for o in orders]
    repo.save_all(order_objects)