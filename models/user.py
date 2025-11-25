"""
User Model Class
"""


class User:
    """Represents a user in the system (both admin and regular users)"""
    
    def __init__(self, name, dob, phone, location, password, role="user"):
        self.name = name
        self.dob = dob
        self.phone = phone
        self.location = location
        self.password = password
        self.role = role
    
    def is_admin(self):
        """Check if user is an administrator"""
        return self.role == "admin"
    
    def validate_password(self, password):
        """Validate if provided password matches"""
        return self.password == password
    
    def update_profile(self, **kwargs):
        """Update user profile information"""
        for key, value in kwargs.items():
            if hasattr(self, key) and key != 'phone':
                setattr(self, key, value)
    
    def to_dict(self):
        """Convert to dictionary for JSON storage"""
        return {
            "name": self.name,
            "dob": self.dob,
            "phone": self.phone,
            "location": self.location,
            "password": self.password,
            "role": self.role
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create User object from dictionary"""
        return cls(
            name=data['name'],
            dob=data['dob'],
            phone=data['phone'],
            location=data['location'],
            password=data['password'],
            role=data.get('role', 'user')
        )
    
    def __str__(self):
        return f"User({self.name}, {self.phone}, {self.role})"


class Product:
    """Represents a product in inventory"""
    
    def __init__(self, id, name, category, quantity, price):
        self.id = id
        self.name = name
        self.category = category
        self.quantity = quantity
        self.price = price
    
    def is_in_stock(self):
        """Check if product is in stock"""
        return self.quantity > 0
    
    def is_out_of_stock(self):
        """Check if product is out of stock"""
        return self.quantity == 0
    
    def is_low_stock(self, threshold=10):
        """Check if product has low stock"""
        return 0 < self.quantity < threshold
    
    def restock(self, quantity):
        """Add quantity to existing stock"""
        if quantity > 0:
            self.quantity += quantity
            return True
        return False
    
    def reduce_stock(self, quantity):
        """Reduce stock by specified quantity"""
        if quantity <= self.quantity:
            self.quantity -= quantity
            return True
        return False
    
    def calculate_inventory_value(self):
        """Calculate total inventory value"""
        return self.quantity * self.price
    
    def get_stock_status(self):
        """Get human-readable stock status"""
        if self.is_out_of_stock():
            return "✗ Out of Stock"
        elif self.is_low_stock():
            return "⚠️ Low Stock"
        else:
            return "✓ In Stock"
    
    def to_dict(self):
        """Convert to dictionary for JSON storage"""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "quantity": self.quantity,
            "price": self.price
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Product object from dictionary"""
        return cls(
            id=data['id'],
            name=data['name'],
            category=data['category'],
            quantity=data['quantity'],
            price=data['price']
        )
    
    def __str__(self):
        return f"Product({self.id}, {self.name}, ₹{self.price}, Qty: {self.quantity})"


class OrderItem:
    """Represents a single item in an order"""
    
    def __init__(self, product_id, product_name, quantity, price):
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.price = price
    
    def get_subtotal(self):
        """Calculate subtotal for this item"""
        return self.quantity * self.price
    
    def to_dict(self):
        """Convert to dictionary for JSON storage"""
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "price": self.price,
            "subtotal": self.get_subtotal()
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create OrderItem object from dictionary"""
        return cls(
            product_id=data['product_id'],
            product_name=data['product_name'],
            quantity=data['quantity'],
            price=data['price']
        )


class Order:
    """Represents a customer order"""
    
    def __init__(self, order_id, customer_name, customer_phone, status="Pending"):
        from datetime import datetime
        self.order_id = order_id
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.items = []
        self.status = status
        self.order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def add_item(self, order_item):
        """Add an item to the order"""
        self.items.append(order_item)
    
    def calculate_total(self):
        """Calculate total order amount"""
        return sum(item.get_subtotal() for item in self.items)
    
    def update_status(self, new_status):
        """Update order status"""
        valid_statuses = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled", "Completed"]
        if new_status in valid_statuses:
            self.status = new_status
            return True
        return False
    
    def is_completed(self):
        """Check if order is completed"""
        return self.status in ["Completed", "Delivered"]
    
    def to_dict(self):
        """Convert to dictionary for JSON storage"""
        return {
            "order_id": self.order_id,
            "customer_name": self.customer_name,
            "customer_phone": self.customer_phone,
            "items": [item.to_dict() for item in self.items],
            "total_amount": self.calculate_total(),
            "order_date": self.order_date,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Order object from dictionary"""
        order = cls(
            order_id=data['order_id'],
            customer_name=data['customer_name'],
            customer_phone=data['customer_phone'],
            status=data.get('status', 'Pending')
        )
        order.order_date = data.get('order_date', order.order_date)
        order.items = [OrderItem.from_dict(item) for item in data.get('items', [])]
        return order


class Supplier:
    """Represents a supplier"""
    
    def __init__(self, id, name, contact_person, phone, email, address, products_supplied):
        from datetime import datetime
        self.id = id
        self.name = name
        self.contact_person = contact_person
        self.phone = phone
        self.email = email
        self.address = address
        self.products_supplied = products_supplied if isinstance(products_supplied, list) else []
        self.total_orders = 0
        self.total_amount = 0
        self.rating = 5.0
        self.status = "Active"
        self.added_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def is_active(self):
        """Check if supplier is active"""
        return self.status == "Active"
    
    def update_rating(self, new_rating):
        """Update supplier rating"""
        if 0 <= new_rating <= 5:
            self.rating = new_rating
            return True
        return False
    
    def record_purchase(self, amount):
        """Record a purchase from this supplier"""
        self.total_orders += 1
        self.total_amount += amount
    
    def to_dict(self):
        """Convert to dictionary for JSON storage"""
        return {
            "id": self.id,
            "name": self.name,
            "contact_person": self.contact_person,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "products_supplied": self.products_supplied,
            "total_orders": self.total_orders,
            "total_amount": self.total_amount,
            "rating": self.rating,
            "status": self.status,
            "added_date": self.added_date
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Supplier object from dictionary"""
        supplier = cls(
            id=data['id'],
            name=data['name'],
            contact_person=data['contact_person'],
            phone=data['phone'],
            email=data['email'],
            address=data['address'],
            products_supplied=data.get('products_supplied', [])
        )
        supplier.total_orders = data.get('total_orders', 0)
        supplier.total_amount = data.get('total_amount', 0)
        supplier.rating = data.get('rating', 5.0)
        supplier.status = data.get('status', 'Active')
        supplier.added_date = data.get('added_date', supplier.added_date)
        return supplier


class ShoppingCart:
    """Represents a shopping cart"""
    
    def __init__(self):
        self.items = []
    
    def add_item(self, product, quantity):
        """Add item to cart"""
        # Check if product already in cart
        for item in self.items:
            if item['id'] == product.id:
                item['qty'] += quantity
                return True
        
        # Add new item
        self.items.append({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "qty": quantity
        })
        return True
    
    def remove_item(self, product_id):
        """Remove item from cart"""
        self.items = [item for item in self.items if item['id'] != product_id]
    
    def get_total(self):
        """Calculate cart total"""
        return sum(item['price'] * item['qty'] for item in self.items)
    
    def is_empty(self):
        """Check if cart is empty"""
        return len(self.items) == 0
    
    def clear(self):
        """Clear all items from cart"""
        self.items = []
    
    def get_item_count(self):
        """Get total number of items in cart"""
        return sum(item['qty'] for item in self.items)
    
    def display(self):
        """Display cart contents"""
        if self.is_empty():
            print("🛒 Cart is empty.")
            return
        
        print("\n---- YOUR CART ----")
        total = 0
        for item in self.items:
            subtotal = item['price'] * item['qty']
            total += subtotal
            print(f"ID: {item['id']} | {item['name']} × {item['qty']} = ₹{subtotal}")
        
        print("-" * 40)
        print(f"Total: ₹{total}")