import json
import os
from datetime import datetime
from utils.validation import get_validated_quantity
from models.user import ShoppingCart, Product, Order, OrderItem

PRODUCT_FILE_PATH = "data/products.json"
ORDER_FILE_PATH = "data/orders.json"


class ProductRepository:
    """Repository for product data access"""
    
    def __init__(self, file_path=PRODUCT_FILE_PATH):
        self.file_path = file_path
    
    def load_all(self):
        """Load all products"""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                try:
                    data = json.load(file)
                    return [Product.from_dict(p) for p in data]
                except json.JSONDecodeError:
                    return []
        return []
    
    def save_all(self, products):
        """Save all products"""
        with open(self.file_path, "w") as file:
            product_dicts = [p.to_dict() for p in products]
            json.dump(product_dicts, file, indent=4)
    
    def find_by_id(self, product_id):
        """Find product by ID"""
        products = self.load_all()
        for p in products:
            if p.id == product_id:
                return p
        return None
    
    def update_product(self, product):
        """Update a product"""
        products = self.load_all()
        for i, p in enumerate(products):
            if p.id == product.id:
                products[i] = product
                self.save_all(products)
                return True
        return False


class OrderRepository:
    """Repository for order data access"""
    
    def __init__(self, file_path=ORDER_FILE_PATH):
        self.file_path = file_path
    
    def load_all(self):
        """Load all orders"""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                try:
                    data = json.load(file)
                    return [Order.from_dict(o) for o in data]
                except json.JSONDecodeError:
                    return []
        return []
    
    def save_order(self, order):
        """Save a new order"""
        orders = self.load_all()
        orders.append(order)
        with open(self.file_path, "w") as file:
            order_dicts = [o.to_dict() for o in orders]
            json.dump(order_dicts, file, indent=4)
    
    def get_next_id(self):
        """Get next order ID"""
        orders = self.load_all()
        if not orders:
            return 1
        return max(o.order_id for o in orders) + 1
    
    def find_by_customer_phone(self, phone):
        """Find orders by customer phone"""
        orders = self.load_all()
        return [o for o in orders if o.customer_phone == phone]


class ShoppingService:
    """Service class for shopping operations"""
    
    def __init__(self, user):
        self.user = user
        self.cart = ShoppingCart()
        self.product_repo = ProductRepository()
        self.order_repo = OrderRepository()
    
    def view_products(self):
        """Display all available products"""
        print("\n---- AVAILABLE PRODUCTS ----")
        products = self.product_repo.load_all()
        
        if not products:
            print("⚠️  No products available.")
            return
        
        for product in products:
            status = product.get_stock_status()
            print(f"ID: {product.id} | {product.name} | Category: {product.category} | Price: ₹{product.price} | Qty: {product.quantity} | {status}")
    
    def add_to_cart(self):
        """Add a product to shopping cart"""
        products = self.product_repo.load_all()
        
        if not products:
            print("\n⚠️  No products available.")
            return
        
        try:
            product_id = int(input("\nEnter product ID to add: "))
            
            # Find product
            product = self.product_repo.find_by_id(product_id)
            
            if not product:
                print("❌ Invalid product ID.")
                return
            
            if not product.is_in_stock():
                print(f"❌ Sorry, '{product.name}' is out of stock.")
                return
            
            quantity = get_validated_quantity()
            
            if quantity > product.quantity:
                print(f"❌ Not enough stock. Only {product.quantity} available.")
                return
            
            # Add to cart
            self.cart.add_item(product, quantity)
            print(f"✅ '{product.name}' added to cart.")
        
        except ValueError:
            print("❌ Invalid input. Please enter numbers only.")
    
    def view_cart(self):
        """Display items in shopping cart"""
        self.cart.display()
    
    def remove_from_cart(self):
        """Remove an item from cart"""
        if self.cart.is_empty():
            print("\n🛒 Cart is empty.")
            return
        
        self.cart.display()
        
        try:
            product_id = int(input("\nEnter product ID to remove: "))
            
            # Check if product exists in cart
            found = False
            for item in self.cart.items:
                if item['id'] == product_id:
                    found = True
                    item_name = item['name']
                    break
            
            if found:
                self.cart.remove_item(product_id)
                print(f"✅ '{item_name}' removed from cart.")
            else:
                print("❌ Product not found in cart.")
        
        except ValueError:
            print("❌ Invalid input.")
    
    def checkout(self):
        """Process checkout and place order"""
        if self.cart.is_empty():
            print("\n🛒 Cart is empty. Cannot checkout.")
            return
        
        print("\n---- CHECKOUT SUMMARY ----")
        
        # Create order
        order_id = self.order_repo.get_next_id()
        order = Order(order_id, self.user.name, self.user.phone, status="Completed")
        
        # Add items to order and update product quantities
        for cart_item in self.cart.items:
            # Create order item
            order_item = OrderItem(
                product_id=cart_item['id'],
                product_name=cart_item['name'],
                quantity=cart_item['qty'],
                price=cart_item['price']
            )
            order.add_item(order_item)
            
            # Display item
            print(f"{cart_item['name']} × {cart_item['qty']} = ₹{order_item.get_subtotal()}")
        
        print("-" * 40)
        print(f"Total Amount: ₹{order.calculate_total()}")
        
        confirm = input("\nConfirm order? (yes/no): ").lower()
        
        if confirm != "yes":
            print("❌ Order cancelled.")
            return
        
        # Update product quantities
        for cart_item in self.cart.items:
            product = self.product_repo.find_by_id(cart_item['id'])
            if product:
                product.reduce_stock(cart_item['qty'])
                self.product_repo.update_product(product)
        
        # Save order
        self.order_repo.save_order(order)
        
        print(f"\n✅ Order placed successfully! Order ID: {order_id}")
        print(f"Total Amount: ₹{order.calculate_total()}")
        print("Thank you for shopping with us! 🎉")
        
        # Clear cart
        self.cart.clear()
    
    def view_my_orders(self):
        """View all orders placed by the current user"""
        print("\n---- MY ORDERS ----")
        
        user_orders = self.order_repo.find_by_customer_phone(self.user.phone)
        
        if not user_orders:
            print("📦 No orders found.")
            return
        
        for order in user_orders:
            print(f"\nOrder ID: {order.order_id}")
            print(f"Date: {order.order_date}")
            print(f"Status: {order.status}")
            print("Items:")
            for item in order.items:
                print(f"  - {item.product_name} × {item.quantity} = ₹{item.get_subtotal()}")
            print(f"Total: ₹{order.calculate_total()}")
            print("-" * 40)


