import sqlite3
from typing import List, Dict, Optional

class Database:
    def __init__(self, db_name: str = "store.db"):
        self.db_name = db_name

    def get_user_history(self, user_id: int) -> Optional[str]:
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

    def get_products(self) -> List[Dict]:
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

    def get_product_categories(self, user_history: str) -> Dict[str, List[str]]:
        """Clasifica los productos basado en el historial del usuario"""
        products = self.get_products()
        categories = {
            "Highly Recommended": [],
            "Recommended": [],
            "Not Recommended": []
        }
        
        # Convertir historial en lista de marcas y categorías
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

    def initialize_database(self):
        """Inicializa la base de datos con las tablas necesarias"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            # Crear tabla de usuarios
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    purchase_history TEXT
                )
            """)
            
            # Crear tabla de productos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    product_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    brand TEXT NOT NULL,
                    price REAL NOT NULL,
                    stock INTEGER NOT NULL,
                    sales INTEGER DEFAULT 0
                )
            """)
            
            conn.commit() 