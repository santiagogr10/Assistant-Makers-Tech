import streamlit as st
import sqlite3
import requests

# Page configuration
st.set_page_config(page_title="Makers Tech ChatBot", layout="wide")

# Custom CSS for the red logout button
st.markdown("""
    <style>
    .stButton>button[data-baseweb="button"].logout-btn {
        background-color: #ff4b4b;
        color: white;
    }
    .stButton>button[data-baseweb="button"].logout-btn:hover {
        background-color: #ff0000;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'main'

# Database class implementation
class Database:
    def __init__(self, db_name: str = "store.db"):
        self.db_name = db_name

    def get_user_history(self, user_id: int) -> str:
        """Obtiene el historial de compras del usuario"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT purchase_history 
                FROM users 
                WHERE user_id = ?
            """, (user_id,))
            result = cursor.fetchone()
            return result[0] if result else None

    def get_products(self):
        """Obtiene todos los productos con su información"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name, category, brand, price, stock 
                FROM products 
                WHERE stock > 0
            """)
            columns = ['name', 'category', 'brand', 'price', 'stock']
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_product_categories(self, user_history: str):
        """Clasifica los productos basado en el historial del usuario"""
        products = self.get_products()
        categories = {
            "Highly Recommended": [],
            "Recommended": [],
            "Not Recommended": []
        }
        
        history_items = user_history.split(',') if user_history else []
        
        for product in products:
            if len(categories["Highly Recommended"]) >= 2 and \
               len(categories["Recommended"]) >= 2 and \
               len(categories["Not Recommended"]) >= 2:
                break
                
            if product['brand'] in history_items or product['category'] in history_items:
                if len(categories["Highly Recommended"]) < 2:
                    categories["Highly Recommended"].append(product['name'])
            elif any(item in history_items for item in [product['brand'], product['category']]):
                if len(categories["Recommended"]) < 2:
                    categories["Recommended"].append(product['name'])
            else:
                if len(categories["Not Recommended"]) < 2:
                    categories["Not Recommended"].append(product['name'])
        
        return categories

# Initialize database
db = Database()

def generate_ai_response(user_message: str, user_history: str, products: list):
    """
    Genera una respuesta usando el cliente de IA
    """
    try:
        # Conectar con el endpoint de la IA
        response = requests.post(
            "http://127.0.0.1:5000/api/chat",  # URL del endpoint de la IA
            json={
                "message": user_message
            }
        )
        
        if response.status_code == 200:
            return response.json().get("response", "I couldn't process that request.")
        else:
            return f"I'm having trouble processing your request. Status code: {response.status_code}"
            
    except requests.exceptions.ConnectionError:
        return "I'm currently unable to connect to my knowledge base. Please try again in a moment."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

# Sidebar para navegación
with st.sidebar:
    if st.session_state.logged_in:
        if st.button("Dashboard", key="dashboard_btn"):
            st.session_state.current_page = 'dashboard'
        if st.button("Main Chat", key="main_chat_btn"):
            st.session_state.current_page = 'main'
        if st.button("Log Out", key="logout_btn", type="primary", help="Click to log out"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.chat_history = []
            st.session_state.current_page = 'main'
            st.rerun()

# Main layout
st.title("Makers Tech ChatBot")

if not st.session_state.logged_in:
    st.write("Welcome to Makers Tech! Please log in to see your personalized recommendations.")
    user_id = st.text_input("", placeholder="Enter your User ID", key="login_input", label_visibility="collapsed")

    if st.button("Log In"):
        if user_id:
            user_history = db.get_user_history(int(user_id))
            if user_history:
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.rerun()
            else:
                st.warning("User not found. Please check your User ID.")
        else:
            st.warning("Please enter a User ID to log in.")

elif st.session_state.current_page == 'main':
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Chat section
    st.subheader("Chat with our ChatBot")
    
    # Fixed chat input at top
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([4, 1])
    with col1:
        user_message = st.text_input("", placeholder="Enter your question here...", key="chat_input", label_visibility="collapsed")
    with col2:
        if st.button("Send", key="send_button"):
            if user_message:
                # Clear previous messages
                st.session_state.messages = []
                st.session_state.messages.append({"text": user_message, "is_bot": False})
                
                # Obtener el historial del usuario
                user_history = db.get_user_history(int(st.session_state.user_id))
                
                with st.spinner("Getting response..."):
                    bot_response = generate_ai_response(
                        user_message=user_message,
                        user_history=user_history,
                        products=db.get_products()
                    )
                
                st.session_state.messages.append({"text": bot_response, "is_bot": True})
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display chat messages below
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Show only last exchange
    if len(st.session_state.messages) > 0:
        last_user_msg = st.session_state.messages[-2] if len(st.session_state.messages) >= 2 else None
        last_bot_msg = st.session_state.messages[-1] if len(st.session_state.messages) >= 1 else None
        
        if last_user_msg:
            st.markdown(f"<div class='user-message'>👤 You: {last_user_msg['text']}</div>", unsafe_allow_html=True)
        if last_bot_msg:
            st.markdown(f"<div class='bot-message'>🤖 Bot: {last_bot_msg['text']}</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == 'dashboard':
    st.title("Admin Dashboard")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Sales", "$10,000")
    with col2:
        st.metric("Active Users", "150")
    with col3:
        st.metric("Products in Stock", "75")
    
    st.subheader("Recent Activities")
    st.write("Recent sales and user activities would appear here")
    
    st.subheader("Inventory Status")
    st.write("Inventory levels and alerts would appear here")

# Footer
st.divider()
st.markdown("**Makers Tech ChatBot** © 2025 - All rights reserved")
# Actualizar el CSS
st.markdown("""
    <style>
    /* Chat input container at top */
    .chat-input-container {
        background-color: #1f1f2e;
        padding: 10px;
        border-bottom: 1px solid #333;
        margin-bottom: 20px;
    }

    /* Chat messages below */
    .chat-messages {
        padding: 10px;
        margin-top: 20px;
    }

    .user-message {
        background-color: #2d2d3d;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }

    .bot-message {
        background-color: #3d3d4d;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }

    .main-content {
        padding: 20px;
    }
    </style>
""", unsafe_allow_html=True)

