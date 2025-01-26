import os
import sys

# Agregar el directorio raíz al PYTHONPATH
sys.path.append(os.path.dirname(__file__))

# Ejecutar la aplicación de Streamlit
os.system("streamlit run frontend/app.py") 