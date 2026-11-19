import sqlite3
from contextlib import closing

DB_NAME = "inventory.db"
LOW_STOCK_LIMIT = 5


def connect_db():
    """Create and return a connection to the inventory database."""
    return sqlite3.connect(DB_NAME)


def create_table():
    """Create the products table if it does not already exist."""
    with closing(connect_db()) as connection, connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL COLLATE NOCASE,
                price REAL NOT NULL CHECK (price >= 0),
                stock INTEGER NOT NULL CHECK (stock >= 0)
            )
        """)


def get_non_empty_text(prompt):
    """Keep asking until the user enters non-empty text."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")


def get_non_negative_integer(prompt):
    """Get an integer that is zero or greater."""
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
            if number < 0:
                print("Please enter zero or a positive number.")
                continue
            return number
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def get_positive_integer(prompt):
    """Get an integer greater than zero."""
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
            if number <= 0:
                print("Please enter a number greater than zero.")
                continue
            return number
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def get_non_negative_price(prompt):
    """Get a valid non-negative product price."""
    while True:
        value = input(prompt).strip()
        try:
            price = float(value)
            if price < 0:
                print("Price cannot be negative.")
                continue
            return price
        except ValueError:
            print("Invalid price. Please enter a number, such as 250 or 250.50.")


def add_product():
    print("\n--- Add Product ---")
    name = get_non_empty_text("Enter product name: ")
    price = get_non_negative_price("Enter product price: ₹")
    stock = get_non_negative_integer("Enter available stock: ")

    with closing(connect_db()) as connection, connection:
        connection.execute(
            "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
            (name, price, stock)
        )

    print("Product added successfully.")


def view_inventory():
    print("\n--- Inventory ---")
    with closing(connect_db()) as connection, connection:
        products = connection.execute(
            "SELECT id, name, price, stock FROM products ORDER BY id"
        ).fetchall()

    if not products:
        print("Inventory is empty.")
        return

    print("-" * 75)
    print(f"{'ID':<6}{'Product Name':<35}{'Price (₹)':>15}{'Stock':>12}")
    print("-" * 75)

    for product_id, name, price, stock in products:
        print(f"{product_id:<6}{name:<35}{price:>15.2f}{stock:>12}")

    print("-" * 75)


def search_product():
    print("\n--- Search Product ---")
    search_term = get_non_empty_text("Enter product ID or product name: ")

    with closing(connect_db()) as connection, connection:
        if search_term.isdigit():
            products = connection.execute(
                "SELECT id, name, price, stock FROM products WHERE id = ?",
                (int(search_term),)
            ).fetchall()
        else:
            products = connection.execute(
                """SELECT id, name, price, stock
                   FROM products
                   WHERE name LIKE ? COLLATE NOCASE
                   ORDER BY id""",
                (f"%{search_term}%",)
            ).fetchall()

    if not products:
        print("No matching product found.")
        return

    print("-" * 75)
    print(f"{'ID':<6}{'Product Name':<35}{'Price (₹)':>15}{'Stock':>12}")
    print("-" * 75)
    for product_id, name, price, stock in products:
        print(f"{product_id:<6}{name:<35}{price:>15.2f}{stock:>12}")
    print("-" * 75)


def update_product():
    print("\n--- Update Product ---")
    product_id = get_positive_integer("Enter product ID to update: ")

    with closing(connect_db()) as connection, connection:
        product = connection.execute(
            "SELECT id, name, price, stock FROM products WHERE id = ?",
            (product_id,)
        ).fetchone()

    if product is None:
        print("Product not found.")
        return

    print(f"Selected product: {product[1]}")
    new_price = get_non_negative_price("Enter new price: ₹")
    new_stock = get_non_negative_integer("Enter new stock quantity: ")

    with closing(connect_db()) as connection, connection:
        cursor = connection.execute(
            "UPDATE products SET price = ?, stock = ? WHERE id = ?",
            (new_price, new_stock, product_id)
        )

    if cursor.rowcount == 1:
        print("Product updated successfully.")
    else:
        print("Product could not be updated because it no longer exists.")


def delete_product():
    print("\n--- Delete One Product ---")
    product_id = get_positive_integer("Enter product ID to delete: ")

    with closing(connect_db()) as connection, connection:
        product = connection.execute(
            "SELECT name FROM products WHERE id = ?",
            (product_id,)
        ).fetchone()

    if product is None:
        print("Product not found.")
        return

    print(f"Product selected: {product[0]}")
    confirmation = input("Are you sure you want to delete it? Type YES to confirm: ").strip()

    if confirmation != "YES":
        print("Deletion cancelled.")
        return

    with closing(connect_db()) as connection, connection:
        cursor = connection.execute(
            "DELETE FROM products WHERE id = ?",
            (product_id,)
        )

    if cursor.rowcount == 1:
        print("Product deleted successfully.")
    else:
        print("Product could not be deleted because it no longer exists.")


