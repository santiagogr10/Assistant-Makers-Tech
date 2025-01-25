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


def fetch_inventory(db_name="store.db") -> str:
    """
    Consulta los productos del inventario en la base de datos.

    Args:
        db_name (str): Nombre de la base de datos.

    Returns:
        str: Productos del inventario como texto estructurado.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT name, category, brand, price, stock FROM products;")
    products = cursor.fetchall()
    conn.close()

    inventory = "Inventario de productos:\n"
    for product in products:
        name, category, brand, price, stock = product
        inventory += f"- {name} ({category} - {brand}): Precio ${price}, Stock: {stock}\n"

    return inventory


def generate_response(user_message: str, user_id: int, db_name="store.db") -> dict:
    """
    Genera una respuesta basada en el mensaje del usuario y su historial.

    Args:
        user_message (str): Consulta del usuario en lenguaje natural.
        user_id (int): ID del usuario.
        db_name (str): Nombre de la base de datos.

    Returns:
        dict: Respuesta generada por la IA.
    """
    try:
        # Obtener historial del usuario e inventario
        user_history = fetch_user_history(user_id, db_name)
        inventory = fetch_inventory(db_name)

        # Preparar el prompt
        prompt = (
            "Eres un asistente inteligente para Makers Tech. Clasifica los productos en las siguientes categorías:\n"
            "- Highly Recommended: Coinciden con las marcas o categorías del historial del usuario.\n"
            "- Recommended: Relación indirecta o complementaria.\n"
            "- Not Recommended: Sin conexión relevante.\n\n"
            f"Historial del usuario:\n{user_history}\n\n"
            f"{inventory}\n\n"
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
