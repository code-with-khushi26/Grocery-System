import re
from datetime import datetime


def validate_phone(phone):
    """
    Validate phone number.
    Accepts 10-digit numbers with optional +91 prefix.
    Returns: (is_valid: bool, message: str)
    """
    if not phone:
        return False, "Phone number cannot be empty."
    
    # Remove spaces and hyphens
    phone_clean = phone.replace(" ", "").replace("-", "")
    
    # Check for +91 prefix
    if phone_clean.startswith("+91"):
        phone_clean = phone_clean[3:]
    elif phone_clean.startswith("91") and len(phone_clean) == 12:
        phone_clean = phone_clean[2:]
    
    # Check if it's 10 digits
    if not phone_clean.isdigit():
        return False, "Phone number should contain only digits."
    
    if len(phone_clean) != 10:
        return False, "Phone number should be 10 digits."
    
    if phone_clean[0] not in '6789':
        return False, "Phone number should start with 6, 7, 8, or 9."
    
    return True, "Valid phone number."


def validate_email(email):
    """
    Validate email address format.
    Returns: (is_valid: bool, message: str)
    """
    if not email:
        return False, "Email cannot be empty."
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(pattern, email):
        return True, "Valid email address."
    else:
        return False, "Invalid email format. Use: example@domain.com"


