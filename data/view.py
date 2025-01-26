import sqlite3


def view_database(db_name="store.db"):
    """
    Displays the structure and data of the database.

    Args:
        db_name (str): Name of the database file.
    """
    try:
        # Connect to the database
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Display the existing tables
        print("\nExisting tables in the database:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            print(f"- {table[0]}")

        # Display data from each table
        for table in tables:
            table_name = table[0]
            print(f"\nData in the table '{table_name}':")
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()

            # Get the column names
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = [col[1] for col in cursor.fetchall()]
            print(f"Columns: {columns}")

            # Display the data
            if rows:
                for row in rows:
                    print(row)
            else:
                print("(Table is empty)")

        # Close the connection
        conn.close()

    except Exception as e:
        print(f"Error while viewing the database: {e}")


if __name__ == "__main__":
    view_database()
