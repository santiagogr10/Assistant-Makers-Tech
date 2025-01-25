from backend.deepseek_client import get_client
from backend.database_reader import fetch_database_context  # Importar la función combinada

# Obtener el cliente configurado
client = get_client()

def generate_response(user_message: str, user_id: int = None, db_name="store.db") -> dict:
    """
    Genera una respuesta basada en el mensaje del usuario y el contexto completo de la base de datos.

    Args:
        user_message (str): Consulta del usuario en lenguaje natural.
        user_id (int, opcional): ID del usuario.
        db_name (str): Nombre de la base de datos.

    Returns:
        dict: Respuesta generada por la IA.
    """
    try:
        # Obtener el contexto completo de la base de datos
        database_context = fetch_database_context(db_name)

        # Personalizar el contexto si se proporciona un user_id
        user_context = f"ID del usuario: {user_id}\n" if user_id else "Usuario no identificado\n"

        # Preparar el prompt
        prompt = (
            "Eres un asistente inteligente para Makers Tech. Clasifica los productos en las siguientes categorías:\n"
            "- Highly Recommended: Coinciden con las marcas o categorías del historial del usuario.\n"
            "- Recommended: Relación indirecta o complementaria.\n"
            "- Not Recommended: Sin conexión relevante.\n\n"
            f"{user_context}"
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
    user_id = input("Ingresa tu ID de usuario (opcional): ")
    user_input = input("Escribe tu consulta: ")
    user_id = int(user_id) if user_id.isdigit() else None  # Convertir a int si es válido
    respuesta = generate_response(user_input, user_id)
    print("Respuesta del sistema:")
    print(respuesta)
