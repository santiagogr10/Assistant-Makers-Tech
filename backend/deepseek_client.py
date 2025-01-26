from openai import OpenAI
from dotenv import load_dotenv
import os

# Load variables from the .env file
load_dotenv()

# Retrieve the API Key from the .env file
api_key = os.getenv("DEEPSEEK_API_KEY")

# Configure the API client
client = OpenAI(
    api_key=api_key,  # Use the API Key from .env
    base_url="https://api.deepseek.com",  # DeepSeek API URL
)


def get_client():
    """
    Returns a configured client instance to be used in other modules.

    Raises:
        ValueError: If the API Key is not found in the .env file.
    """
    if not api_key:
        raise ValueError("API Key not found. Make sure it is set in the .env file.")
    return client