def parse_product_ids(raw_ids):
    """Parse comma-separated positive IDs, removing duplicates in input order."""
    pieces = raw_ids.split(",")
    if not pieces or any(not piece.strip() for piece in pieces):
        raise ValueError("Enter IDs separated by commas, without empty entries.")

    ids = []
    seen = set()

    for piece in pieces:
        value = piece.strip()
        try:
            product_id = int(value)
        except ValueError:
            raise ValueError(f"'{value}' is not a valid whole-number ID.")

        if product_id <= 0:
            raise ValueError("Product IDs must be greater than zero.")

        if product_id not in seen:
            ids.append(product_id)
            seen.add(product_id)

    return ids


def delete_multiple_products():
    print("\n--- Delete Multiple Products ---")
    print("Enter product IDs separated by commas, for example: 1, 3, 4")

    while True:
        raw_ids = input("Enter product IDs: ").strip()
        try:
            product_ids = parse_product_ids(raw_ids)
            break
        except ValueError as error:
            print(f"Invalid input: {error}")

    placeholders = ",".join("?" for _ in product_ids)

    with closing(connect_db()) as connection, connection:
        selected_products = connection.execute(
            f"""SELECT id, name, price, stock
                FROM products
                WHERE id IN ({placeholders})
                ORDER BY id""",
            product_ids
        ).fetchall()

    if not selected_products:
        print("No products were found for the IDs you entered.")
        return

    found_ids = [product[0] for product in selected_products]
    missing_ids = [product_id for product_id in product_ids if product_id not in found_ids]

    print("\nThe following products will be deleted:")
    print("-" * 60)
    print(f"{'ID':<8}{'Product Name':<35}{'Stock':>10}")
    print("-" * 60)
    for product_id, name, price, stock in selected_products:
        print(f"{product_id:<8}{name:<35}{stock:>10}")
    print("-" * 60)

    if missing_ids:
        print("These IDs were not found and will be skipped:", ", ".join(map(str, missing_ids)))

    confirmation = input(
        f"Delete these {len(selected_products)} product(s)? Type YES to confirm: "
    ).strip()

    if confirmation != "YES":
        print("Bulk deletion cancelled. No products were deleted.")
        return

    delete_placeholders = ",".join("?" for _ in found_ids)

    # The IDs are passed as parameters; only the number of placeholders is built dynamically.
    with closing(connect_db()) as connection, connection:
        cursor = connection.execute(
            f"DELETE FROM products WHERE id IN ({delete_placeholders})",
            found_ids
        )

    print(f"Successfully deleted {cursor.rowcount} product(s).")


def show_inventory_value():
    print("\n--- Total Inventory Value ---")
    with closing(connect_db()) as connection, connection:
        result = connection.execute(
            "SELECT COALESCE(SUM(price * stock), 0) FROM products"
        ).fetchone()

    total_value = result[0]
    print(f"Total inventory value: ₹{total_value:,.2f}")


def low_stock_report():
    print("\n--- Low Stock Report ---")
    with closing(connect_db()) as connection, connection:
        products = connection.execute(
            """SELECT id, name, price, stock
               FROM products
               WHERE stock <= ?
               ORDER BY stock, id""",
            (LOW_STOCK_LIMIT,)
        ).fetchall()

    if not products:
        print("No low-stock products found.")
        return

    print(f"Products with stock of {LOW_STOCK_LIMIT} or fewer:")
    print("-" * 75)
    print(f"{'ID':<6}{'Product Name':<35}{'Price (₹)':>15}{'Stock':>12}")
    print("-" * 75)
    for product_id, name, price, stock in products:
        print(f"{product_id:<6}{name:<35}{price:>15.2f}{stock:>12}")
    print("-" * 75)


def show_menu():
    print("\n========== INVENTORY MANAGEMENT SYSTEM ==========")
    print("1. Add Product")
    print("2. View Inventory")
    print("3. Search Product")
    print("4. Update Product")
    print("5. Delete One Product")
    print("6. Show Total Inventory Value")
    print("7. Low Stock Report")
    print("8. Exit")
    print("9. Delete Multiple Products")
    print("==================================================")


def main():
    create_table()
    print("Welcome to the Inventory Management System!")

    while True:
        show_menu()
        choice = input("Enter your choice (1-9): ").strip()

        if choice == "1":
            add_product()
        elif choice == "2":
            view_inventory()
        elif choice == "3":
            search_product()
        elif choice == "4":
            update_product()
        elif choice == "5":
            delete_product()
        elif choice == "6":
            show_inventory_value()
        elif choice == "7":
            low_stock_report()
        elif choice == "8":
            print("Thank you for using the Inventory Management System. Goodbye!")
            break
        elif choice == "9":
            delete_multiple_products()
        else:
            print("Invalid choice. Please enter a number from 1 to 9.")


if __name__ == "__main__":
    main()
