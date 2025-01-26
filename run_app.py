import os
import sys

# Add the root directory to PYTHONPATH
sys.path.append(os.path.dirname(__file__))

# Run the Streamlit application
os.system("streamlit run frontend/app.py")
