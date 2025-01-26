from backend.deepseek_client import get_client
import sqlite3

# Get the configured client
client = get_client()


DB_NAME = "store.db"


def fetch_user_history(user_id: int, db_name=DB_NAME) -> str:
    """
    Queries the user's purchase history from the database.

    Args:
        user_id (int): The user's ID.
        db_name (str): The name of the database.

    Returns:
        str: The user's purchase history as a string.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT purchase_history FROM users WHERE user_id = ?;", (user_id,))
    result = cursor.fetchone()
    conn.close()

    return result[0] if result else ""


def fetch_inventory(db_name=DB_NAME) -> list:
    """
    Queries the inventory products from the database.

    Args:
        db_name (str): The name of the database.

    Returns:
        list: A list of inventory products.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT name, category, brand, price, stock FROM products;")
    products = cursor.fetchall()
    conn.close()

    return products


def classify_products(user_history: str, inventory: list) -> dict:
    """
    Classifies products into categories based on the user's purchase history.

    Args:
        user_history (str): The user's purchase history.
        inventory (list): The inventory products list.

    Returns:
        dict: Products categorized into specific groups.
    """
    categories = {"Highly Recommended": [], "Recommended": [], "Not Recommended": []}

    for product in inventory:
        name, category, brand, _, stock = product
        if stock <= 0:
            continue  # Skip out-of-stock items

        if brand in user_history or category in user_history:
            categories["Highly Recommended"].append(name)
        elif any(item in user_history for item in [brand, category]):
            categories["Recommended"].append(name)
        else:
            categories["Not Recommended"].append(name)

    return categories


def fetch_database_context(db_name=DB_NAME) -> str:
    """
    Retrieves the full database context to be used for queries.

    Args:
        db_name (str): The name of the database.

    Returns:
        str: The database context as a formatted string.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Adjust the query to retrieve the necessary context
    cursor.execute("SELECT name, category, brand, price, stock FROM products;")
    products = cursor.fetchall()
    conn.close()

    # Format the database context
    database_context = "\n".join(
        f"{name} ({category} - {brand}): Price ${price}, Stock: {stock}"
        for name, category, brand, price, stock in products
    )

    return database_context


def generate_response(user_message: str, user_id: int = None, db_name=DB_NAME) -> dict:
    """
    Generates a response based on the user's message and the database context.

    Args:
        user_message (str): The user's natural language query.
        user_id (int, optional): The user's ID.
        db_name (str): The name of the database.

    Returns:
        dict: The AI-generated response.
    """
    try:
        # Retrieve the database context
        database_context = fetch_database_context(db_name)

        # Prepare the prompt
        prompt = (
            "You are an intelligent assistant for Makers Tech. Respond to the user's queries based on the following database information:\n"
            f"{database_context}\n\n"
            "User query:\n"
            f"{user_message}\n"
        )

        # Send the prompt to the AI
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message},
            ],
            max_tokens=500,
            temperature=0.7,
        )

        # Extract and return the response
        return {"status": "success", "response": response.choices[0].message.content.strip()}

    except Exception as e:
        return {"status": "error", "message": f"Error generating the response: {e}"}


# Direct test
if __name__ == "__main__":
    user_id = int(input("Enter your user ID: "))
    user_input = input("Enter your query: ")
    response = generate_response(user_input, user_id)
    print("System response:")
    print(response)
