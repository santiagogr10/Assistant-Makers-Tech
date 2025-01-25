import requests

BASE_URL = "http://127.0.0.1:5000/api/chat"

# Solicitar inputs al usuario
user_id = input("Ingresa tu ID de usuario (opcional, deja en blanco si no hay login): ")
user_message = input("Escribe tu consulta para el asistente virtual: ")

# Crear el payload con los datos del usuario y el mensaje
payload = {
    "user_id": user_id if user_id else None,  # Si no hay login, dejamos user_id como None
    "message": user_message
}

# Enviar la solicitud al endpoint de chat
response = requests.post(BASE_URL, json=payload)

# Imprimir la respuesta del servidor
print("Respuesta del Servidor:")
print(response.json())
