import streamlit as st
import requests
import pandas as pd

# Page configuration
st.set_page_config(page_title="Makers Tech ChatBot", layout="wide")

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# App title and description
st.title("Makers Tech ChatBot")
st.write("Welcome to Makers Tech! Here, you can consult our inventory, get product details, and find recommendations tailored to you.")

# Divider
st.divider()

# Chatbot interaction section
st.subheader("Chat with our ChatBot")

# User input
user_input = st.text_input("Enter your question:", placeholder="E.g., How many laptops are available?")

# Display chat history
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# Handle user input
if st.button("Send"):
    if user_input.strip():
        # Save user message to session state
        st.session_state["messages"].append({"role": "user", "content": user_input})

        try:
            # Send the query to the backend
            with st.spinner("Fetching response from the chatbot..."):
                response = requests.post(
                    "http://127.0.0.1:8000/chatbot",  # Replace with your backend URL
                    json={"query": user_input}
                )
            if response.status_code == 200:
                chatbot_response = response.json().get("response", "No response received.")
                st.session_state["messages"].append({"role": "assistant", "content": chatbot_response})
            else:
                chatbot_response = "Error: Unable to fetch a valid response from the server."
                st.session_state["messages"].append({"role": "assistant", "content": chatbot_response})
        except Exception as e:
            st.error(f"Error connecting to the backend: {e}")
    else:
        st.warning("Please enter a question before clicking 'Send'.")

# Divider
st.divider()

# Recommendations Section
st.subheader("Recommended Products")

# Example recommendations (static)
recommendations = {
    "Highly Recommended": ["Laptop A", "Smartphone X"],
    "Recommended": ["Tablet Z", "Monitor B"],
    "Not Recommended": ["Printer C"]
}

# Display recommendations
for category, products in recommendations.items():
    st.write(f"**{category}:**")
    for product in products:
        st.write(f"- {product}")

# Divider
st.divider()

# Admin Dashboard Section
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
st.bar_chart(df.set_index("Product")["Stock"])

# Divider
st.divider()

# Footer
st.write("**Makers Tech ChatBot** © 2025 - All rights reserved")
