import json
import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from utils.validation import (
    get_validated_name,
    get_validated_phone,
    get_validated_email,
    sanitize_input
)
from models.user import Supplier, Product

SUPPLIER_FILE_PATH = "data/suppliers.json"
PRODUCT_FILE_PATH = "data/products.json"


class SupplierRepository:
    """Repository for supplier data persistence"""
    
    def __init__(self, file_path=SUPPLIER_FILE_PATH):
        self.file_path = file_path
    
    def load_all(self):
        """Load all suppliers"""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                try:
                    data = json.load(file)
                    return [Supplier.from_dict(s) for s in data]
                except json.JSONDecodeError:
                    return []
        return []
    
    def save_all(self, suppliers):
        """Save all suppliers"""
        with open(self.file_path, "w") as file:
            supplier_dicts = [s.to_dict() for s in suppliers]
            json.dump(supplier_dicts, file, indent=4)
    
    def find_by_id(self, supplier_id):
        """Find supplier by ID"""
        suppliers = self.load_all()
        for s in suppliers:
            if s.id == supplier_id:
                return s
        return None
    
    def find_by_phone(self, phone):
        """Find supplier by phone"""
        suppliers = self.load_all()
        for s in suppliers:
            if s.phone == phone:
                return s
        return None
    
    def add_supplier(self, supplier):
        """Add new supplier"""
        suppliers = self.load_all()
        suppliers.append(supplier)
        self.save_all(suppliers)
        return True
    
    def update_supplier(self, supplier):
        """Update existing supplier"""
        suppliers = self.load_all()
        for i, s in enumerate(suppliers):
            if s.id == supplier.id:
                suppliers[i] = supplier
                self.save_all(suppliers)
                return True
        return False
    
    def delete_supplier(self, supplier_id):
        """Delete supplier"""
        suppliers = self.load_all()
        suppliers = [s for s in suppliers if s.id != supplier_id]
        self.save_all(suppliers)
        return True
    
    def get_next_id(self):
        """Get next supplier ID"""
        suppliers = self.load_all()
        if not suppliers:
            return 1
        return max(s.id for s in suppliers) + 1


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
        """Update product"""
        products = self.load_all()
        for i, p in enumerate(products):
            if p.id == product.id:
                products[i] = product
                self.save_all(products)
                return True
        return False


