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
        
        # Preparar el prompt con instrucciones específicas para diferentes tipos de consultas
        prompt = """
        You are a Makers Tech assistant. Follow these specific response formats based on the type of query:

        1. For stock queries (when users ask about quantity or availability):
        Response format: "The [Product Name] has [X] units in stock."
        Example: "The MacBook Pro has 15 units in stock."

        2. For price queries:
        Response format: "The [Product Name] costs $[Price]."
        Example: "The iPhone 13 costs $999."

        3. For product recommendations, strictly follow these classification criteria and format:

        When providing recommendations, ALWAYS use this EXACT markdown format with separators:
        say that given the purchase history, give the user recommendations for products that are highly recommended, recommended and not recommended.
        and explain why each product is recommended or not recommended.
        explain that the recomenendations are based on the purchase history.
        ----

        ## Highly Recommended:
        - [Product 1]: [Brief reason with specific details about brand/category match]
        - [Product 2]: [Brief reason with specific details about brand/category match]

        ## Recommended:
        - [Product 1]: [Brief reason explaining the related category or complementary use]
        - [Product 2]: [Brief reason explaining the related category or complementary use]

        ## Not Recommended:
        - [Product 1]: [Brief reason explaining why it doesn't match user preferences]
        - [Product 2]: [Brief reason explaining why it doesn't match user preferences]
        ----

        Classification criteria:
        - Highly Recommended:
          * Products from brands the user has already purchased
          * Products in categories from user's history
          * Complementary products to existing purchases
          * Must be in stock

        - Recommended:
          * Products from related categories
          * Generic complementary products
          * Can be from different brands
          * Must be in stock

        - Not Recommended:
          * Products unrelated to user's brands/categories
          * Non-complementary items
          * Products without clear utility for user's needs

        4. For general product information:
        Response format: "[Product Name]: [Category] by [Brand], priced at $[Price] with [X] units in stock."
        Example: "MacBook Pro: Laptop by Apple, priced at $1299 with 15 units in stock."

        Available product information:
        {database_context}

        User message:
        {user_message}

        Remember to:
        1. Be concise and direct
        2. Use the exact format specified for each type of query
        3. Use markdown formatting ONLY for recommendations section
        4. Always include the ---- separators and ## headers in recommendations
        5. Provide only the information that was asked for
        """

        # Send the prompt to the AI
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": prompt.format(
                    database_context=database_context,
                    user_message=user_message
                )},
                {"role": "user", "content": user_message}
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
