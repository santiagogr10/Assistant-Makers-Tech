import sqlite3


def get_database_content_as_dict(db_name="store.db") -> dict:
    """
    Retrieves the entire database content as a dictionary.

    Args:
        db_name (str): Name of the database.

    Returns:
        dict: Dictionary containing the database content.
    """
    try:
        # Connect to the database
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Execute a query to fetch all tables in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Initialize a dictionary to store the database content
        database_content = {}

        # Iterate over each table to fetch their contents
        for (table_name,) in tables:
            cursor.execute(f"SELECT * FROM {table_name}")
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()

            # Store the table data in the dictionary
            database_content[table_name] = [dict(zip(columns, row)) for row in rows]

        # Close the database connection
        conn.close()

        parsed_data = {
            "Product": [],
            "Category": [],
            "Brand": [],
            "Stock": [],
            "Price": [],
        }

        # Extract product information and map to table format
        for product in database_content.get("products", []):
            parsed_data["Product"].append(product["name"])
            parsed_data["Category"].append(product["category"])
            parsed_data["Brand"].append(product["brand"])
            parsed_data["Stock"].append(product["stock"])
            parsed_data["Price"].append(
                f"${product['price']:.2f}"
            )  # Format price as string with 2 decimals

        return parsed_data

    except Exception as e:
        return {"status": "error", "message": f"Error retrieving the database content: {e}"}
