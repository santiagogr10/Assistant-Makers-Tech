import sqlite3
from typing import List, Dict, Optional


class Database:
    def __init__(self, db_name: str = "store.db"):
        self.db_name = db_name

    def get_user_history(self, user_id: int) -> Optional[str]:
        """
        Retrieves the purchase history of a user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            Optional[str]: The user's purchase history as a string, or None if not found.
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

    def get_products(self) -> List[Dict]:
        """
        Retrieves all products with their information.

        Returns:
            List[Dict]: A list of dictionaries containing product details.
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

    def get_product_categories(self, user_history: str) -> Dict[str, List[str]]:
        """
        Classifies products based on the user's purchase history.

        Args:
            user_history (str): A comma-separated string of the user's purchase history.

        Returns:
            Dict[str, List[str]]: A dictionary with categorized product names.
        """
        products = self.get_products()
        categories = {"Highly Recommended": [], "Recommended": [], "Not Recommended": []}

        # Convert history into a list of brands and categories
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

    def initialize_database(self):
        """
        Initializes the database with the required tables.
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            # Create users table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    purchase_history TEXT
                )
            """
            )

            # Create products table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS products (
                    product_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    brand TEXT NOT NULL,
                    price REAL NOT NULL,
                    stock INTEGER NOT NULL,
                    sales INTEGER DEFAULT 0
                )
            """
            )

            conn.commit()
