import json
import os
from datetime import datetime
from utils.validation import get_validated_quantity

PRODUCT_FILE_PATH = "data/products.json"
ORDER_FILE_PATH = "data/orders.json"


def load_products():
    """Load products from JSON file."""
    if os.path.exists(PRODUCT_FILE_PATH):
        with open(PRODUCT_FILE_PATH, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []


def save_products(products):
    """Save updated products to JSON."""
    with open(PRODUCT_FILE_PATH, "w") as file:
        json.dump(products, file, indent=4)


def load_orders():
    """Load orders from JSON file."""
    if os.path.exists(ORDER_FILE_PATH):
        with open(ORDER_FILE_PATH, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []


def save_order(order):
    """Save a new order to orders.json."""
    orders = load_orders()
    orders.append(order)
    with open(ORDER_FILE_PATH, "w") as file:
        json.dump(orders, file, indent=4)


def user_menu(user):
    """Main menu for regular users - shopping functionality."""
    cart = []

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
            view_products()
        elif choice == "2":
            add_to_cart(cart)
        elif choice == "3":
            view_cart(cart)
        elif choice == "4":
            remove_from_cart(cart)
        elif choice == "5":
            checkout(cart, user)
        elif choice == "6":
            view_my_orders(user)
        elif choice == "7":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")


def view_products():
    """Display all available products."""
    print("\n---- AVAILABLE PRODUCTS ----")
    products = load_products()
    
    if not products:
        print("⚠ No products available.")
        return
    
    for item in products:
        status = "✓ In Stock" if item['quantity'] > 0 else "✗ Out of Stock"
        print(f"ID: {item['id']} | {item['name']} | Category: {item['category']} | Price: ₹{item['price']} | Qty: {item['quantity']} | {status}")


def add_to_cart(cart):
    """Add a product to shopping cart."""
    products = load_products()
    
    if not products:
        print("\n⚠ No products available.")
        return
    
    try:
        product_id = int(input("\nEnter product ID to add: "))
        
        # Find product
        product = None
        for p in products:
            if p['id'] == product_id:
                product = p
                break
        
        if not product:
            print("❌ Invalid product ID.")
            return
        
        if product['quantity'] <= 0:
            print(f"❌ Sorry, '{product['name']}' is out of stock.")
            return
        
        quantity = get_validated_quantity()
        if quantity > product['quantity']:
            print(f"❌ Not enough stock. Only {product['quantity']} available.")
        return
        
    
        # Check if product already in cart
        found = False
        for item in cart:
            if item['id'] == product_id:
                item['qty'] += quantity
                found = True
                print(f"✅ Updated quantity in cart. Total: {item['qty']}")
                break
        
        if not found:
            cart.append({
                "id": product_id,
                "name": product['name'],
                "price": product['price'],
                "qty": quantity
            })
            print(f"✅ '{product['name']}' added to cart.")
    
    except ValueError:
        print("❌ Invalid input. Please enter numbers only.")


def view_cart(cart):
    """Display items in shopping cart."""
    print("\n---- YOUR CART ----")
    
    if not cart:
        print("🛒 Cart is empty.")
        return
    
    total = 0
    for item in cart:
        subtotal = item['price'] * item['qty']
        total += subtotal
        print(f"ID: {item['id']} | {item['name']} × {item['qty']} = ₹{subtotal}")
    
    print("-" * 40)
    print(f"Total: ₹{total}")


def remove_from_cart(cart):
    """Remove an item from cart."""
    if not cart:
        print("\n🛒 Cart is empty.")
        return
    
    view_cart(cart)
    
    try:
        product_id = int(input("\nEnter product ID to remove: "))
        
        for item in cart:
            if item['id'] == product_id:
                cart.remove(item)
                print(f"✅ '{item['name']}' removed from cart.")
                return
        
        print("❌ Product not found in cart.")
    
    except ValueError:
        print("❌ Invalid input.")


def checkout(cart, user):
    """Process checkout and place order."""
    if not cart:
        print("\n🛒 Cart is empty. Cannot checkout.")
        return
    
    print("\n---- CHECKOUT SUMMARY ----")
    products = load_products()
    total = 0
    order_items = []
    
    # Calculate total and prepare order items
    for item in cart:
        subtotal = item['price'] * item['qty']
        total += subtotal
        print(f"{item['name']} × {item['qty']} = ₹{subtotal}")
        order_items.append({
            "product_id": item['id'],
            "product_name": item['name'],
            "quantity": item['qty'],
            "price": item['price'],
            "subtotal": subtotal
        })
    
    print("-" * 40)
    print(f"Total Amount: ₹{total}")
    
    confirm = input("\nConfirm order? (yes/no): ").lower()
    
    if confirm != "yes":
        print("❌ Order cancelled.")
        return
    
    # Update product quantities
    for item in cart:
        for product in products:
            if product['id'] == item['id']:
                product['quantity'] -= item['qty']
                break
    
    save_products(products)
    
    # Create order record
    orders = load_orders()
    order_id = len(orders) + 1
    
    order = {
        "order_id": order_id,
        "customer_name": user['name'],
        "customer_phone": user['phone'],
        "items": order_items,
        "total_amount": total,
        "order_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Completed"
    }
    
    save_order(order)
    
    print(f"\n✅ Order placed successfully! Order ID: {order_id}")
    print(f"Total Amount: ₹{total}")
    print("Thank you for shopping with us! 🎉")
    
    cart.clear()


def view_my_orders(user):
    """View all orders placed by the current user."""
    print("\n---- MY ORDERS ----")
    orders = load_orders()
    
    user_orders = [order for order in orders if order.get('customer_phone') == user['phone']]
    
    if not user_orders:
        print("📦 No orders found.")
        return
    
    for order in user_orders:
        print(f"\nOrder ID: {order['order_id']}")
        print(f"Date: {order['order_date']}")
        print(f"Status: {order['status']}")
        print("Items:")
        for item in order['items']:
            print(f"  - {item['product_name']} × {item['quantity']} = ₹{item['subtotal']}")
        print(f"Total: ₹{order['total_amount']}")
        print("-" * 40)