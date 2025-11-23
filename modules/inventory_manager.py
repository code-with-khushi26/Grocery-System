import json
import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

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


def check_low_stock():
    """Display products with low stock levels."""
    print("\n---- LOW STOCK ALERT ----")
    
    products = load_products()
    
    if not products:
        print("⚠ No products found.")
        return
    
    low_stock_threshold = int(input("Enter low stock threshold (default 10): ") or "10")
    
    low_stock_items = []
    out_of_stock = []
    
    for product in products:
        if product['quantity'] == 0:
            out_of_stock.append(product)
        elif product['quantity'] < low_stock_threshold:
            low_stock_items.append(product)
    
    if out_of_stock:
        print("\n🚨 OUT OF STOCK:")
        for p in out_of_stock:
            print(f"  ❌ ID: {p['id']} | {p['name']} | Qty: {p['quantity']}")
    
    if low_stock_items:
        print(f"\n⚠️  LOW STOCK (< {low_stock_threshold} units):")
        for p in low_stock_items:
            print(f"  ⚠️  ID: {p['id']} | {p['name']} | Qty: {p['quantity']}")
    
    if not out_of_stock and not low_stock_items:
        print("✅ All products have adequate stock levels!")
    
    total_critical = len(out_of_stock) + len(low_stock_items)
    print(f"\nTotal Critical Items: {total_critical}")


def restock_product():
    """Restock a specific product."""
    print("\n---- RESTOCK PRODUCT ----")
    
    products = load_products()
    
    if not products:
        print("⚠ No products found.")
        return
    
    print("\nCurrent Inventory:")
    for p in products:
        status = "✓" if p['quantity'] > 10 else "⚠️"
        print(f"{status} ID: {p['id']} | {p['name']} | Stock: {p['quantity']}")
    
    try:
        product_id = int(input("\nEnter Product ID to restock: "))
        
        product = None
        for p in products:
            if p['id'] == product_id:
                product = p
                break
        
        if not product:
            print("❌ Product not found.")
            return
        
        print(f"\nProduct: {product['name']}")
        print(f"Current Stock: {product['quantity']}")
        
        quantity = int(input("Enter quantity to add: "))
        
        if quantity <= 0:
            print("❌ Quantity must be greater than 0.")
            return
        
        product['quantity'] += quantity
        save_products(products)
        
        print(f"\n✅ Restocked successfully!")
        print(f"New stock level: {product['quantity']} units")
    
    except ValueError:
        print("❌ Invalid input.")


def bulk_restock():
    """Restock multiple products at once."""
    print("\n---- BULK RESTOCK ----")
    
    products = load_products()
    
    if not products:
        print("⚠ No products found.")
        return
    
    print("\nProducts requiring restock:")
    low_stock = [p for p in products if p['quantity'] < 10]
    
    if not low_stock:
        print("✅ No products need restocking!")
        return
    
    for p in low_stock:
        print(f"ID: {p['id']} | {p['name']} | Stock: {p['quantity']}")
    
    print("\nEnter restock quantities (or 0 to skip):")
    
    for product in low_stock:
        try:
            qty = int(input(f"{product['name']} (current: {product['quantity']}): ") or "0")
            if qty > 0:
                product['quantity'] += qty
                print(f"  ✅ Added {qty} units. New stock: {product['quantity']}")
        except ValueError:
            print(f"  ⚠️  Skipped {product['name']}")
    
    save_products(products)
    print("\n✅ Bulk restock completed!")


def inventory_value_analysis():
    """Calculate total inventory value with numpy analysis."""
    print("\n---- INVENTORY VALUE ANALYSIS ----")
    
    products = load_products()
    
    if not products:
        print("⚠ No products found.")
        return
    
    # Calculate values
    product_values = []
    total_value = 0
    
    print("\nProduct-wise Inventory Value:\n")
    for p in products:
        value = p['quantity'] * p['price']
        product_values.append(value)
        total_value += value
        print(f"{p['name']}: {p['quantity']} × ₹{p['price']} = ₹{value:,.2f}")
    
    print(f"\n{'='*50}")
    print(f"Total Inventory Value: ₹{total_value:,.2f}")
    print(f"{'='*50}\n")
    
    # Numpy statistical analysis
    if product_values:
        values_array = np.array(product_values)
        
        print("Statistical Analysis:")
        print(f"  Average Product Value: ₹{np.mean(values_array):,.2f}")
        print(f"  Median Product Value: ₹{np.median(values_array):,.2f}")
        print(f"  Highest Value: ₹{np.max(values_array):,.2f}")
        print(f"  Lowest Value: ₹{np.min(values_array):,.2f}")
        print(f"  Standard Deviation: ₹{np.std(values_array):,.2f}")
        
        # Value distribution
        visualize = input("\nGenerate value distribution chart? (yes/no): ").lower()
        
        if visualize == "yes":
            names = [p['name'] for p in products]
            values = product_values
            
            # Sort by value
            sorted_data = sorted(zip(names, values), key=lambda x: x[1], reverse=True)
            names_sorted = [x[0] for x in sorted_data[:10]]
            values_sorted = [x[1] for x in sorted_data[:10]]
            
            plt.figure(figsize=(12, 6))
            bars = plt.barh(names_sorted, values_sorted, color='mediumseagreen', edgecolor='darkgreen')
            plt.xlabel('Inventory Value (₹)', fontsize=12, fontweight='bold')
            plt.ylabel('Products', fontsize=12, fontweight='bold')
            plt.title('Top 10 Products by Inventory Value', fontsize=14, fontweight='bold')
            
            # Add value labels
            for i, bar in enumerate(bars):
                width = bar.get_width()
                plt.text(width, bar.get_y() + bar.get_height()/2.,
                        f'₹{width:,.0f}', ha='left', va='center', fontsize=9)
            
            plt.tight_layout()
            plt.show()


