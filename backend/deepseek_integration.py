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

    Args:
        user_message (str): Consulta del usuario en lenguaje natural.
        user_id (int, opcional): ID del usuario.
        db_name (str): Nombre de la base de datos.

    Returns:
        dict: Respuesta generada por la IA.
    """
    try:
        # Obtener el contexto de la base de datos
        database_context = fetch_database_context(db_name)

        # Preparar el prompt
        prompt = (
            "Eres un asistente inteligente para Makers Tech. Responde a las consultas del usuario basándote en la siguiente información de la base de datos:\n"
            f"{database_context}\n\n"
            "Consulta del usuario:\n"
            f"{user_message}\n"
        )

        # Enviar el prompt a la IA
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": prompt},
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