def validate_password(password):
    """
    Validate password strength.
    Requirements: 6+ chars, at least one letter and one number.
    Returns: (is_valid: bool, message: str)
    """
    if not password:
        return False, "Password cannot be empty."
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    
    if len(password) > 50:
        return False, "Password too long (max 50 characters)."
    
    has_letter = any(c.isalpha() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    if not has_letter:
        return False, "Password must contain at least one letter."
    
    if not has_digit:
        return False, "Password must contain at least one number."
    
    return True, "Strong password."


def validate_name(name):
    """
    Validate name (letters, spaces, hyphens only).
    Returns: (is_valid: bool, message: str)
    """
    if not name:
        return False, "Name cannot be empty."
    
    if len(name) < 2:
        return False, "Name too short (minimum 2 characters)."
    
    if len(name) > 50:
        return False, "Name too long (maximum 50 characters)."
    
    # Allow letters, spaces, hyphens, and apostrophes
    pattern = r"^[a-zA-Z\s\-']+$"
    
    if re.match(pattern, name):
        return True, "Valid name."
    else:
        return False, "Name should contain only letters, spaces, and hyphens."


def validate_date(date_str, format="%d-%m-%Y"):
    """
    Validate date format and check if it's a valid date.
    Default format: DD-MM-YYYY
    Returns: (is_valid: bool, message: str)
    """
    if not date_str:
        return False, "Date cannot be empty."
    
    try:
        date_obj = datetime.strptime(date_str, format)
        
        # Check if date is not in the future (for DOB)
        if date_obj > datetime.now():
            return False, "Date cannot be in the future."
        
        # Check if person is not too old (reasonable age check)
        year_diff = datetime.now().year - date_obj.year
        if year_diff > 120:
            return False, "Invalid date (too old)."
        
        return True, "Valid date."
    
    except ValueError:
        return False, f"Invalid date format. Use {format} (e.g., 25-12-2000)"


def validate_price(price_str):
    """
    Validate price (positive number, up to 2 decimal places).
    Returns: (is_valid: bool, value: float/None, message: str)
    """
    if not price_str:
        return False, None, "Price cannot be empty."
    
    try:
        price = float(price_str)
        
        if price < 0:
            return False, None, "Price cannot be negative."
        
        if price == 0:
            return False, None, "Price must be greater than 0."
        
        if price > 1000000:
            return False, None, "Price too high (max ₹10,00,000)."
        
        # Check decimal places
        if len(str(price).split('.')[-1]) > 2:
            return False, None, "Price should have maximum 2 decimal places."
        
        return True, round(price, 2), "Valid price."
    
    except ValueError:
        return False, None, "Invalid price format. Enter a number."


def validate_quantity(quantity_str):
    """
    Validate quantity (positive integer).
    Returns: (is_valid: bool, value: int/None, message: str)
    """
    if not quantity_str:
        return False, None, "Quantity cannot be empty."
    
    try:
        quantity = int(quantity_str)
        
        if quantity < 0:
            return False, None, "Quantity cannot be negative."
        
        if quantity > 100000:
            return False, None, "Quantity too high (max 100,000)."
        
        return True, quantity, "Valid quantity."
    
    except ValueError:
        return False, None, "Invalid quantity. Enter a whole number."


def validate_rating(rating_str):
    """
    Validate rating (0.0 to 5.0).
    Returns: (is_valid: bool, value: float/None, message: str)
    """
    if not rating_str:
        return False, None, "Rating cannot be empty."
    
    try:
        rating = float(rating_str)
        
        if rating < 0 or rating > 5:
            return False, None, "Rating must be between 0.0 and 5.0."
        
        return True, round(rating, 1), "Valid rating."
    
    except ValueError:
        return False, None, "Invalid rating. Enter a number between 0 and 5."


def validate_category(category):
    """
    Validate product category (non-empty string).
    Returns: (is_valid: bool, message: str)
    """
    if not category:
        return False, "Category cannot be empty."
    
    if len(category) < 2:
        return False, "Category too short (minimum 2 characters)."
    
    if len(category) > 30:
        return False, "Category too long (maximum 30 characters)."
    
    # Allow letters, spaces, and ampersands
    pattern = r"^[a-zA-Z\s&]+$"
    
    if re.match(pattern, category):
        return True, "Valid category."
    else:
        return False, "Category should contain only letters and spaces."


def validate_choice(choice, min_val, max_val):
    """
    Validate menu choice (integer within range).
    Returns: (is_valid: bool, value: int/None, message: str)
    """
    if not choice:
        return False, None, "Choice cannot be empty."
    
    try:
        choice_int = int(choice)
        
        if choice_int < min_val or choice_int > max_val:
            return False, None, f"Choose between {min_val} and {max_val}."
        
        return True, choice_int, "Valid choice."
    
    except ValueError:
        return False, None, "Invalid input. Enter a number."


def validate_non_empty(text, field_name="Field"):
    """
    Validate that a field is not empty.
    Returns: (is_valid: bool, message: str)
    """
    if not text or text.strip() == "":
        return False, f"{field_name} cannot be empty."
    
    return True, f"Valid {field_name.lower()}."


def sanitize_input(text):
    """
    Sanitize user input by removing extra spaces and special characters.
    Returns: cleaned string
    """
    if not text:
        return ""
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Remove multiple spaces
    text = " ".join(text.split())
    
    return text


def get_validated_input(prompt, validator, *validator_args):
    """
    Generic function to get validated input from user.
    Keeps asking until valid input is provided.
    
    Args:
        prompt: Input prompt to display
        validator: Validation function to use
        *validator_args: Additional arguments for validator
    
    Returns: validated value
    """
    while True:
        user_input = input(prompt).strip()
        
        result = validator(user_input, *validator_args)
        
        # Handle different return formats
        if len(result) == 2:  # (is_valid, message)
            is_valid, message = result
            value = user_input
        else:  # (is_valid, value, message)
            is_valid, value, message = result
        
        if is_valid:
            return value
        else:
            print(f"❌ {message}")


# Example usage functions for common inputs

def get_validated_phone():
    """Get validated phone number from user."""
    return get_validated_input("Enter phone number: ", validate_phone)


def get_validated_email():
    """Get validated email from user."""
    return get_validated_input("Enter email: ", validate_email)


def get_validated_password():
    """Get validated password from user."""
    from getpass import getpass
    while True:
        password = getpass("Enter password (min 6 chars, letters + numbers): ")
        is_valid, message = validate_password(password)
        if is_valid:
            return password
        else:
            print(f"❌ {message}")


def get_validated_name(field_name="Name"):
    """Get validated name from user."""
    return get_validated_input(f"Enter {field_name}: ", validate_name)


def get_validated_date(field_name="Date", format="%d-%m-%Y"):
    """Get validated date from user."""
    return get_validated_input(
        f"Enter {field_name} ({format}, e.g., 25-12-2000): ", 
        validate_date, 
        format
    )

def get_validated_price():
    """Get validated price from user."""
    while True:
        user_input = input("Enter price (₹): ").strip()
        is_valid, value, message = validate_price(user_input)
        if is_valid:
            return value
        else:
            print(f"❌ {message}")

def get_validated_quantity():
    """Get validated quantity from user."""
    while True:
        user_input = input("Enter quantity: ").strip()
        is_valid, value, message = validate_quantity(user_input)
        if is_valid:
            return value
        else:
            print(f"❌ {message}")

def get_validated_rating():
    """Get validated rating from user."""
    return get_validated_input("Enter rating (0.0 - 5.0): ", validate_rating)


def get_validated_category():
    """Get validated category from user."""
    return get_validated_input("Enter category: ", validate_category)


def get_validated_choice(min_val, max_val):
    """Get validated menu choice from user."""
    return get_validated_input(
        "Enter your choice: ", 
        validate_choice, 
        min_val, 
        max_val
    )


# Test function
def test_validators():
    """Test all validation functions."""
    print("=== VALIDATION TESTS ===\n")
    
    # Phone tests
    print("Phone Validation:")
    print(validate_phone("9876543210"))
    print(validate_phone("+919876543210"))
    print(validate_phone("1234567890"))
    print(validate_phone("98765"))
    
    # Email tests
    print("\nEmail Validation:")
    print(validate_email("user@example.com"))
    print(validate_email("invalid.email"))
    print(validate_email("test@domain"))
    
    # Password tests
    print("\nPassword Validation:")
    print(validate_password("pass123"))
    print(validate_password("weak"))
    print(validate_password("secure2024"))
    
    # Price tests
    print("\nPrice Validation:")
    print(validate_price("99.99"))
    print(validate_price("-10"))
    print(validate_price("abc"))
    
    # Quantity tests
    print("\nQuantity Validation:")
    print(validate_quantity("50"))
    print(validate_quantity("-5"))
    print(validate_quantity("10.5"))


if __name__ == "__main__":
    test_validators()