def stock_turnover_analysis():
    """Analyze stock turnover rate using sales data."""
    print("\n---- STOCK TURNOVER ANALYSIS ----")
    
    products = load_products()
    orders = load_orders()
    
    if not products or not orders:
        print("⚠ Insufficient data for analysis.")
        return
    
    # Calculate units sold per product
    from collections import defaultdict
    units_sold = defaultdict(int)
    
    for order in orders:
        if order.get('status') in ['Completed', 'Delivered']:
            for item in order['items']:
                units_sold[item['product_id']] += item['quantity']
    
    print("\nProduct Turnover Analysis:\n")
    
    turnover_data = []
    for p in products:
        sold = units_sold.get(p['id'], 0)
        current_stock = p['quantity']
        
        if current_stock > 0:
            turnover_rate = sold / current_stock
        else:
            turnover_rate = sold if sold > 0 else 0
        
        turnover_data.append({
            'name': p['name'],
            'sold': sold,
            'stock': current_stock,
            'rate': turnover_rate
        })
        
        print(f"{p['name']}:")
        print(f"  Units Sold: {sold}")
        print(f"  Current Stock: {current_stock}")
        print(f"  Turnover Rate: {turnover_rate:.2f}\n")
    
    # Identify fast and slow movers
    sorted_turnover = sorted(turnover_data, key=lambda x: x['rate'], reverse=True)
    
    print(f"{'='*50}")
    print("\n🚀 FAST MOVERS (High Turnover):")
    for item in sorted_turnover[:5]:
        print(f"  • {item['name']} (Rate: {item['rate']:.2f})")
    
    print("\n🐌 SLOW MOVERS (Low Turnover):")
    for item in sorted_turnover[-5:]:
        print(f"  • {item['name']} (Rate: {item['rate']:.2f})")


def stock_forecast():
    """Predict when products will run out based on sales trend."""
    print("\n---- STOCK FORECAST ----")
    
    products = load_products()
    orders = load_orders()
    
    if not products or not orders:
        print("⚠ Insufficient data for forecast.")
        return
    
    # Calculate average daily sales
    from collections import defaultdict
    product_sales = defaultdict(list)
    
    for order in orders:
        if order.get('status') in ['Completed', 'Delivered']:
            for item in order['items']:
                product_sales[item['product_id']].append(item['quantity'])
    
    print("\nStock Depletion Forecast:\n")
    
    forecast_data = []
    for p in products:
        sales_data = product_sales.get(p['id'], [])
        
        if sales_data:
            # Use numpy to calculate average daily sales
            avg_daily_sales = np.mean(sales_data)
            
            if avg_daily_sales > 0 and p['quantity'] > 0:
                days_until_stockout = p['quantity'] / avg_daily_sales
                forecast_data.append({
                    'name': p['name'],
                    'days': days_until_stockout,
                    'current_stock': p['quantity'],
                    'avg_sales': avg_daily_sales
                })
            else:
                days_until_stockout = 0
        else:
            days_until_stockout = float('inf')
            avg_daily_sales = 0
        
        status = "🚨" if days_until_stockout < 7 else "⚠️" if days_until_stockout < 14 else "✅"
        
        if days_until_stockout != float('inf'):
            print(f"{status} {p['name']}:")
            print(f"  Current Stock: {p['quantity']}")
            print(f"  Avg Daily Sales: {avg_daily_sales:.2f}")
            print(f"  Days Until Stockout: {days_until_stockout:.0f} days\n")
    
    # Sort by urgency
    if forecast_data:
        forecast_data.sort(key=lambda x: x['days'])
        
        print(f"{'='*50}")
        print("\n⚠️  URGENT RESTOCKING NEEDED (< 7 days):")
        urgent = [f for f in forecast_data if f['days'] < 7]
        if urgent:
            for item in urgent:
                print(f"  • {item['name']}: {item['days']:.0f} days left")
        else:
            print("  None")


