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

# Recommendations Section
def show_recommendations():
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
