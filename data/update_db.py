import sqlite3


def update_products(db_name="store.db"):
    """
    Inserts or updates data in the 'products' table.

    Args:
        db_name (str): Name of the database file.
    """
    products = [
        (
            1,
            "MacBook Air",
            "Computers",
            "Apple",
            999,
            5,
            "Lightweight and powerful laptop",
            "M1 chip, 256GB SSD, 8GB RAM",
        ),
        (
            2,
            "Dell Inspiron 15",
            "Computers",
            "Dell",
            650,
            10,
            "Affordable performance laptop",
            "i5, 512GB SSD, 8GB RAM",
        ),
        (
            3,
            "HP Pavilion 14",
            "Computers",
            "HP",
            700,
            8,
            "Sleek design with good specs",
            "i5, 256GB SSD, 16GB RAM",
        ),
        (
            4,
            "iPhone 14 Pro",
            "Smartphones",
            "Apple",
            1099,
            15,
            "Advanced smartphone features",
            "A16 chip, 256GB, Pro camera",
        ),
        (
            5,
            "Samsung Galaxy S22",
            "Smartphones",
            "Samsung",
            899,
            20,
            "High-performance smartphone",
            "Exynos 2200, 128GB, AMOLED display",
        ),
        (
            6,
            "Google Pixel 7",
            "Smartphones",
            "Google",
            799,
            12,
            "Excellent camera and clean Android UI",
            "Tensor G2, 128GB, 6.3-inch OLED",
        ),
        (
            7,
            "Logitech MX Master 3",
            "Peripherals",
            "Logitech",
            100,
            25,
            "Ergonomic wireless mouse",
            "Bluetooth, USB-C charging, customizable",
        ),
        (
            8,
            "Razer BlackWidow V3",
            "Peripherals",
            "Razer",
            150,
            18,
            "High-performance mechanical keyboard",
            "RGB lighting, tactile switches",
        ),
        (
            9,
            "Samsung T7 Portable SSD",
            "Peripherals",
            "Samsung",
            120,
            30,
            "Portable SSD for fast data storage",
            "1TB capacity, USB 3.2 Gen 2",
        ),
        (
            10,
            "Dell UltraSharp U2723QE",
            "Peripherals",
            "Dell",
            750,
            10,
            "High-resolution 4K monitor",
            "27-inch UHD 4K, IPS, USB-C connectivity",
        ),
    ]

    # Connect to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Insert or ignore products
    cursor.executemany(
        """
    INSERT OR IGNORE INTO products (product_id, name, category, brand, price, stock, description, features)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """,
        products,
    )

    print("Data successfully inserted or updated in 'products'.")

    # Commit changes and close the connection
    conn.commit()
    conn.close()


def update_users(db_name="store.db"):
    """
    Inserts or updates data in the 'users' table.

    Args:
        db_name (str): Name of the database file.
    """
    users = [
        (
            1,
            "John Doe",
            "john.doe@example.com",
            "Computers, Peripherals",
            "MacBook Air, Logitech MX Master 3",
        ),
        (
            2,
            "Jane Smith",
            "jane.smith@example.com",
            "Smartphones, Peripherals",
            "iPhone 14 Pro, Samsung T7 SSD",
        ),
        (3, "Alex Johnson", "alex.j@example.com", "Gaming Accessories", "Razer BlackWidow V3"),
        (
            4,
            "Emily Carter",
            "emily.c@example.com",
            "Samsung Products, Smartphones",
            "Samsung Galaxy S22, Samsung T7 SSD",
        ),
        (
            5,
            "Michael Brown",
            "michael.b@example.com",
            "High-end Computers",
            "Dell UltraSharp U2723QE",
        ),
    ]

    # Connect to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Insert or ignore users
    cursor.executemany(
        """
    INSERT OR IGNORE INTO users (user_id, name, email, preferences, purchase_history)
    VALUES (?, ?, ?, ?, ?);
    """,
        users,
    )

    print("Data successfully inserted or updated in 'users'.")

    # Commit changes and close the connection
    conn.commit()
    conn.close()


if __name__ == "__main__":
    update_products()
    update_users()
