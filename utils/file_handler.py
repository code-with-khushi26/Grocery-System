import json
import os
import shutil
from datetime import datetime

# File paths
USER_FILE_PATH = "data/users.json"
PRODUCT_FILE_PATH = "data/products.json"
ORDER_FILE_PATH = "data/orders.json"
SUPPLIER_FILE_PATH = "data/suppliers.json"
REPORTS_FILE_PATH = "data/reports.json"

# Backup directory
BACKUP_DIR = "data/backups/"


def ensure_data_directory():
    """Create data directory if it doesn't exist."""
    if not os.path.exists("data"):
        os.makedirs("data")
        print("✅ Created 'data' directory")
    
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print("✅ Created 'backups' directory")


def initialize_json_files():
    """Initialize all JSON files with proper structure if they don't exist."""
    ensure_data_directory()
    
    files = {
        USER_FILE_PATH: [
            {
                "name": "Admin",
                "dob": "01-01-2000",
                "phone": "admin",
                "location": "System",
                "password": "admin123",
                "role": "admin"
            }
        ],
        PRODUCT_FILE_PATH: [],
        ORDER_FILE_PATH: [],
        SUPPLIER_FILE_PATH: [],
        REPORTS_FILE_PATH: []
    }
    
    for file_path, default_data in files.items():
        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                json.dump(default_data, file, indent=4)
            print(f"✅ Initialized {file_path}")
        else:
            print(f"ℹ️  {file_path} already exists")


def load_json_file(file_path):
    """Generic function to load any JSON file."""
    try:
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                return json.load(file)
        else:
            print(f"⚠️  File not found: {file_path}")
            return []
    except json.JSONDecodeError:
        print(f"❌ Error reading {file_path}. File may be corrupted.")
        return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []


def save_json_file(file_path, data):
    """Generic function to save data to any JSON file."""
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        print(f"❌ Error saving to {file_path}: {e}")
        return False


def backup_all_data():
    """Create backup of all data files."""
    ensure_data_directory()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder = os.path.join(BACKUP_DIR, f"backup_{timestamp}")
    
    try:
        os.makedirs(backup_folder)
        
        files_to_backup = [
            USER_FILE_PATH,
            PRODUCT_FILE_PATH,
            ORDER_FILE_PATH,
            SUPPLIER_FILE_PATH,
            REPORTS_FILE_PATH
        ]
        
        backed_up = 0
        for file_path in files_to_backup:
            if os.path.exists(file_path):
                filename = os.path.basename(file_path)
                backup_path = os.path.join(backup_folder, filename)
                shutil.copy2(file_path, backup_path)
                backed_up += 1
        
        print(f"\n✅ Backup created successfully!")
        print(f"Location: {backup_folder}")
        print(f"Files backed up: {backed_up}")
        return True
    
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False


def restore_from_backup():
    """Restore data from a backup."""
    if not os.path.exists(BACKUP_DIR):
        print("❌ No backups found.")
        return
    
    # List available backups
    backups = [d for d in os.listdir(BACKUP_DIR) if d.startswith("backup_")]
    
    if not backups:
        print("❌ No backups available.")
        return
    
    print("\n---- AVAILABLE BACKUPS ----")
    for i, backup in enumerate(backups, 1):
        # Extract timestamp
        timestamp = backup.replace("backup_", "")
        readable_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
        print(f"{i}. {readable_time}")
    
    try:
        choice = int(input("\nSelect backup to restore (0 to cancel): "))
        
        if choice == 0:
            print("Restore cancelled.")
            return
        
        if 1 <= choice <= len(backups):
            selected_backup = backups[choice - 1]
            backup_path = os.path.join(BACKUP_DIR, selected_backup)
            
            confirm = input(f"\n⚠️  This will overwrite current data. Continue? (yes/no): ").lower()
            
            if confirm == "yes":
                files = os.listdir(backup_path)
                restored = 0
                
                for filename in files:
                    source = os.path.join(backup_path, filename)
                    destination = os.path.join("data", filename)
                    shutil.copy2(source, destination)
                    restored += 1
                
                print(f"\n✅ Backup restored successfully!")
                print(f"Files restored: {restored}")
            else:
                print("Restore cancelled.")
        else:
            print("❌ Invalid selection.")
    
    except ValueError:
        print("❌ Invalid input.")
    except Exception as e:
        print(f"❌ Restore failed: {e}")


def export_data_to_json():
    """Export all data to a single JSON file."""
    print("\n---- EXPORT ALL DATA ----")
    
    try:
        export_data = {
            "export_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "users": load_json_file(USER_FILE_PATH),
            "products": load_json_file(PRODUCT_FILE_PATH),
            "orders": load_json_file(ORDER_FILE_PATH),
            "suppliers": load_json_file(SUPPLIER_FILE_PATH),
            "reports": load_json_file(REPORTS_FILE_PATH)
        }
        
        filename = f"grocery_system_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, "w") as file:
            json.dump(export_data, file, indent=4)
        
        print(f"\n✅ Data exported successfully!")
        print(f"File: {filename}")
        print(f"Location: {os.path.abspath(filename)}")
        
        # Calculate file size
        file_size = os.path.getsize(filename) / 1024  # KB
        print(f"Size: {file_size:.2f} KB")
    
    except Exception as e:
        print(f"❌ Export failed: {e}")