def generate_inventory_report():
    """Comprehensive inventory dashboard with multiple charts."""
    print("\n---- COMPREHENSIVE INVENTORY DASHBOARD ----")
    
    products = load_products()
    
    if not products:
        print("⚠ No products found.")
        return
    
    # Categorize products
    out_of_stock = [p for p in products if p['quantity'] == 0]
    low_stock = [p for p in products if 0 < p['quantity'] < 10]
    adequate_stock = [p for p in products if p['quantity'] >= 10]
    
    print(f"\nInventory Summary:")
    print(f"  Total Products: {len(products)}")
    print(f"  Out of Stock: {len(out_of_stock)}")
    print(f"  Low Stock: {len(low_stock)}")
    print(f"  Adequate Stock: {len(adequate_stock)}")
    
    # Calculate values
    quantities = np.array([p['quantity'] for p in products])
    prices = np.array([p['price'] for p in products])
    values = quantities * prices
    
    print(f"\nStock Statistics:")
    print(f"  Total Units: {np.sum(quantities)}")
    print(f"  Average Stock per Product: {np.mean(quantities):.2f}")
    print(f"  Total Inventory Value: ₹{np.sum(values):,.2f}")
    
    # Generate dashboard
    visualize = input("\nGenerate inventory dashboard? (yes/no): ").lower()
    
    if visualize == "yes":
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Inventory Management Dashboard', fontsize=16, fontweight='bold')
        
        # Chart 1: Stock Status Distribution
        categories = ['Out of Stock', 'Low Stock', 'Adequate Stock']
        counts = [len(out_of_stock), len(low_stock), len(adequate_stock)]
        colors = ['red', 'orange', 'green']
        
        axes[0, 0].bar(categories, counts, color=colors, edgecolor='black')
        axes[0, 0].set_title('Stock Status Distribution', fontweight='bold')
        axes[0, 0].set_ylabel('Number of Products')
        for i, (cat, count) in enumerate(zip(categories, counts)):
            axes[0, 0].text(i, count, f'{count}', ha='center', va='bottom', fontsize=10)
        
        # Chart 2: Top 10 products by quantity
        sorted_products = sorted(products, key=lambda x: x['quantity'], reverse=True)[:10]
        names = [p['name'] for p in sorted_products]
        quantities_top = [p['quantity'] for p in sorted_products]
        
        axes[0, 1].barh(names, quantities_top, color='steelblue', edgecolor='navy')
        axes[0, 1].set_title('Top 10 Products by Stock Quantity', fontweight='bold')
        axes[0, 1].set_xlabel('Quantity')
        for i, qty in enumerate(quantities_top):
            axes[0, 1].text(qty, i, f'{qty}', ha='left', va='center', fontsize=9)
        
        # Chart 3: Price distribution
        axes[1, 0].hist(prices, bins=10, color='purple', edgecolor='black', alpha=0.7)
        axes[1, 0].set_title('Price Distribution', fontweight='bold')
        axes[1, 0].set_xlabel('Price (₹)')
        axes[1, 0].set_ylabel('Number of Products')
        axes[1, 0].axvline(np.mean(prices), color='red', linestyle='--', 
                          linewidth=2, label=f'Mean: ₹{np.mean(prices):.2f}')
        axes[1, 0].legend()
        
        # Chart 4: Category-wise stock
        from collections import defaultdict
        category_stock = defaultdict(int)
        for p in products:
            category_stock[p['category']] += p['quantity']
        
        categories_list = list(category_stock.keys())
        stock_list = list(category_stock.values())
        
        axes[1, 1].pie(stock_list, labels=categories_list, autopct='%1.1f%%',
                      startangle=90, shadow=True)
        axes[1, 1].set_title('Stock Distribution by Category', fontweight='bold')
        
        plt.tight_layout()
        plt.show()


def inventory_menu():
    """Main inventory management menu."""
    while True:
        print("\n========== INVENTORY MANAGEMENT ==========")
        print("1. Check Low Stock Alerts")
        print("2. Restock Product")
        print("3. Bulk Restock")
        print("4. Inventory Value Analysis")
        print("5. Stock Turnover Analysis")
        print("6. Stock Forecast")
        print("7. Generate Inventory Dashboard")
        print("8. Back to Admin Menu")
        
        choice = input("\nEnter choice: ")
        
        if choice == "1":
            check_low_stock()
        elif choice == "2":
            restock_product()
        elif choice == "3":
            bulk_restock()
        elif choice == "4":
            inventory_value_analysis()
        elif choice == "5":
            stock_turnover_analysis()
        elif choice == "6":
            stock_forecast()
        elif choice == "7":
            generate_inventory_report()
        elif choice == "8":
            break
        else:
            print("Invalid choice. Try again.")