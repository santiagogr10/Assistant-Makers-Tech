import streamlit as st
import sqlite3
import requests
import pandas as pd
import matplotlib.pyplot as plt
from database_reader import get_database_content_as_dict

# Page configuration
st.set_page_config(page_title="Makers Tech ChatBot", layout="wide")

# Custom CSS for the red logout button
st.markdown(
    """
    <style>
    .stButton>button[data-baseweb="button"].logout-btn {
        background-color: #ff4b4b;
        color: white;
    }
    .stButton>button[data-baseweb="button"].logout-btn:hover {
        background-color: #ff0000;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_page" not in st.session_state:
    st.session_state.current_page = "main"


# Database class implementation
class Database:
    def __init__(self, db_name: str = "store.db"):
        self.db_name = db_name

    def verify_user(self, user_id: int) -> bool:
        """
        Verifies if the user exists in the database.

        Args:
            user_id (int): The user ID.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
                return cursor.fetchone() is not None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def get_user_data(self, user_id: int) -> dict:
        """
        Retrieves all relevant data for the user.

        Args:
            user_id (int): The user ID.

        Returns:
            dict: A dictionary containing the user's data, or None if not found.
        """
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT user_id, purchase_history, preferences 
                    FROM users 
                    WHERE user_id = ?
                """,
                    (user_id,),
                )
                result = cursor.fetchone()
                if result:
                    return {
                        "user_id": result[0],
                        "purchase_history": result[1],
                        "preferences": result[2],
                    }
                return None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    def get_user_history(self, user_id: int) -> str:
        """
        Retrieves the purchase history for the user.

        Args:
            user_id (int): The user ID.

        Returns:
            str: The user's purchase history as a string, or None if not found.
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT purchase_history 
                FROM users 
                WHERE user_id = ?
            """,
                (user_id,),
            )
            result = cursor.fetchone()
            return result[0] if result else None

    def get_products(self):
        """
        Retrieves all products with their details.

        Returns:
            list: A list of dictionaries containing product information.
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT name, category, brand, price, stock 
                FROM products 
                WHERE stock > 0
            """
            )
            columns = ["name", "category", "brand", "price", "stock"]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_product_categories(self, user_history: str):
        """
        Classifies products based on the user's purchase history.

        Args:
            user_history (str): The user's purchase history.

        Returns:
            dict: A dictionary categorizing products into "Highly Recommended",
                  "Recommended", and "Not Recommended".
        """
        products = self.get_products()
        categories = {"Highly Recommended": [], "Recommended": [], "Not Recommended": []}

        history_items = user_history.split(",") if user_history else []

        for product in products:
            if (
                len(categories["Highly Recommended"]) >= 2
                and len(categories["Recommended"]) >= 2
                and len(categories["Not Recommended"]) >= 2
            ):
                break

            if product["brand"] in history_items or product["category"] in history_items:
                if len(categories["Highly Recommended"]) < 2:
                    categories["Highly Recommended"].append(product["name"])
            elif any(item in history_items for item in [product["brand"], product["category"]]):
                if len(categories["Recommended"]) < 2:
                    categories["Recommended"].append(product["name"])
            else:
                if len(categories["Not Recommended"]) < 2:
                    categories["Not Recommended"].append(product["name"])

        return categories


# Initialize database
db = Database()


def generate_ai_response(user_message: str, user_data: dict):
    """
    Generates a response using the AI client.

    Args:
        user_message (str): The user's query.
        user_data (dict): User data containing history and preferences.

    Returns:
        str: The AI-generated response or an error message if something goes wrong.
    """
    try:
        # Check if user_data is None or empty
        if not user_data:
            return "Sorry, I cannot access the user's data at the moment."

        # Debug print
        print(f"Generating response for user data: {user_data}")

        # Ensure all fields exist, using default values if missing
        context = f"""
        Based on the following user history and preferences:
        - Purchase history: {user_data.get('purchase_history', 'No history')}
        - Purchased brands: {', '.join(user_data.get('bought_brands', ['No brands']))
                           if user_data.get('bought_brands') else 'No brands'}
        - Purchased categories: {', '.join(user_data.get('bought_categories', ['No categories']))
                               if user_data.get('bought_categories') else 'No categories'}
        - Preferences: {user_data.get('preferences', 'No preferences')}

        Please follow these criteria for recommendations:

        1. Highly Recommended:
           - ONLY products from the brands: {', '.join(user_data.get('bought_brands', ['No brands']))
                                         if user_data.get('bought_brands') else 'No brands'}
           - ONLY from the categories: {', '.join(user_data.get('bought_categories', ['No categories']))
                                   if user_data.get('bought_categories') else 'No categories'}
           - Must be complementary to previous purchases
           - Only products in stock

        2. Recommended:
           - Products from categories related to: {', '.join(user_data.get('bought_categories', ['No categories']))
                                                   if user_data.get('bought_categories') else 'No categories'}
           - Useful complements for previously purchased products
           - Can be from other brands
           - Only products in stock

        3. Not Recommended:
           - Products from brands and categories different from those mentioned
           - Non-complementary products

        Respond STRICTLY based on these criteria and the specific history of this user.
        If the user has no history, recommend popular or basic products.
        """

        response = requests.post(
            "http://127.0.0.1:5000/api/chat",
            json={"message": user_message, "user_data": user_data, "context": context},
        )

        if response.status_code == 200:
            return response.json().get("response", "I couldn't process that request.")
        else:
            return (
                f"I'm having trouble processing your request. Status code: {response.status_code}"
            )
    except Exception as e:
        print(f"Error in generate_ai_response: {str(e)}")  # Debug print
        return f"An unexpected error occurred: {str(e)}"


# Sidebar para navegación
with st.sidebar:
    if st.session_state.logged_in:
        if st.button("Dashboard", key="dashboard_btn"):
            st.session_state.current_page = "dashboard"
        if st.button("Main Chat", key="main_chat_btn"):
            st.session_state.current_page = "main"
        if st.button("Log Out", key="logout_btn", type="primary", help="Click to log out"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.chat_history = []
            st.session_state.current_page = "main"
            st.rerun()

# Main layout
st.title("Makers Tech ChatBot")

if not st.session_state.logged_in:
    st.write("Welcome to Makers Tech! Please log in to chat with our AI.")
    user_id = st.text_input(
        "", placeholder="Enter your User ID", key="login_input", label_visibility="collapsed"
    )

    if st.button("Log In"):
        if user_id:
            try:
                user_id = int(user_id)
                if db.verify_user(user_id):
                    user_data = db.get_user_data(user_id)
                    if user_data:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user_id
                        st.session_state.user_data = user_data
                        st.rerun()
                    else:
                        st.error("Could not retrieve user data.")
                else:
                    st.error("User not found. Please check your User ID.")
            except ValueError:
                st.error("Please enter a valid numeric ID.")
        else:
            st.warning("Please enter a User ID to log in.")

elif st.session_state.current_page == "main":
    st.markdown('<div class="main-content">', unsafe_allow_html=True)

    # Chat section
    st.subheader("Chat with our ChatBot")

    # Fixed chat input at top
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([4, 1])
    with col1:
        user_message = st.text_input(
            "",
            placeholder="Enter your question here...",
            key="chat_input",
            label_visibility="collapsed",
        )
    with col2:
        if st.button("Send", key="send_button"):
            if user_message:
                print(f"Current session state: {st.session_state}")  # Debug print
                print(f"User data in session: {st.session_state.user_data}")  # Debug print

                st.session_state.messages = []
                st.session_state.messages.append({"text": user_message, "is_bot": False})

                with st.spinner("Getting response..."):
                    bot_response = generate_ai_response(
                        user_message=user_message, user_data=st.session_state.user_data
                    )

                st.session_state.messages.append({"text": bot_response, "is_bot": True})
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Display chat messages below
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show only last exchange
    if len(st.session_state.messages) > 0:
        last_user_msg = (
            st.session_state.messages[-2] if len(st.session_state.messages) >= 2 else None
        )
        last_bot_msg = (
            st.session_state.messages[-1] if len(st.session_state.messages) >= 1 else None
        )

        if last_user_msg:
            st.markdown(
                f"<div class='user-message'>👤 You: {last_user_msg['text']}</div>",
                unsafe_allow_html=True,
            )
        if last_bot_msg:
            st.markdown(
                f"<div class='bot-message'>🤖 Bot: {last_bot_msg['text']}</div>",
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.current_page == "dashboard":
    st.title("Admin Dashboard")

    # Métricas principales en la parte superior
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Products", "75", "↑ 4")
    with col2:
        st.metric("Low Stock Items", "12", "↓ 2")
    with col3:
        st.metric("Out of Stock", "3", "↑ 1")
    with col4:
        st.metric("Total Categories", "8", "")

    # Primera fila de gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Stock Levels by Category")
        # Datos de ejemplo para el gráfico de barras
        stock_data = {
            "Category": ["Laptops", "Smartphones", "Tablets", "Accessories"],
            "Stock": [45, 30, 25, 60],
        }
        df_stock = pd.DataFrame(stock_data)

        fig1, ax1 = plt.subplots(figsize=(10, 6))
        df_stock.plot(kind="bar", x="Category", y="Stock", ax=ax1, color="#4c9aff")
        ax1.set_facecolor("#1f1f2e")
        fig1.patch.set_facecolor("#1f1f2e")
        ax1.spines["bottom"].set_color("white")
        ax1.spines["left"].set_color("white")
        ax1.tick_params(colors="white")
        ax1.set_ylabel("Quantity", color="white")
        plt.xticks(rotation=45)
        st.pyplot(fig1)

    with col2:
        st.subheader("Sales Distribution by Brand")
        # Datos de ejemplo para el gráfico circular
        sales_data = {
            "Brand": ["Apple", "Dell", "HP", "Lenovo", "Others"],
            "Sales": [35, 25, 20, 15, 5],
        }
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.pie(
            sales_data["Sales"],
            labels=sales_data["Brand"],
            autopct="%1.1f%%",
            colors=["#4c9aff", "#ff6b6b", "#ffd93d", "#6c5ce7", "#a8e6cf"],
        )
        ax2.set_facecolor("#1f1f2e")
        fig2.patch.set_facecolor("#1f1f2e")
        st.pyplot(fig2)

    # Segunda fila
    st.subheader("Inventory Details")
    inventory_data = get_database_content_as_dict()
    df_inventory = pd.DataFrame(inventory_data)

    # Estilo para la tabla
    st.dataframe(
        df_inventory,
        column_config={
            "Product": "Product Name",
            "Category": "Category",
            "Brand": "Brand",
            "Stock": st.column_config.NumberColumn(
                "Current Stock", help="Current stock level", format="%d units"
            ),
            "Price": "Price",
        },
        hide_index=True,
        use_container_width=True,
    )

    # Alertas de stock bajo
    st.subheader("Low Stock Alerts")
    low_stock_items = df_inventory[df_inventory["Stock"] < 10]
    if not low_stock_items.empty:
        for _, item in low_stock_items.iterrows():
            st.warning(
                f"⚠️ Low stock alert: {item['Product']} - Only {item['Stock']} units remaining"
            )

# Footer
st.divider()
st.markdown("**Makers Tech ChatBot** © 2025 - All rights reserved")
# Actualizar el CSS
st.markdown(
    """
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
""",
    unsafe_allow_html=True,
)
