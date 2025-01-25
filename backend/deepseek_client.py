from openai import OpenAI
from dotenv import load_dotenv
import os

# Cargar las variables del archivo .env
load_dotenv()

# Obtener la API Key desde .env
api_key = os.getenv("DEEPSEEK_API_KEY")

# Configurar el cliente de la API
client = OpenAI(
    api_key=api_key,  # Usar la API Key desde .env
    base_url="https://api.deepseek.com"  # URL de la API de DeepSeek
)

def get_client():
    """
    Devuelve una instancia del cliente configurado para usar en otros módulos.
    """
    if not api_key:
        raise ValueError("API Key no encontrada. Asegúrate de configurarla en el archivo .env")
    return client
