import json
import os
from utils.validation import (
    get_validated_name,
    get_validated_category,
    get_validated_quantity,
    get_validated_price
)

PRODUCT_FILE_PATH = "data/products.json"


def load_products():
    """Load product data from JSON file."""
    if os.path.exists(PRODUCT_FILE_PATH):
        with open(PRODUCT_FILE_PATH, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []


def save_products(products):
    """Save updated product data to JSON."""
    with open(PRODUCT_FILE_PATH, "w") as file:
        json.dump(products, file, indent=4)


def product_name_exists(products, name, exclude_id=None):
    """Check if a product with the given name already exists (case-insensitive)."""
    for product in products:
        if product["name"].lower() == name.lower():
            if exclude_id is None or product["id"] != exclude_id:
                return True
    return False


def add_product():
    """Add a new product to the system."""
    print("\n---- ADD PRODUCT ----")
    name = get_validated_name("Product Name")
    
    products = load_products()
    
    # Check for duplicate name
    if product_name_exists(products, name):
        print(f"\n❌ Product with name '{name}' already exists! Please use a different name.\n")
        return
    
    category = get_validated_category()
    quantity = get_validated_quantity()
    price = get_validated_price()

    # Auto assign ID (increment)
    product_id = len(products) + 1

    new_product = {
        "id": product_id,
        "name": name,
        "category": category,
        "quantity": quantity,
        "price": price
    }

    products.append(new_product)
    save_products(products)

    print(f"\n✅ Product '{name}' added successfully!\n")


def view_products():
    """Display all available products."""
    print("\n---- PRODUCT LIST ----")
    products = load_products()

    if not products:
        print("⚠ No products available.")
        return

    for item in products:
        print(f"ID: {item['id']} | {item['name']} | Qty: {item['quantity']} | Price: ₹{item['price']}")


def update_product():
    """Update product details such as name, price, or quantity."""
    print("\n---- UPDATE PRODUCT ----")
    products = load_products()

    if not products:
        print("⚠ No products available.")
        return

    view_products()

    prod_id = int(input("\nEnter Product ID to update: "))

    for product in products:
        if product["id"] == prod_id:
            print("\nWhat do you want to update?")
            print("1. Name\n2. Category\n3. Quantity\n4. Price")
            choice = input("Enter choice: ")

            if choice == "1":
                new_name = input("New Name: ")
                # Check if new name already exists (excluding current product)
                if product_name_exists(products, new_name, exclude_id=prod_id):
                    print(f"\n❌ Product with name '{new_name}' already exists! Please use a different name.")
                    return
                product["name"] = new_name

            elif choice == "2":
                product["category"] = input("New Category: ")

            elif choice == "3":
                product["quantity"] = int(input("New Quantity: "))

            elif choice == "4":
                product["price"] = float(input("New Price: "))

            else:
                print("❌ Invalid choice.")
                return

            save_products(products)
            print("\n✅ Product updated successfully!")
            return

    print("❌ Product ID not found.")


def delete_product():
    """Delete a product by ID."""
    print("\n---- DELETE PRODUCT ----")
    products = load_products()

    if not products:
        print("⚠ No products available.")
        return

    view_products()

    prod_id = int(input("\nEnter Product ID to delete: "))

    for p in products:
        if p["id"] == prod_id:
            products.remove(p)
            save_products(products)
            print("\n🗑 Product deleted successfully!")
            return

    print("❌ Product not found.")