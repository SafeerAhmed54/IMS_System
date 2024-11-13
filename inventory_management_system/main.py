import os

# Paths to data files
USER_FILE_PATH = os.path.join(os.getcwd(), "Files", "users.txt")
PRODUCT_FILE_PATH = os.path.join(os.getcwd(), "Files", "products.txt")

print("Current Working Directory:", os.getcwd())


# User class to manage user data
class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def __str__(self):
        return f"{self.username},{self.password},{self.role}"


# Dictionary to hold users
users = {}


def file_read_users():
    try:
        if os.path.exists(USER_FILE_PATH):
            with open(USER_FILE_PATH, "r") as f:
                for line in f:
                    username, password, role = line.strip().split(",")
                    users[username] = User(username, password, role)
            print("User data loaded successfully.")
        else:
            print("User data file not found. Starting with an empty user list.")
    except Exception as e:
        print(f"Error reading user file: {e}")


def file_read_products():
    try:
        if os.path.exists(PRODUCT_FILE_PATH):
            with open(PRODUCT_FILE_PATH, "r") as f:
                for line in f:
                    product_id, name, category, price, stock_quantity = (
                        line.strip().split(",")
                    )
                    inventory[product_id] = Product(
                        product_id, name, category, float(price), int(stock_quantity)
                    )
            print("Product data loaded successfully.")
        else:
            print("Product data file not found. Starting with an empty inventory.")
    except Exception as e:
        print(f"Error reading product file: {e}")


# Save users to file
def file_write_users():
    with open(USER_FILE_PATH, "w") as f:
        for user in users.values():
            f.write(str(user) + "\n")
    print("User data saved successfully.")


# User login
def login():
    try:
        username = input("Enter username: ")
        password = input("Enter password: ")
        if username in users and users[username].password == password:
            print(f"Welcome, {users[username].role}!")
            return users[username]
        else:
            print("Invalid credentials. Try again.")
            return None
    except Exception as e:
        print(f"An error occurred during login: {e}")
        return None


def get_valid_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def get_valid_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")


# Create new user
def create_user():
    username = input("Enter username to create account: ")
    password = input("Enter password to create account: ")
    role = input("Enter the role: ")
    if username in users:
        print("Username already exists. Please choose a different username.")
    else:
        users[username] = User(username, password, role)
        print(f"User {username} with role {role} created successfully.")
        file_write_users()  # Save the new user to the file


# Retry login on failure
def login_invalid():
    while True:
        user = login()
        if user is not None:
            return user  # Exit the loop if login is successful


# Welcome message and option to create a new account
def welcome_message():
    while True:
        create_new = (
            input(
                "Hello! Welcome to the IMS app. Do you want to create a new account? Type 'yes' or 'no': "
            )
            .strip()
            .lower()
        )
        if create_new in ["yes", "no"]:
            break
        else:
            print("Invalid input. Please type 'yes' or 'no'.")

    if create_new == "yes":
        create_user()


