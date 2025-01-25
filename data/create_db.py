import sqlite3


def create_database(db_name="store.db"):
    """
    Crea la base de datos con las tablas 'products' y 'users'.
    Si las tablas ya existen, no las recrea.

    Args:
        db_name (str): Nombre del archivo de la base de datos.
    """
    # Conectar o crear la base de datos
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Crear la tabla 'products'
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        brand TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL,
        description TEXT,
        features TEXT
    );
    """)

    # Crear la tabla 'users'
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        preferences TEXT,
        purchase_history TEXT
    );
    """)

    print("Base de datos y tablas creadas exitosamente.")

    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
