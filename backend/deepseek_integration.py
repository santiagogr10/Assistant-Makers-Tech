from backend.deepseek_client import get_client
import sqlite3

# Obtener el cliente configurado
client = get_client()

def fetch_user_history(user_id: int, db_name="store.db") -> str:
    """
    Consulta el historial de compras del usuario en la base de datos.

    Args:
        user_id (int): ID del usuario.
        db_name (str): Nombre de la base de datos.

    Returns:
        str: Historial de compras del usuario como string.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT purchase_history FROM users WHERE user_id = ?;", (user_id,))
    result = cursor.fetchone()
    conn.close()

    return result[0] if result else ""


def fetch_inventory(db_name="store.db") -> list:
    """
    Consulta los productos del inventario en la base de datos.

    Args:
        db_name (str): Nombre de la base de datos.

    Returns:
        list: Lista de productos del inventario.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT name, category, brand, price, stock FROM products;")
    products = cursor.fetchall()
    conn.close()

    return products


def classify_products(user_history: str, inventory: list) -> dict:
    """
    Clasifica los productos en categorías basadas en el historial del usuario.

    Args:
        user_history (str): Historial de compras del usuario.
        inventory (list): Lista de productos del inventario.

    Returns:
        dict: Productos clasificados en categorías.
    """
    categories = {
        "Highly Recommended": [],
        "Recommended": [],
        "Not Recommended": []
    }

    for product in inventory:
        name, category, brand, price, stock = product
        if stock <= 0:
            continue  # Skip out-of-stock items

        if brand in user_history or category in user_history:
            categories["Highly Recommended"].append(name)
        elif any(item in user_history for item in [brand, category]):
            categories["Recommended"].append(name)
        else:
            categories["Not Recommended"].append(name)

    return categories


def fetch_database_context(db_name="store.db") -> str:
    """
    Obtiene el contexto completo de la base de datos para ser usado en las consultas.

    Args:
        db_name (str): Nombre de la base de datos.

    Returns:
        str: Contexto de la base de datos como string.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Aquí puedes ajustar la consulta para obtener el contexto necesario
    cursor.execute("SELECT name, category, brand, price, stock FROM products;")
    products = cursor.fetchall()
    conn.close()

    # Formatear el contexto de la base de datos
    database_context = "\n".join(
        f"{name} ({category} - {brand}): Precio ${price}, Stock: {stock}"
        for name, category, brand, price, stock in products
    )

    return database_context


def generate_response(user_message: str, user_id: int = None, db_name="store.db") -> dict:
    """
    Genera una respuesta basada en el mensaje del usuario y el contexto de la base de datos.
    """
    try:
        # Obtener el contexto de la base de datos
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

        # Enviar el prompt a la IA
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
            temperature=0.7
        )

        # Extraer y devolver la respuesta
        return {
            "status": "success",
            "response": response.choices[0].message.content.strip()
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error al generar la respuesta: {e}"
        }


# Prueba directa
if __name__ == "__main__":
    user_id = int(input("Ingresa tu ID de usuario: "))
    user_input = input("Escribe tu consulta: ")
    respuesta = generate_response(user_input, user_id)
    print("Respuesta del sistema:")
    print(respuesta)