class SupplierService:
    """Service for supplier management operations"""
    
    def __init__(self):
        self.supplier_repo = SupplierRepository()
        self.product_repo = ProductRepository()
    
    def add_supplier(self):
        """Add a new supplier"""
        print("\n---- ADD SUPPLIER ----")
        
        name = get_validated_name("Supplier Name")
        contact_person = get_validated_name("Contact Person")
        phone = get_validated_phone()
        email = get_validated_email()
        address = sanitize_input(input("Enter address: "))
        products_supplied = input("Products Supplied (comma-separated): ")
        
        # Check if supplier already exists
        if self.supplier_repo.find_by_phone(phone):
            print("❌ Supplier with this phone number already exists!")
            return
        
        # Get next ID
        supplier_id = self.supplier_repo.get_next_id()
        
        # Create supplier object
        new_supplier = Supplier(
            id=supplier_id,
            name=name,
            contact_person=contact_person,
            phone=phone,
            email=email,
            address=address,
            products_supplied=[p.strip() for p in products_supplied.split(',')]
        )
        
        # Save supplier
        self.supplier_repo.add_supplier(new_supplier)
        
        print(f"\n✅ Supplier '{name}' added successfully!\n")
    
    def view_suppliers(self):
        """Display all suppliers"""
        print("\n---- SUPPLIER LIST ----")
        suppliers = self.supplier_repo.load_all()
        
        if not suppliers:
            print("⚠️  No suppliers found.")
            return
        
        for supplier in suppliers:
            status_icon = "✓" if supplier.is_active() else "✗"
            print(f"\nID: {supplier.id} | {supplier.name} {status_icon}")
            print(f"Contact: {supplier.contact_person} | Phone: {supplier.phone}")
            print(f"Email: {supplier.email}")
            print(f"Products: {', '.join(supplier.products_supplied)}")
            print(f"Total Orders: {supplier.total_orders} | Total Amount: ₹{supplier.total_amount:,.2f}")
            print(f"Rating: {supplier.rating}/5.0 | Status: {supplier.status}")
            print("-" * 60)
    
    def update_supplier(self):
        """Update supplier details"""
        print("\n---- UPDATE SUPPLIER ----")
        suppliers = self.supplier_repo.load_all()
        
        if not suppliers:
            print("⚠️  No suppliers found.")
            return
        
        self.view_suppliers()
        
        try:
            supplier_id = int(input("\nEnter Supplier ID to update: "))
            
            supplier = self.supplier_repo.find_by_id(supplier_id)
            
            if not supplier:
                print("❌ Supplier ID not found.")
                return
            
            print(f"\nUpdating: {supplier.name}")
            print("\nWhat do you want to update?")
            print("1. Name")
            print("2. Contact Person")
            print("3. Phone")
            print("4. Email")
            print("5. Address")
            print("6. Products Supplied")
            print("7. Rating")
            print("8. Status")
            
            choice = input("\nEnter choice: ")
            
            if choice == "1":
                supplier.name = input("New Name: ")
            elif choice == "2":
                supplier.contact_person = input("New Contact Person: ")
            elif choice == "3":
                supplier.phone = input("New Phone: ")
            elif choice == "4":
                supplier.email = input("New Email: ")
            elif choice == "5":
                supplier.address = input("New Address: ")
            elif choice == "6":
                products = input("New Products (comma-separated): ")
                supplier.products_supplied = [p.strip() for p in products.split(',')]
            elif choice == "7":
                rating = float(input("New Rating (0.0-5.0): "))
                if not supplier.update_rating(rating):
                    print("❌ Invalid rating. Must be between 0 and 5.")
                    return
            elif choice == "8":
                print("Status Options: Active / Inactive")
                status = input("New Status: ")
                if status in ["Active", "Inactive"]:
                    supplier.status = status
                else:
                    print("❌ Invalid status.")
                    return
            else:
                print("❌ Invalid choice.")
                return
            
            self.supplier_repo.update_supplier(supplier)
            print("\n✅ Supplier updated successfully!")
        
        except ValueError:
            print("❌ Invalid input.")
    
    def delete_supplier(self):
        """Delete a supplier"""
        print("\n---- DELETE SUPPLIER ----")
        suppliers = self.supplier_repo.load_all()
        
        if not suppliers:
            print("⚠️  No suppliers found.")
            return
        
        self.view_suppliers()
        
        try:
            supplier_id = int(input("\nEnter Supplier ID to delete: "))
            
            supplier = self.supplier_repo.find_by_id(supplier_id)
            
            if not supplier:
                print("❌ Supplier ID not found.")
                return
            
            print(f"\nSupplier: {supplier.name}")
            print(f"Contact: {supplier.phone}")
            
            confirm = input("\nAre you sure you want to delete? (yes/no): ").lower()
            
            if confirm == "yes":
                self.supplier_repo.delete_supplier(supplier_id)
                print("🗑️ Supplier deleted successfully!")
            else:
                print("❌ Deletion cancelled.")
        
        except ValueError:
            print("❌ Invalid input.")
    
    def record_purchase_order(self):
        """Record a purchase order from supplier"""
        print("\n---- RECORD PURCHASE ORDER ----")
        
        suppliers = self.supplier_repo.load_all()
        products = self.product_repo.load_all()
        
        if not suppliers:
            print("⚠️  No suppliers found.")
            return
        
        if not products:
            print("⚠️  No products found.")
            return
        
        self.view_suppliers()
        
        try:
            supplier_id = int(input("\nEnter Supplier ID: "))
            
            supplier = self.supplier_repo.find_by_id(supplier_id)
            
            if not supplier:
                print("❌ Supplier not found.")
                return
            
            print(f"\nSupplier: {supplier.name}")
            print("\nAvailable Products:")
            for p in products:
                print(f"ID: {p.id} | {p.name} | Current Stock: {p.quantity}")
            
            product_id = int(input("\nEnter Product ID to restock: "))
            
            product = self.product_repo.find_by_id(product_id)
            
            if not product:
                print("❌ Product not found.")
                return
            
            quantity = int(input(f"Enter quantity to purchase: "))
            price_per_unit = float(input(f"Enter price per unit: "))
            
            if quantity <= 0 or price_per_unit <= 0:
                print("❌ Invalid quantity or price.")
                return
            
            total_cost = quantity * price_per_unit
            
            print(f"\n---- PURCHASE ORDER SUMMARY ----")
            print(f"Supplier: {supplier.name}")
            print(f"Product: {product.name}")
            print(f"Quantity: {quantity}")
            print(f"Price per Unit: ₹{price_per_unit}")
            print(f"Total Cost: ₹{total_cost:,.2f}")
            
            confirm = input("\nConfirm purchase order? (yes/no): ").lower()
            
            if confirm == "yes":
                # Update product stock
                product.restock(quantity)
                self.product_repo.update_product(product)
                
                # Update supplier stats
                supplier.record_purchase(total_cost)
                self.supplier_repo.update_supplier(supplier)
                
                print(f"\n✅ Purchase order recorded successfully!")
                print(f"New stock for {product.name}: {product.quantity} units")
            else:
                print("❌ Purchase order cancelled.")
        
        except ValueError:
            print("❌ Invalid input.")
    
    def supplier_performance_report(self):
        """Generate supplier performance report with charts"""
        print("\n---- SUPPLIER PERFORMANCE REPORT ----")
        
        suppliers = self.supplier_repo.load_all()
        
        if not suppliers:
            print("⚠️  No suppliers found.")
            return
        
        active_suppliers = [s for s in suppliers if s.is_active()]
        inactive_suppliers = [s for s in suppliers if not s.is_active()]
        
        print(f"\nTotal Suppliers: {len(suppliers)}")
        print(f"Active: {len(active_suppliers)}")
        print(f"Inactive: {len(inactive_suppliers)}")
        print(f"\n{'='*60}\n")
        
        # Sort by total amount
        sorted_suppliers = sorted(suppliers, key=lambda x: x.total_amount, reverse=True)
        
        print("Top Suppliers by Purchase Volume:\n")
        for i, supplier in enumerate(sorted_suppliers[:10], 1):
            print(f"{i}. {supplier.name}")
            print(f"   Total Orders: {supplier.total_orders}")
            print(f"   Total Amount: ₹{supplier.total_amount:,.2f}")
            print(f"   Rating: {supplier.rating}/5.0")
            print(f"   Status: {supplier.status}\n")
        
        # Visualizations
        visualize = input("Generate performance charts? (yes/no): ").lower()
        
        if visualize == "yes" and len(suppliers) > 0:
            # Chart 1: Top suppliers by spending
            top_5 = sorted_suppliers[:5]
            names = [s.name for s in top_5]
            amounts = [s.total_amount for s in top_5]
            
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            fig.suptitle('Supplier Performance Analysis', fontsize=16, fontweight='bold')
            
            # Bar chart - Top suppliers
            axes[0, 0].bar(names, amounts, color='teal', edgecolor='black')
            axes[0, 0].set_title('Top 5 Suppliers by Purchase Volume', fontweight='bold')
            axes[0, 0].set_ylabel('Total Amount (₹)')
            axes[0, 0].tick_params(axis='x', rotation=45)
            for i, (name, amount) in enumerate(zip(names, amounts)):
                axes[0, 0].text(i, amount, f'₹{amount:,.0f}', 
                              ha='center', va='bottom', fontsize=9)
            
            # Rating comparison
            ratings = [s.rating for s in top_5]
            axes[0, 1].barh(names, ratings, color='gold', edgecolor='orange')
            axes[0, 1].set_title('Supplier Ratings', fontweight='bold')
            axes[0, 1].set_xlabel('Rating (out of 5)')
            axes[0, 1].set_xlim(0, 5)
            for i, (name, rating) in enumerate(zip(names, ratings)):
                axes[0, 1].text(rating, i, f'{rating:.1f}', 
                              ha='left', va='center', fontsize=9)
            
            # Status distribution pie chart
            status_counts = [len(active_suppliers), len(inactive_suppliers)]
            status_labels = ['Active', 'Inactive']
            colors = ['lightgreen', 'lightcoral']
            axes[1, 0].pie(status_counts, labels=status_labels, autopct='%1.1f%%',
                          colors=colors, startangle=90, shadow=True)
            axes[1, 0].set_title('Supplier Status Distribution', fontweight='bold')
            
            # Order frequency
            order_counts = [s.total_orders for s in top_5]
            axes[1, 1].plot(names, order_counts, marker='o', linewidth=2,
                           markersize=8, color='purple', markerfacecolor='pink')
            axes[1, 1].set_title('Order Frequency (Top 5 Suppliers)', fontweight='bold')
            axes[1, 1].set_ylabel('Number of Orders')
            axes[1, 1].tick_params(axis='x', rotation=45)
            axes[1, 1].grid(True, alpha=0.3)
            for i, (name, count) in enumerate(zip(names, order_counts)):
                axes[1, 1].text(i, count, f'{count}', 
                              ha='center', va='bottom', fontsize=9)
            
            plt.tight_layout()
            plt.show()
    
    def supplier_comparison(self):
        """Compare multiple suppliers using numpy statistics"""
        print("\n---- SUPPLIER COMPARISON ----")
        
        suppliers = self.supplier_repo.load_all()
        
        if len(suppliers) < 2:
            print("⚠️  Need at least 2 suppliers for comparison.")
            return
        
        # Calculate statistics using numpy
        ratings = np.array([s.rating for s in suppliers])
        orders = np.array([s.total_orders for s in suppliers])
        amounts = np.array([s.total_amount for s in suppliers])
        
        print("\n---- STATISTICAL ANALYSIS ----\n")
        
        print("Ratings:")
        print(f"  Average: {np.mean(ratings):.2f}")
        print(f"  Median: {np.median(ratings):.2f}")
        print(f"  Std Deviation: {np.std(ratings):.2f}")
        print(f"  Min: {np.min(ratings):.2f} | Max: {np.max(ratings):.2f}")
        
        print("\nTotal Orders:")
        print(f"  Average: {np.mean(orders):.2f}")
        print(f"  Median: {np.median(orders):.2f}")
        print(f"  Total: {np.sum(orders)}")
        
        print("\nTotal Amount Spent:")
        print(f"  Average: ₹{np.mean(amounts):,.2f}")
        print(f"  Median: ₹{np.median(amounts):,.2f}")
        print(f"  Total: ₹{np.sum(amounts):,.2f}")
        print(f"  Std Deviation: ₹{np.std(amounts):,.2f}")


