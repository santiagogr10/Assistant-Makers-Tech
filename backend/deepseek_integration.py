from deepseek_client import get_client

# Obtener el cliente configurado
client = get_client()

def generate_response(user_message: str) -> str:
    """
    Genera una respuesta basada en el mensaje del usuario usando la API de Deepseek.

    Args:
        user_message (str): Consulta del usuario en lenguaje natural.

    Returns:
        str: Respuesta generada por la IA.
    """
    try:
        # Preparar el prompt
        prompt = (
            "Eres un asistente de Makers Tech. Responde preguntas sobre inventario, "
            "características y precios de productos de manera clara y directa."
        )

        # Enviar el mensaje a la API de Deepseek
        response = client.chat.completions.create(
            model="deepseek-chat",  # Cambiar si Deepseek tiene otros modelos
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.7
        )

        # Extraer la respuesta de la IA
        return response.choices[0].message.content.strip()

    except Exception as e:
        # Manejar errores
        return f"Error al generar la respuesta: {e}"


# Prueba directa
if __name__ == "__main__":
    user_input = input("Escribe tu consulta: ")
    respuesta = generate_response(user_input)
    print("Respuesta de la IA:")
    print(respuesta)
