import json
import os
from utils.validation import (
    get_validated_name,
    get_validated_category,
    get_validated_quantity,
    get_validated_price
)
from models.user import Product

PRODUCT_FILE_PATH = "data/products.json"


class ProductRepository:
    """Repository class for managing product data persistence"""
    
    def __init__(self, file_path=PRODUCT_FILE_PATH):
        self.file_path = file_path
    
    def load_all(self):
        """Load all products from JSON file"""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                try:
                    data = json.load(file)
                    return [Product.from_dict(product_data) for product_data in data]
                except json.JSONDecodeError:
                    return []
        return []
    
    def save_all(self, products):
        """Save all products to JSON file"""
        with open(self.file_path, "w") as file:
            product_dicts = [product.to_dict() for product in products]
            json.dump(product_dicts, file, indent=4)
    
    def find_by_id(self, product_id):
        """Find a product by ID"""
        products = self.load_all()
        for product in products:
            if product.id == product_id:
                return product
        return None
    
    def find_by_name(self, name):
        """Find a product by name (case-insensitive)"""
        products = self.load_all()
        for product in products:
            if product.name.lower() == name.lower():
                return product
        return None
    
    def add_product(self, product):
        """Add a new product"""
        products = self.load_all()
        products.append(product)
        self.save_all(products)
        return True
    
    def update_product(self, product):
        """Update an existing product"""
        products = self.load_all()
        for i, p in enumerate(products):
            if p.id == product.id:
                products[i] = product
                self.save_all(products)
                return True
        return False
    
    def delete_product(self, product_id):
        """Delete a product by ID"""
        products = self.load_all()
        products = [p for p in products if p.id != product_id]
        self.save_all(products)
        return True
    
    def get_next_id(self):
        """Get the next available product ID"""
        products = self.load_all()
        if not products:
            return 1
        return max(p.id for p in products) + 1


class ProductService:
    """Service class for product management operations"""
    
    def __init__(self):
        self.product_repo = ProductRepository()
    
    def add_product(self):
        """Add a new product to the system"""
        print("\n---- ADD PRODUCT ----")
        name = get_validated_name("Product Name")
        
        # Check for duplicate name
        if self.product_repo.find_by_name(name):
            print(f"\n❌ Product with name '{name}' already exists! Please use a different name.\n")
            return
        
        category = get_validated_category()
        quantity = get_validated_quantity()
        price = get_validated_price()
        
        # Get next available ID
        product_id = self.product_repo.get_next_id()
        
        # Create new product object
        new_product = Product(product_id, name, category, quantity, price)
        
        # Save product
        self.product_repo.add_product(new_product)
        
        print(f"\n✅ Product '{name}' added successfully!\n")
    
    def view_products(self):
        """Display all available products"""
        print("\n---- PRODUCT LIST ----")
        products = self.product_repo.load_all()
        
        if not products:
            print("⚠️  No products available.")
            return
        
        for product in products:
            print(f"ID: {product.id} | {product.name} | Qty: {product.quantity} | Price: ₹{product.price}")
    
    def update_product(self):
        """Update product details"""
        print("\n---- UPDATE PRODUCT ----")
        products = self.product_repo.load_all()
        
        if not products:
            print("⚠️  No products available.")
            return
        
        self.view_products()
        
        prod_id = int(input("\nEnter Product ID to update: "))
        
        product = self.product_repo.find_by_id(prod_id)
        
        if not product:
            print("❌ Product ID not found.")
            return
        
        print("\nWhat do you want to update?")
        print("1. Name\n2. Category\n3. Quantity\n4. Price")
        choice = input("Enter choice: ")
        
        if choice == "1":
            new_name = input("New Name: ")
            # Check if new name already exists
            existing = self.product_repo.find_by_name(new_name)
            if existing and existing.id != prod_id:
                print(f"\n❌ Product with name '{new_name}' already exists! Please use a different name.")
                return
            product.name = new_name
        
        elif choice == "2":
            product.category = input("New Category: ")
        
        elif choice == "3":
            product.quantity = int(input("New Quantity: "))
        
        elif choice == "4":
            product.price = float(input("New Price: "))
        
        else:
            print("❌ Invalid choice.")
            return
        
        self.product_repo.update_product(product)
        print("\n✅ Product updated successfully!")
    
    def delete_product(self):
        """Delete a product by ID"""
        print("\n---- DELETE PRODUCT ----")
        products = self.product_repo.load_all()
        
        if not products:
            print("⚠️  No products available.")
            return
        
        self.view_products()
        
        prod_id = int(input("\nEnter Product ID to delete: "))
        
        product = self.product_repo.find_by_id(prod_id)
        
        if product:
            self.product_repo.delete_product(prod_id)
            print("\n🗑️ Product deleted successfully!")
        else:
            print("❌ Product not found.")


# Legacy functions for backward compatibility
def load_products():
    """Load products from JSON (legacy function)"""
    repo = ProductRepository()
    products = repo.load_all()
    return [product.to_dict() for product in products]


def save_products(products):
    """Save products to JSON (legacy function)"""
    repo = ProductRepository()
    product_objects = [Product.from_dict(p) if isinstance(p, dict) else p for p in products]
    repo.save_all(product_objects)


def add_product():
    """Add product (legacy function)"""
    service = ProductService()
    service.add_product()


def view_products():
    """View products (legacy function)"""
    service = ProductService()
    service.view_products()


def update_product():
    """Update product (legacy function)"""
    service = ProductService()
    service.update_product()


def delete_product():
    """Delete product (legacy function)"""
    service = ProductService()
    service.delete_product()