def user_menu(user):
    """Main menu for regular users - shopping functionality"""
    shopping_service = ShoppingService(user)
    
    while True:
        print("\n===== USER MENU =====")
        print("1. View Products")
        print("2. Add to Cart")
        print("3. View Cart")
        print("4. Remove from Cart")
        print("5. Checkout")
        print("6. View My Orders")
        print("7. Logout")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            shopping_service.view_products()
        elif choice == "2":
            shopping_service.add_to_cart()
        elif choice == "3":
            shopping_service.view_cart()
        elif choice == "4":
            shopping_service.remove_from_cart()
        elif choice == "5":
            shopping_service.checkout()
        elif choice == "6":
            shopping_service.view_my_orders()
        elif choice == "7":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")


# Legacy functions for backward compatibility
def load_products():
    """Load products (legacy function)"""
    repo = ProductRepository()
    products = repo.load_all()
    return [p.to_dict() for p in products]


def save_products(products):
    """Save products (legacy function)"""
    repo = ProductRepository()
    product_objects = [Product.from_dict(p) if isinstance(p, dict) else p for p in products]
    repo.save_all(product_objects)


def load_orders():
    """Load orders (legacy function)"""
    repo = OrderRepository()
    orders = repo.load_all()
    return [o.to_dict() for o in orders]


def save_order(order):
    """Save order (legacy function)"""
    repo = OrderRepository()
    order_obj = Order.from_dict(order) if isinstance(order, dict) else order
    repo.save_order(order_obj)


def view_products():
    """View products (legacy function)"""
    repo = ProductRepository()
    products = repo.load_all()
    print("\n---- AVAILABLE PRODUCTS ----")
    if not products:
        print("⚠️  No products available.")
        return
    for product in products:
        status = product.get_stock_status()
        print(f"ID: {product.id} | {product.name} | Category: {product.category} | Price: ₹{product.price} | Qty: {product.quantity} | {status}")


def view_my_orders(user):
    """View my orders (legacy function)"""
    repo = OrderRepository()
    user_orders = repo.find_by_customer_phone(user['phone'] if isinstance(user, dict) else user.phone)
    
    print("\n---- MY ORDERS ----")
    if not user_orders:
        print("📦 No orders found.")
        return
    
    for order in user_orders:
        print(f"\nOrder ID: {order.order_id}")
        print(f"Date: {order.order_date}")
        print(f"Status: {order.status}")
        print("Items:")
        for item in order.items:
            print(f"  - {item.product_name} × {item.quantity} = ₹{item.get_subtotal()}")
        print(f"Total: ₹{order.calculate_total()}")
        print("-" * 40)