# Product class to manage product data
class Product:
    def __init__(self, product_id, name, category, price, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock_quantity = stock_quantity

    def __str__(self):
        return f"{self.product_id},{self.name},{self.category},{self.price},{self.stock_quantity}"


# Dictionary to hold inventory
inventory = {}


# Save products to file
def file_write_products():
    with open(PRODUCT_FILE_PATH, "w") as f:
        for product in inventory.values():
            f.write(str(product) + "\n")
    print("Product data saved successfully.")


# Add new product
def add_product():
    product_id = input("Enter product ID: ")
    # Check for existing product ID
    if product_id in inventory:
        print("Product ID already exists. Please choose a different ID.")
        return  # Exit the function if the ID exists

    name = input("Enter product name: ")
    # Check for existing product name
    if any(product.name.lower() == name.lower() for product in inventory.values()):
        print("Product name already exists. Please choose a different name.")
        return  # Exit the function if the name exists

    category = input("Enter product category: ")
    price = float(input("Enter product price: "))
    stock_quantity = int(input("Enter stock quantity: "))

    inventory[product_id] = Product(product_id, name, category, price, stock_quantity)
    print(f"Product {name} added successfully.")
    file_write_products()  # Save the new product to the file


def edit_product(product_id):
    if product_id in inventory:
        try:
            name = input("Enter new product name (leave blank to keep current): ")
            category = input(
                "Enter new product category (leave blank to keep current): "
            )
            price = input("Enter new product price (leave blank to keep current): ")
            stock_quantity = input(
                "Enter new stock quantity (leave blank to keep current): "
            )

            if name:
                inventory[product_id].name = name
            if category:
                inventory[product_id].category = category
            if price:
                inventory[product_id].price = float(price)
            if stock_quantity:
                inventory[product_id].stock_quantity = int(stock_quantity)

            print(f"Product {product_id} updated successfully.")
            file_write_products()  # Save the updated product data to the file
        except ValueError as e:
            print(f"Invalid data provided: {e}")
    else:
        print("Product not found.")


def adjust_stock():
    product_id = input("Enter product ID to adjust stock: ")
    if product_id in inventory:
        try:
            adjustment = get_valid_int(
                "Enter adjustment (positive to restock, negative to reduce): "
            )
            inventory[product_id].stock_quantity += adjustment
            if inventory[product_id].stock_quantity < 0:
                print("Stock quantity cannot be negative. Adjusting to 0.")
                inventory[product_id].stock_quantity = 0
            print(
                f"Stock for {inventory[product_id].name} updated to {inventory[product_id].stock_quantity}."
            )
            file_write_products()  # Save the updated product data to the file

            if inventory[product_id].stock_quantity < 50:  # Low stock threshold
                print(
                    f"Warning: Stock for {inventory[product_id].name} is low ({inventory[product_id].stock_quantity}). Consider restocking."
                )
        except ValueError:
            print("Invalid input for stock adjustment.")
    else:
        print("Product not found.")


# View inventory
def view_inventory(user):
    print("Current Inventory:")
    for product in inventory.values():
        print(product)


# Search for products
def search_product():
    search_type = input("Search by [name, category]: ").strip().lower()
    search_value = input("Enter search value: ").strip().lower()

    found_products = []
    for product in inventory.values():
        if (search_type == "name" and search_value in product.name.lower()) or (
            search_type == "category" and search_value in product.category.lower()
        ):
            found_products.append(product)

    if found_products:
        print("Search Results:")
        for product in found_products:
            print(product)
    else:
        print("No products found.")


def Role_Check():
    """Manages the login process and allows actions based on user roles."""
    while True:
        # Attempt login and allow retry if the first attempt fails
        user = login()
        if user is None:
            user = login_invalid()

        # Provide options based on the user's role
        if user.role.lower() == "admin":
            print("Access granted to Admin functionalities.")
            while True:
                action = input(
                    "Choose action: [add, edit, view, search, adjust stock, logout]: "
                ).lower()
                if action == "add":
                    add_product()
                elif action == "edit":
                    product_id = input("Enter product ID to edit: ")
                    edit_product(product_id)
                elif action == "view":
                    view_inventory(user)
                elif action == "search":
                    search_product()
                elif action == "adjust stock":
                    adjust_stock()
                elif action == "logout":
                    print("Logging out.")
                    break
                else:
                    print("Invalid action. Please choose a valid option.")
        elif user.role.lower() == "user":
            print("Access granted to basic functionalities.")
            while True:
                action = input("Choose action: [view, search, logout]: ").lower()
                if action == "view":
                    view_inventory(user)
                elif action == "search":
                    search_product()
                elif action == "logout":
                    print("Logging out.")
                    break
                else:
                    print("Invalid action. Please choose a valid option.")

        # After logging out, prompt the user to log in again or quit
        choice = (
            input(
                "Do you want to log in again or quit? Type 'login' to log in again or 'quit' to exit: "
            )
            .strip()
            .lower()
        )
        if choice == "quit":
            print("Exiting the system. Goodbye!")
            break
        elif choice != "login":
            print("Invalid input. Exiting the system.")
            break


# Main function to initialize and handle user interactions
def main():
    file_read_users()  # Load existing users from file
    file_read_products()  # Load existing products from file
    welcome_message()
    Role_Check()


if __name__ == "__main__":
    main()
