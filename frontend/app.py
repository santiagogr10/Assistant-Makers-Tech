import streamlit as st
import requests

# Configuración de la página
st.set_page_config(page_title="Makers Tech ChatBot", layout="wide")

# Título y descripción
st.title("Makers Tech ChatBot")
st.write("Bienvenido a Makers Tech. Aquí puedes consultar el inventario y obtener información sobre nuestros productos.")

# Divisor para separar secciones
st.divider()

# Entrada del usuario
user_input = st.text_input("Escribe tu consulta:", placeholder="¿Cuántos laptops están disponibles?")

# Inicializar el historial de mensajes
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Mostrar historial de conversación
st.subheader("Historial de conversación")
for msg in st.session_state["messages"]:
    st.write(msg)

# Divisor para separar secciones
st.divider()

# Botón para enviar consulta
if st.button("Enviar"):
    if user_input.strip() != "":
        try:
            # Llamada al backend
            response = requests.post(
                "http://127.0.0.1:8000/chatbot",  # Cambia esta URL por la del backend
                json={"query": user_input}
            )
            if response.status_code == 200:
                data = response.json()
                # Guardar mensajes en el historial
                st.session_state["messages"].append(f"Tú: {user_input}")
                st.session_state["messages"].append(f"ChatBot: {data['response']}")
                # Mostrar la respuesta del chatbot
                st.write(f"Respuesta del chatbot: {data['response']}")
            else:
                st.error("Hubo un error al obtener la respuesta del servidor.")
        except Exception as e:
            st.error(f"No se pudo conectar con el servidor: {e}")
    else:
        st.warning("Por favor, escribe una consulta antes de enviar.")

# Divisor para separar secciones
st.divider()

# Footer
st.write("**Makers Tech ChatBot** © 2025 - Todos los derechos reservados")