def import_data_from_json():
    """Import data from an exported JSON file."""
    print("\n---- IMPORT DATA ----")
    
    filename = input("Enter filename to import: ")
    
    if not os.path.exists(filename):
        print(f"❌ File '{filename}' not found.")
        return
    
    try:
        with open(filename, "r") as file:
            import_data = json.load(file)
        
        print("\n⚠️  WARNING: This will overwrite existing data!")
        print(f"Import contains:")
        print(f"  - Users: {len(import_data.get('users', []))}")
        print(f"  - Products: {len(import_data.get('products', []))}")
        print(f"  - Orders: {len(import_data.get('orders', []))}")
        print(f"  - Suppliers: {len(import_data.get('suppliers', []))}")
        
        confirm = input("\nContinue with import? (yes/no): ").lower()
        
        if confirm == "yes":
            # Create backup first
            print("\nCreating backup before import...")
            backup_all_data()
            
            # Import data
            save_json_file(USER_FILE_PATH, import_data.get('users', []))
            save_json_file(PRODUCT_FILE_PATH, import_data.get('products', []))
            save_json_file(ORDER_FILE_PATH, import_data.get('orders', []))
            save_json_file(SUPPLIER_FILE_PATH, import_data.get('suppliers', []))
            save_json_file(REPORTS_FILE_PATH, import_data.get('reports', []))
            
            print("\n✅ Data imported successfully!")
        else:
            print("Import cancelled.")
    
    except json.JSONDecodeError:
        print("❌ Invalid JSON file.")
    except Exception as e:
        print(f"❌ Import failed: {e}")


def clear_all_data():
    """Clear all data (with confirmation)."""
    print("\n⚠️  WARNING: CLEAR ALL DATA ⚠️")
    print("This will delete all users, products, orders, and suppliers!")
    
    confirm1 = input("\nAre you absolutely sure? (type 'DELETE ALL'): ")
    
    if confirm1 == "DELETE ALL":
        confirm2 = input("Type 'CONFIRM' to proceed: ")
        
        if confirm2 == "CONFIRM":
            # Create backup first
            print("\nCreating backup before clearing...")
            backup_all_data()
            
            # Clear all files (keep admin user)
            save_json_file(USER_FILE_PATH, [{
                "name": "Admin",
                "dob": "01-01-2000",
                "phone": "admin",
                "location": "System",
                "password": "admin123",
                "role": "admin"
            }])
            save_json_file(PRODUCT_FILE_PATH, [])
            save_json_file(ORDER_FILE_PATH, [])
            save_json_file(SUPPLIER_FILE_PATH, [])
            save_json_file(REPORTS_FILE_PATH, [])
            
            print("\n✅ All data cleared. Admin account retained.")
        else:
            print("Operation cancelled.")
    else:
        print("Operation cancelled.")


def view_file_statistics():
    """Display statistics about data files."""
    print("\n---- FILE STATISTICS ----\n")
    
    files = {
        "Users": USER_FILE_PATH,
        "Products": PRODUCT_FILE_PATH,
        "Orders": ORDER_FILE_PATH,
        "Suppliers": SUPPLIER_FILE_PATH,
        "Reports": REPORTS_FILE_PATH
    }
    
    total_size = 0
    
    for name, path in files.items():
        if os.path.exists(path):
            size = os.path.getsize(path) / 1024  # KB
            total_size += size
            
            data = load_json_file(path)
            count = len(data) if isinstance(data, list) else 0
            
            print(f"{name}:")
            print(f"  Records: {count}")
            print(f"  File Size: {size:.2f} KB")
            print(f"  Path: {path}\n")
        else:
            print(f"{name}: File not found\n")
    
    print(f"{'='*50}")
    print(f"Total Storage Used: {total_size:.2f} KB")
    
    # Check backup directory
    if os.path.exists(BACKUP_DIR):
        backups = [d for d in os.listdir(BACKUP_DIR) if d.startswith("backup_")]
        print(f"Backups Available: {len(backups)}")


def fix_corrupted_files():
    """Attempt to fix corrupted JSON files."""
    print("\n---- FIX CORRUPTED FILES ----")
    
    files = {
        USER_FILE_PATH: [{
            "name": "Admin",
            "dob": "01-01-2000",
            "phone": "admin",
            "location": "System",
            "password": "admin123",
            "role": "admin"
        }],
        PRODUCT_FILE_PATH: [],
        ORDER_FILE_PATH: [],
        SUPPLIER_FILE_PATH: [],
        REPORTS_FILE_PATH: []
    }
    
    fixed = 0
    
    for file_path, default_data in files.items():
        try:
            with open(file_path, "r") as file:
                json.load(file)
            print(f"✅ {file_path} is valid")
        except (json.JSONDecodeError, FileNotFoundError):
            print(f"⚠️  Fixing {file_path}...")
            save_json_file(file_path, default_data)
            fixed += 1
            print(f"✅ Fixed {file_path}")
    
    if fixed > 0:
        print(f"\n✅ Fixed {fixed} corrupted file(s)")
    else:
        print("\n✅ All files are healthy!")


def file_management_menu():
    """Main file management menu."""
    while True:
        print("\n========== FILE MANAGEMENT ==========")
        print("1. Initialize JSON Files")
        print("2. Backup All Data")
        print("3. Restore from Backup")
        print("4. Export Data (Single JSON)")
        print("5. Import Data from JSON")
        print("6. View File Statistics")
        print("7. Fix Corrupted Files")
        print("8. Clear All Data (⚠️ Dangerous)")
        print("9. Back to Admin Menu")
        
        choice = input("\nEnter choice: ")
        
        if choice == "1":
            initialize_json_files()
        elif choice == "2":
            backup_all_data()
        elif choice == "3":
            restore_from_backup()
        elif choice == "4":
            export_data_to_json()
        elif choice == "5":
            import_data_from_json()
        elif choice == "6":
            view_file_statistics()
        elif choice == "7":
            fix_corrupted_files()
        elif choice == "8":
            clear_all_data()
        elif choice == "9":
            break
        else:
            print("Invalid choice. Try again.")


# Run this on system startup to ensure files exist
if __name__ == "__main__":
    initialize_json_files()