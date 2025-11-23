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


SUPPLIER_FILE_PATH = "data/suppliers.json"
PRODUCT_FILE_PATH = "data/products.json"


def load_suppliers():
    """Load suppliers from JSON file."""
    if os.path.exists(SUPPLIER_FILE_PATH):
        with open(SUPPLIER_FILE_PATH, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []


def save_suppliers(suppliers):
    """Save updated suppliers to JSON."""
    with open(SUPPLIER_FILE_PATH, "w") as file:
        json.dump(suppliers, file, indent=4)


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


def add_supplier():
    """Add a new supplier to the system."""
    print("\n---- ADD SUPPLIER ----")
    
    name = get_validated_name("Supplier Name")
    contact_person = get_validated_name("Contact Person")
    phone = get_validated_phone()
    email = get_validated_email()
    address = sanitize_input(input("Enter address: "))
    products_supplied = input("Products Supplied (comma-separated): ")
    
    suppliers = load_suppliers()
    
    # Check if supplier already exists
    for supplier in suppliers:
        if supplier['phone'] == phone:
            print("❌ Supplier with this phone number already exists!")
            return
    
    # Auto assign ID
    supplier_id = len(suppliers) + 1
    
    new_supplier = {
        "id": supplier_id,
        "name": name,
        "contact_person": contact_person,
        "phone": phone,
        "email": email,
        "address": address,
        "products_supplied": [p.strip() for p in products_supplied.split(',')],
        "total_orders": 0,
        "total_amount": 0,
        "rating": 5.0,
        "status": "Active",
        "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    suppliers.append(new_supplier)
    save_suppliers(suppliers)
    
    print(f"\n✅ Supplier '{name}' added successfully!\n")


def view_suppliers():
    """Display all suppliers."""
    print("\n---- SUPPLIER LIST ----")
    suppliers = load_suppliers()
    
    if not suppliers:
        print("⚠ No suppliers found.")
        return
    
    for supplier in suppliers:
        status_icon = "✓" if supplier['status'] == "Active" else "✗"
        print(f"\nID: {supplier['id']} | {supplier['name']} {status_icon}")
        print(f"Contact: {supplier['contact_person']} | Phone: {supplier['phone']}")
        print(f"Email: {supplier['email']}")
        print(f"Products: {', '.join(supplier['products_supplied'])}")
        print(f"Total Orders: {supplier['total_orders']} | Total Amount: ₹{supplier['total_amount']:,.2f}")
        print(f"Rating: {supplier['rating']}/5.0 | Status: {supplier['status']}")
        print("-" * 60)


def update_supplier():
    """Update supplier details."""
    print("\n---- UPDATE SUPPLIER ----")
    suppliers = load_suppliers()
    
    if not suppliers:
        print("⚠ No suppliers found.")
        return
    
    view_suppliers()
    
    try:
        supplier_id = int(input("\nEnter Supplier ID to update: "))
        
        for supplier in suppliers:
            if supplier['id'] == supplier_id:
                print(f"\nUpdating: {supplier['name']}")
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
                    supplier['name'] = input("New Name: ")
                elif choice == "2":
                    supplier['contact_person'] = input("New Contact Person: ")
                elif choice == "3":
                    supplier['phone'] = input("New Phone: ")
                elif choice == "4":
                    supplier['email'] = input("New Email: ")
                elif choice == "5":
                    supplier['address'] = input("New Address: ")
                elif choice == "6":
                    products = input("New Products (comma-separated): ")
                    supplier['products_supplied'] = [p.strip() for p in products.split(',')]
                elif choice == "7":
                    rating = float(input("New Rating (0.0-5.0): "))
                    if 0 <= rating <= 5:
                        supplier['rating'] = rating
                    else:
                        print("❌ Invalid rating. Must be between 0 and 5.")
                        return
                elif choice == "8":
                    print("Status Options: Active / Inactive")
                    status = input("New Status: ")
                    if status in ["Active", "Inactive"]:
                        supplier['status'] = status
                    else:
                        print("❌ Invalid status.")
                        return
                else:
                    print("❌ Invalid choice.")
                    return
                
                save_suppliers(suppliers)
                print("\n✅ Supplier updated successfully!")
                return
        
        print("❌ Supplier ID not found.")
    
    except ValueError:
        print("❌ Invalid input.")


def delete_supplier():
    """Delete a supplier from the system."""
    print("\n---- DELETE SUPPLIER ----")
    suppliers = load_suppliers()
    
    if not suppliers:
        print("⚠ No suppliers found.")
        return
    
    view_suppliers()
    
    try:
        supplier_id = int(input("\nEnter Supplier ID to delete: "))
        
        for supplier in suppliers:
            if supplier['id'] == supplier_id:
                print(f"\nSupplier: {supplier['name']}")
                print(f"Contact: {supplier['phone']}")
                
                confirm = input("\nAre you sure you want to delete? (yes/no): ").lower()
                
                if confirm == "yes":
                    suppliers.remove(supplier)
                    save_suppliers(suppliers)
                    print("🗑️ Supplier deleted successfully!")
                else:
                    print("❌ Deletion cancelled.")
                return
        
        print("❌ Supplier ID not found.")
    
    except ValueError:
        print("❌ Invalid input.")


def record_purchase_order():
    """Record a purchase order from a supplier."""
    print("\n---- RECORD PURCHASE ORDER ----")
    
    suppliers = load_suppliers()
    products = load_products()
    
    if not suppliers:
        print("⚠ No suppliers found.")
        return
    
    if not products:
        print("⚠ No products found.")
        return
    
    view_suppliers()
    
    try:
        supplier_id = int(input("\nEnter Supplier ID: "))
        
        supplier = None
        for s in suppliers:
            if s['id'] == supplier_id:
                supplier = s
                break
        
        if not supplier:
            print("❌ Supplier not found.")
            return
        
        print(f"\nSupplier: {supplier['name']}")
        print("\nAvailable Products:")
        for p in products:
            print(f"ID: {p['id']} | {p['name']} | Current Stock: {p['quantity']}")
        
        product_id = int(input("\nEnter Product ID to restock: "))
        
        product = None
        for p in products:
            if p['id'] == product_id:
                product = p
                break
        
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
        print(f"Supplier: {supplier['name']}")
        print(f"Product: {product['name']}")
        print(f"Quantity: {quantity}")
        print(f"Price per Unit: ₹{price_per_unit}")
        print(f"Total Cost: ₹{total_cost:,.2f}")
        
        confirm = input("\nConfirm purchase order? (yes/no): ").lower()
        
        if confirm == "yes":
            # Update product stock
            product['quantity'] += quantity
            save_products(products)
            
            # Update supplier stats
            supplier['total_orders'] += 1
            supplier['total_amount'] += total_cost
            save_suppliers(suppliers)
            
            print(f"\n✅ Purchase order recorded successfully!")
            print(f"New stock for {product['name']}: {product['quantity']} units")
        else:
            print("❌ Purchase order cancelled.")
    
    except ValueError:
        print("❌ Invalid input.")


def supplier_performance_report():
    """Generate supplier performance analysis with charts."""
    print("\n---- SUPPLIER PERFORMANCE REPORT ----")
    
    suppliers = load_suppliers()
    
    if not suppliers:
        print("⚠ No suppliers found.")
        return
    
    active_suppliers = [s for s in suppliers if s['status'] == 'Active']
    inactive_suppliers = [s for s in suppliers if s['status'] == 'Inactive']
    
    print(f"\nTotal Suppliers: {len(suppliers)}")
    print(f"Active: {len(active_suppliers)}")
    print(f"Inactive: {len(inactive_suppliers)}")
    print(f"\n{'='*60}\n")
    
    # Sort by total amount
    sorted_suppliers = sorted(suppliers, key=lambda x: x['total_amount'], reverse=True)
    
    print("Top Suppliers by Purchase Volume:\n")
    for i, supplier in enumerate(sorted_suppliers[:10], 1):
        print(f"{i}. {supplier['name']}")
        print(f"   Total Orders: {supplier['total_orders']}")
        print(f"   Total Amount: ₹{supplier['total_amount']:,.2f}")
        print(f"   Rating: {supplier['rating']}/5.0")
        print(f"   Status: {supplier['status']}\n")
    
    # Visualizations
    visualize = input("Generate performance charts? (yes/no): ").lower()
    
    if visualize == "yes" and len(suppliers) > 0:
        # Chart 1: Top suppliers by spending
        top_5 = sorted_suppliers[:5]
        names = [s['name'] for s in top_5]
        amounts = [s['total_amount'] for s in top_5]
        
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
        ratings = [s['rating'] for s in top_5]
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
        order_counts = [s['total_orders'] for s in top_5]
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


def supplier_comparison():
    """Compare multiple suppliers using numpy statistics."""
    print("\n---- SUPPLIER COMPARISON ----")
    
    suppliers = load_suppliers()
    
    if len(suppliers) < 2:
        print("⚠ Need at least 2 suppliers for comparison.")
        return
    
    # Calculate statistics using numpy
    ratings = np.array([s['rating'] for s in suppliers])
    orders = np.array([s['total_orders'] for s in suppliers])
    amounts = np.array([s['total_amount'] for s in suppliers])
    
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
    """Main supplier management menu."""
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
            add_supplier()
        elif choice == "2":
            view_suppliers()
        elif choice == "3":
            update_supplier()
        elif choice == "4":
            delete_supplier()
        elif choice == "5":
            record_purchase_order()
        elif choice == "6":
            supplier_performance_report()
        elif choice == "7":
            supplier_comparison()
        elif choice == "8":
            break
        else:
            print("Invalid choice. Try again.")