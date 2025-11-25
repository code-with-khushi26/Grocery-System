import json
import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from collections import defaultdict
from models.user import Order, Product, User

ORDER_FILE_PATH = "data/orders.json"
PRODUCT_FILE_PATH = "data/products.json"
USER_FILE_PATH = "data/users.json"


class OrderRepository:
    """Repository for order data"""
    
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


class ProductRepository:
    """Repository for product data"""
    
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


class UserRepository:
    """Repository for user data"""
    
    def __init__(self, file_path=USER_FILE_PATH):
        self.file_path = file_path
    
    def load_all(self):
        """Load all users"""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                try:
                    data = json.load(file)
                    return [User.from_dict(u) for u in data]
                except json.JSONDecodeError:
                    return []
        return []


class ReportingService:
    """Service for generating reports and analytics"""
    
    def __init__(self):
        self.order_repo = OrderRepository()
        self.product_repo = ProductRepository()
        self.user_repo = UserRepository()
    
    def sales_summary_report(self):
        """Generate comprehensive sales summary with statistics"""
        print("\n========== SALES SUMMARY REPORT ==========\n")
        
        orders = self.order_repo.load_all()
        
        if not orders:
            print("📦 No orders found.")
            return
        
        # Calculate metrics
        total_orders = len(orders)
        completed_orders = [o for o in orders if o.is_completed()]
        pending_orders = [o for o in orders if o.status == 'Pending']
        cancelled_orders = [o for o in orders if o.status == 'Cancelled']
        
        total_revenue = sum(order.calculate_total() for order in completed_orders)
        avg_order_value = total_revenue / len(completed_orders) if completed_orders else 0
        
        # Using numpy for statistical analysis
        if completed_orders:
            order_values = np.array([order.calculate_total() for order in completed_orders])
            max_order = np.max(order_values)
            min_order = np.min(order_values)
            std_deviation = np.std(order_values)
            median_order = np.median(order_values)
        else:
            max_order = min_order = std_deviation = median_order = 0
        
        # Display report
        print(f"Total Orders: {total_orders}")
        print(f"Completed Orders: {len(completed_orders)}")
        print(f"Pending Orders: {len(pending_orders)}")
        print(f"Cancelled Orders: {len(cancelled_orders)}")
        print(f"\n{'='*45}")
        print(f"Total Revenue: ₹{total_revenue:,.2f}")
        print(f"Average Order Value: ₹{avg_order_value:,.2f}")
        print(f"Median Order Value: ₹{median_order:,.2f}")
        print(f"Highest Order: ₹{max_order:,.2f}")
        print(f"Lowest Order: ₹{min_order:,.2f}")
        print(f"Standard Deviation: ₹{std_deviation:,.2f}")
        print(f"{'='*45}\n")
    
    def product_sales_report(self):
        """Report on most sold products with visualization"""
        print("\n========== PRODUCT SALES REPORT ==========\n")
        
        orders = self.order_repo.load_all()
        
        if not orders:
            print("📦 No orders found.")
            return
        
        # Count product sales
        product_sales = defaultdict(lambda: {'quantity': 0, 'revenue': 0})
        
        for order in orders:
            if order.is_completed():
                for item in order.items:
                    prod_name = item.product_name
                    product_sales[prod_name]['quantity'] += item.quantity
                    product_sales[prod_name]['revenue'] += item.get_subtotal()
        
        if not product_sales:
            print("No completed sales found.")
            return
        
        # Sort by quantity sold
        sorted_products = sorted(product_sales.items(), key=lambda x: x[1]['quantity'], reverse=True)
        
        print("Top Selling Products:\n")
        for i, (product, data) in enumerate(sorted_products[:10], 1):
            print(f"{i}. {product}")
            print(f"   Quantity Sold: {data['quantity']}")
            print(f"   Revenue: ₹{data['revenue']:,.2f}\n")
        
        # Visualization
        visualize = input("\nGenerate chart? (yes/no): ").lower()
        if visualize == "yes":
            top_5 = sorted_products[:5]
            products = [p[0] for p in top_5]
            quantities = [p[1]['quantity'] for p in top_5]
            
            plt.figure(figsize=(10, 6))
            bars = plt.bar(products, quantities, color='skyblue', edgecolor='navy')
            plt.xlabel('Products', fontsize=12, fontweight='bold')
            plt.ylabel('Quantity Sold', fontsize=12, fontweight='bold')
            plt.title('Top 5 Best Selling Products', fontsize=14, fontweight='bold')
            plt.xticks(rotation=45, ha='right')
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}', ha='center', va='bottom')
            
            plt.tight_layout()
            plt.show()
    
    def revenue_by_category(self):
        """Analyze revenue distribution by product category"""
        print("\n========== REVENUE BY CATEGORY ==========\n")
        
        orders = self.order_repo.load_all()
        products = self.product_repo.load_all()
        
        if not orders or not products:
            print("Insufficient data for analysis.")
            return
        
        # Create product ID to category mapping
        product_categories = {p.id: p.category for p in products}
        
        # Calculate revenue by category
        category_revenue = defaultdict(float)
        
        for order in orders:
            if order.is_completed():
                for item in order.items:
                    prod_id = item.product_id
                    category = product_categories.get(prod_id, 'Unknown')
                    category_revenue[category] += item.get_subtotal()
        
        if not category_revenue:
            print("No sales data available.")
            return
        
        # Display results
        total = sum(category_revenue.values())
        
        for category, revenue in sorted(category_revenue.items(), key=lambda x: x[1], reverse=True):
            percentage = (revenue / total) * 100
            print(f"{category}: ₹{revenue:,.2f} ({percentage:.1f}%)")
        
        # Pie chart visualization
        visualize = input("\nGenerate pie chart? (yes/no): ").lower()
        if visualize == "yes":
            categories = list(category_revenue.keys())
            revenues = list(category_revenue.values())
            
            plt.figure(figsize=(10, 8))
            colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
            explode = [0.05] * len(categories)
            
            plt.pie(revenues, labels=categories, autopct='%1.1f%%', 
                    startangle=90, colors=colors, explode=explode,
                    shadow=True)
            plt.title('Revenue Distribution by Category', fontsize=14, fontweight='bold')
            plt.axis('equal')
            plt.tight_layout()
            plt.show()
    
    def inventory_status_report(self):
        """Report on current inventory levels with alerts"""
        print("\n========== INVENTORY STATUS REPORT ==========\n")
        
        products = self.product_repo.load_all()
        
        if not products:
            print("No products found.")
            return
        
        low_stock_threshold = 10
        out_of_stock = []
        low_stock = []
        adequate_stock = []
        
        for product in products:
            if product.is_out_of_stock():
                out_of_stock.append(product)
            elif product.is_low_stock(low_stock_threshold):
                low_stock.append(product)
            else:
                adequate_stock.append(product)
        
        # Display summary
        print(f"Total Products: {len(products)}")
        print(f"Out of Stock: {len(out_of_stock)} ⚠️")
        print(f"Low Stock: {len(low_stock)} ⚠️")
        print(f"Adequate Stock: {len(adequate_stock)} ✓")
        print(f"\n{'='*50}\n")
        
        if out_of_stock:
            print("OUT OF STOCK:")
            for p in out_of_stock:
                print(f"  ❌ {p.name} - Qty: {p.quantity}")
        
        if low_stock:
            print("\nLOW STOCK (< 10 units):")
            for p in low_stock:
                print(f"  ⚠️  {p.name} - Qty: {p.quantity}")
        
        # Stock distribution chart
        visualize = input("\nGenerate stock distribution chart? (yes/no): ").lower()
        if visualize == "yes":
            categories = ['Out of Stock', 'Low Stock', 'Adequate Stock']
            counts = [len(out_of_stock), len(low_stock), len(adequate_stock)]
            colors = ['red', 'orange', 'green']
            
            plt.figure(figsize=(8, 6))
            bars = plt.bar(categories, counts, color=colors, edgecolor='black')
            plt.ylabel('Number of Products', fontsize=12, fontweight='bold')
            plt.title('Inventory Status Distribution', fontsize=14, fontweight='bold')
            
            # Add value labels
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}', ha='center', va='bottom', fontsize=12)
            
            plt.tight_layout()
            plt.show()
    
    def customer_analysis_report(self):
        """Analyze customer purchase patterns"""
        print("\n========== CUSTOMER ANALYSIS REPORT ==========\n")
        
        orders = self.order_repo.load_all()
        
        if not orders:
            print("No orders found.")
            return
        
        # Aggregate by customer
        customer_data = defaultdict(lambda: {'orders': 0, 'total_spent': 0})
        
        for order in orders:
            if order.is_completed():
                phone = order.customer_phone
                customer_data[phone]['orders'] += 1
                customer_data[phone]['total_spent'] += order.calculate_total()
                customer_data[phone]['name'] = order.customer_name
        
        if not customer_data:
            print("No completed orders found.")
            return
        
        # Sort by total spent
        sorted_customers = sorted(customer_data.items(), 
                                 key=lambda x: x[1]['total_spent'], 
                                 reverse=True)
        
        print("Top 10 Customers by Revenue:\n")
        for i, (phone, data) in enumerate(sorted_customers[:10], 1):
            avg_order = data['total_spent'] / data['orders']
            print(f"{i}. {data['name']} ({phone})")
            print(f"   Orders: {data['orders']}")
            print(f"   Total Spent: ₹{data['total_spent']:,.2f}")
            print(f"   Avg Order Value: ₹{avg_order:,.2f}\n")
        
        # Customer spending distribution
        visualize = input("Generate customer spending chart? (yes/no): ").lower()
        if visualize == "yes":
            top_10 = sorted_customers[:10]
            names = [c[1]['name'] for c in top_10]
            spending = [c[1]['total_spent'] for c in top_10]
            
            plt.figure(figsize=(12, 6))
            bars = plt.barh(names, spending, color='coral', edgecolor='darkred')
            plt.xlabel('Total Spending (₹)', fontsize=12, fontweight='bold')
            plt.ylabel('Customers', fontsize=12, fontweight='bold')
            plt.title('Top 10 Customers by Total Spending', fontsize=14, fontweight='bold')
            
            # Add value labels
            for i, bar in enumerate(bars):
                width = bar.get_width()
                plt.text(width, bar.get_y() + bar.get_height()/2.,
                        f'₹{width:,.0f}', ha='left', va='center', fontsize=9)
            
            plt.tight_layout()
            plt.show()
    
    def monthly_sales_trend(self):
        """Show sales trend over months using line chart"""
        print("\n========== MONTHLY SALES TREND ==========\n")
        
        orders = self.order_repo.load_all()
        
        if not orders:
            print("No orders found.")
            return
        
        # Group by month
        monthly_sales = defaultdict(float)
        
        for order in orders:
            if order.is_completed():
                date_str = order.order_date
                # Parse date (format: "YYYY-MM-DD HH:MM:SS")
                date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                month_key = date_obj.strftime("%Y-%m")
                monthly_sales[month_key] += order.calculate_total()
        
        if not monthly_sales:
            print("No completed sales found.")
            return
        
        # Sort by month
        sorted_months = sorted(monthly_sales.items())
        
        print("Monthly Revenue:\n")
        for month, revenue in sorted_months:
            print(f"{month}: ₹{revenue:,.2f}")
        
        # Line chart
        visualize = input("\nGenerate trend chart? (yes/no): ").lower()
        if visualize == "yes":
            months = [m[0] for m in sorted_months]
            revenues = [m[1] for m in sorted_months]
            
            plt.figure(figsize=(12, 6))
            plt.plot(months, revenues, marker='o', linewidth=2, 
                    markersize=8, color='green', markerfacecolor='lime')
            plt.xlabel('Month', fontsize=12, fontweight='bold')
            plt.ylabel('Revenue (₹)', fontsize=12, fontweight='bold')
            plt.title('Monthly Sales Trend', fontsize=14, fontweight='bold')
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            
            # Add value labels
            for i, (month, revenue) in enumerate(zip(months, revenues)):
                plt.text(i, revenue, f'₹{revenue:,.0f}', 
                        ha='center', va='bottom', fontsize=9)
            
            plt.tight_layout()
            plt.show()


def reporting_menu():
    """Main reporting menu with all report options"""
    service = ReportingService()
    
    while True:
        print("\n========== REPORTING & ANALYTICS ==========")
        print("1. Sales Summary Report")
        print("2. Product Sales Report")
        print("3. Revenue by Category")
        print("4. Inventory Status Report")
        print("5. Customer Analysis Report")
        print("6. Monthly Sales Trend")
        print("7. Back to Admin Menu")
        
        choice = input("\nEnter choice: ")
        
        if choice == "1":
            service.sales_summary_report()
        elif choice == "2":
            service.product_sales_report()
        elif choice == "3":
            service.revenue_by_category()
        elif choice == "4":
            service.inventory_status_report()
        elif choice == "5":
            service.customer_analysis_report()
        elif choice == "6":
            service.monthly_sales_trend()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Try again.")


# Legacy functions
def load_orders():
    repo = OrderRepository()
    orders = repo.load_all()
    return [o.to_dict() for o in orders]


def load_products():
    repo = ProductRepository()
    products = repo.load_all()
    return [p.to_dict() for p in products]


def load_users():
    repo = UserRepository()
    users = repo.load_all()
    return [u.to_dict() for u in users]