def supplier_menu():
    """Main supplier management menu"""
    service = SupplierService()
    
    while True:
        print("\n========== SUPPLIER MANAGEMENT ==========")
        print("1. Add Supplier")
        print("2. View Suppliers")
        print("3. Update Supplier")
        print("4. Delete Supplier")
        print("5. Record Purchase Order")
        print("6. Supplier Performance Report")
        print("7. Supplier Comparison (Stats)")
        print("8. Back to Admin Menu")
        
        choice = input("\nEnter choice: ")
        
        if choice == "1":
            service.add_supplier()
        elif choice == "2":
            service.view_suppliers()
        elif choice == "3":
            service.update_supplier()
        elif choice == "4":
            service.delete_supplier()
        elif choice == "5":
            service.record_purchase_order()
        elif choice == "6":
            service.supplier_performance_report()
        elif choice == "7":
            service.supplier_comparison()
        elif choice == "8":
            break
        else:
            print("Invalid choice. Try again.")


# Legacy functions
def load_suppliers():
    repo = SupplierRepository()
    suppliers = repo.load_all()
    return [s.to_dict() for s in suppliers]


def save_suppliers(suppliers):
    repo = SupplierRepository()
    supplier_objects = [Supplier.from_dict(s) if isinstance(s, dict) else s for s in suppliers]
    repo.save_all(supplier_objects)


def load_products():
    repo = ProductRepository()
    products = repo.load_all()
    return [p.to_dict() for p in products]


def save_products(products):
    repo = ProductRepository()
    product_objects = [Product.from_dict(p) if isinstance(p, dict) else p for p in products]
    repo.save_all(product_objects)