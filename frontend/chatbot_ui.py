import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd


# Custom CSS for styling
def apply_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

        /* General background and text styling */
        html, body, [class*="css"] {
            font-family: 'Roboto', sans-serif;
            background-color: #1f1f2e;
            color: white;
            overflow-x: hidden;
        }

        /* Centered titles and subtitles */
        h1, h2, h3 {
            text-align: center;
            color: #4c9aff;
        }

        /* Persistent chat input bar (fixed at the bottom) */
        .chat-container {
            position: fixed;
            bottom: 0; /* Stick to the bottom of the screen */
            width: 100%;
            background-color: #1f1f2e;
            z-index: 1000; /* Keep it above other content */
            padding: 10px;
            box-shadow: 0px -2px 10px rgba(0, 0, 0, 0.2);
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .chat-input {
            flex: 1;
            padding: 12px;
            font-size: 16px;
            border-radius: 5px 0 0 5px;
            border: 1px solid #ccc;
            background-color: #2b2b3b;
            color: white;
        }

        .chat-button {
            padding: 12px 20px;
            font-size: 16px;
            background-color: #4c9aff;
            color: white;
            border: none;
            border-radius: 0 5px 5px 0;
            cursor: pointer;
        }

        .chat-button:hover {
            background-color: #3a8ce3;
        }

        /* Chat history container */
        .chat-history {
            padding: 10px;
            max-height: calc(100vh - 140px); /* Adjust height to avoid overlap */
            overflow-y: auto;
            margin-bottom: 80px; /* Leave space for the fixed input bar */
        }

        .user-message {
            font-size: 18px;
            color: #4c9aff;
            margin-bottom: 5px;
            text-align: left;
        }

        .bot-message {
            font-size: 18px;
            color: #d1d1d1;
            margin-bottom: 10px;
            text-align: left;
        }
        </style>
    """, unsafe_allow_html=True)

# ChatBot Section
def show_chatbot():
    st.subheader("Chat with our ChatBot")

    # Initialize session state for conversation history
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # User input and send button in a horizontal bar
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input("", placeholder="Enter your question here...", key="chat_input", label_visibility="collapsed")
    with col2:
        if st.button("Send", key="send_button"):
            if user_input.strip():
                # Clear previous messages
                st.session_state["messages"] = [{"role": "user", "content": user_input}]
                try:
                    with st.spinner("Fetching response..."):
                        # Send the query to the backend
                        response = requests.post(
                            "http://127.0.0.1:5000/api/chat",  # Adjust with actual backend URL
                            json={"message": user_input}
                        )
                        if response.status_code == 200:
                            chatbot_response = response.json().get("response", "No response received.")
                            st.session_state["messages"].append({"role": "assistant", "content": chatbot_response})
                        else:
                            st.session_state["messages"].append({"role": "assistant", "content": "Error fetching response."})
                except Exception as e:
                    st.error(f"Error connecting to backend: {e}")
            else:
                st.warning("Please enter a question before clicking 'Send'.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Display chat history
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**Bot:** {msg['content']}")

def show_recommendations(recommendations):
    """
    Muestra las recomendaciones en formato de columnas comparativas
    Args:
        recommendations (dict): Diccionario con las categorías de productos recomendados
    """
    st.subheader("Recommended Products")
    
    # Display recommendations in columns for comparison
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<h4 style='text-align: center; font-size: 14px;'>Highly Recommended</h4>", unsafe_allow_html=True)
        for product in recommendations["Highly Recommended"]:
            st.markdown(f"<p style='text-align: center; font-size: 12px;'>- {product}</p>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h4 style='text-align: center; font-size: 14px;'>Recommended</h4>", unsafe_allow_html=True)
        for product in recommendations["Recommended"]:
            st.markdown(f"<p style='text-align: center; font-size: 12px;'>- {product}</p>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<h4 style='text-align: center; font-size: 14px;'>Not Recommended</h4>", unsafe_allow_html=True)
        for product in recommendations["Not Recommended"]:
            st.markdown(f"<p style='text-align: center; font-size: 12px;'>- {product}</p>", unsafe_allow_html=True)


# Admin Dashboard Section
import matplotlib.pyplot as plt

def show_dashboard():
    st.subheader("Admin Dashboard")

    # Example inventory data
    data = {
        "Product": ["Laptop", "Tablet", "Smartphone"],
        "Stock": [20, 15, 30],
        "Price": [1000, 500, 800]
    }

    try:
        # Create a DataFrame
        df = pd.DataFrame(data)

        # Display inventory data
        st.write("### Current Inventory")
        st.table(df)

        # Plot stock levels using Matplotlib
        st.write("### Stock Levels")
        fig, ax = plt.subplots(figsize=(10, 6))  # Adjust figure size
        df.plot(
            kind="bar", 
            x="Product", 
            y="Stock", 
            legend=False, 
            ax=ax, 
            color="#4c9aff"  # Match color scheme
        )
        ax.set_facecolor("#1f1f2e")  # Match the background of the webpage
        fig.patch.set_facecolor("#1f1f2e")  # Match the figure background
        ax.spines["bottom"].set_color("white")  # Set axis colors
        ax.spines["left"].set_color("white")
        ax.tick_params(colors="white")  # Set tick colors
        ax.yaxis.label.set_color("white")  # Set axis label color
        ax.xaxis.label.set_color("white")
        ax.title.set_color("white")  # Set title color
        ax.set_ylabel("Stock Quantity")
        ax.set_title("Stock Levels by Product")
        ax.grid(axis='y', color="#3a3a4a", linestyle="--")  # Subtle gridlines
        st.pyplot(fig)

    except Exception as e:
        st.error(f"An error occurred while loading the dashboard: {e}")

