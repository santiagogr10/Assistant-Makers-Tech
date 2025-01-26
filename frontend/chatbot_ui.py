import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# Custom CSS for styling
def apply_custom_css():
    st.markdown("""
        <style>
        .main { background-color: #1f1f2e; color: white; }
        input, button { border-radius: 5px; padding: 10px; }
        button { background-color: #4c9aff; color: white; border: none; cursor: pointer; }
        button:hover { background-color: #3a8ce3; }
        </style>
    """, unsafe_allow_html=True)

# ChatBot Section
def show_chatbot():
    st.subheader("Chat with our ChatBot")
    
    # Initialize session state for conversation history
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    
    if "recommendations" not in st.session_state:
        st.session_state["recommendations"] = {
            "Highly Recommended": [],
            "Recommended": [],
            "Not Recommended": []
        }
    
    # Display chat history
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    # Input and Send Button in the same row
    col1, col2 = st.columns([4, 1])  # Adjust column widths if needed

    with col1:
        user_input = st.text_input("Enter your question:", placeholder="E.g., How many laptops are available?")

    with col2:
        send_clicked = st.button("Send")

    # Handle user input
    if send_clicked and user_input.strip():
        # Save user message to session state
        st.session_state["messages"].append({"role": "user", "content": user_input})
        try:
            # Send the query to the backend
            with st.spinner("Fetching response from the chatbot..."):
                response = requests.post(
                    "http://127.0.0.1:5000/api/chat",  # Backend URL
                    json={"user_id": 1, "message": user_input}
                )
            if response.status_code == 200:
                chatbot_response = response.json().get("response", "No response received.")
                st.session_state["messages"].append({"role": "assistant", "content": chatbot_response})

                # Update recommendations dynamically
                st.session_state["recommendations"] = {
                    "Highly Recommended": ["MacBook Air"],  # Replace with dynamic logic
                    "Recommended": ["Dell Inspiron 15", "HP Pavilion 14"],
                    "Not Recommended": []
                }
            else:
                chatbot_response = "Error: Unable to fetch a valid response from the server."
                st.session_state["messages"].append({"role": "assistant", "content": chatbot_response})
        except Exception as e:
            st.error(f"Error connecting to the backend: {e}")
    elif send_clicked:
        st.warning("Please enter a question before clicking 'Send'.")

# Recommendations Section
def show_recommendations():
    st.subheader("Recommended Products")
    
    # Get recommendations from session state
    recommendations = st.session_state.get("recommendations", {
        "Highly Recommended": [],
        "Recommended": [],
        "Not Recommended": []
    })
    
    # Display recommendations dynamically
    for category, products in recommendations.items():
        st.write(f"**{category}:**")
        for product in products:
            st.write(f"- {product}")

# Admin Dashboard Section
def show_dashboard():
    st.subheader("Admin Dashboard")
    
    # Example inventory data
    data = {
        "Product": ["Laptop", "Tablet", "Smartphone"],
        "Stock": [20, 15, 30],
        "Price": [1000, 500, 800]
    }
    df = pd.DataFrame(data)
    
    # Display inventory data
    st.write("### Current Inventory")
    st.table(df)
    
    # Plot stock levels
    st.write("### Stock Levels")
    fig = px.bar(df, x="Product", y="Stock", title="Stock Levels", color="Product", text="Stock")
    st.plotly_chart(fig)

# Page configuration
st.set_page_config(page_title="Makers Tech ChatBot", layout="wide")

# Apply custom CSS for styling
apply_custom_css()

# App layout
st.title("Makers Tech ChatBot")
st.write("Welcome to Makers Tech! Explore inventory, chat with our bot, and view product recommendations.")

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
st.write("**Makers Tech ChatBot** © 2025 - All rights reserved")
