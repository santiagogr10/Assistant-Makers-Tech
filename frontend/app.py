import streamlit as st
from chatbot_ui import apply_custom_css, show_chatbot, show_recommendations, show_dashboard

# Page configuration (must be the first Streamlit command)
st.set_page_config(page_title="Makers Tech ChatBot", layout="wide")

# Apply custom CSS for styling
apply_custom_css()

# App layout
st.title("Makers Tech ChatBot")
st.write("Welcome to Makers Tech! Chat with our bot, explore recommendations, and manage inventory.")

# Tabs for different sections
tab1, tab2, tab3 = st.tabs(["ChatBot", "Recommendations", "Admin Dashboard"])

# ChatBot Tab
with tab1:
    show_chatbot()

# Recommendations Tab
with tab2:
    show_recommendations()

# Admin Dashboard Tab
with tab3:
    show_dashboard()

# Footer
st.divider()
st.markdown("<h3>**Makers Tech ChatBot** © 2025 - All rights reserved</h3>", unsafe_allow_html=True)
