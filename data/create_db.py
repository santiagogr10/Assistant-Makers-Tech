import sqlite3


def create_database(db_name="store.db"):
    """
    Creates the database with the tables 'products' and 'users'.
    If the tables already exist, they will not be recreated.

    Args:
        db_name (str): Name of the database file.
    """
    # Connect to or create the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create the 'products' table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        brand TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL,
        description TEXT,
        features TEXT
    );
    """
    )

    # Create the 'users' table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        preferences TEXT,
        purchase_history TEXT
    );
    """
    )

    print("Database and tables created successfully.")

    # Commit changes and close the connection
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
