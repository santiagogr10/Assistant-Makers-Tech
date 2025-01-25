import sqlite3


def view_database(db_name="store.db"):
    """
    Muestra la estructura y los datos de la base de datos.

    Args:
        db_name (str): Nombre del archivo de la base de datos.
    """
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Mostrar las tablas existentes
        print("\nTablas existentes en la base de datos:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            print(f"- {table[0]}")

        # Mostrar los datos de cada tabla
        for table in tables:
            table_name = table[0]
            print(f"\nDatos en la tabla '{table_name}':")
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()

            # Obtener los nombres de las columnas
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = [col[1] for col in cursor.fetchall()]
            print(f"Columnas: {columns}")

            # Mostrar los datos
            if rows:
                for row in rows:
                    print(row)
            else:
                print("(Tabla vacía)")

        # Cerrar la conexión
        conn.close()

    except Exception as e:
        print(f"Error al visualizar la base de datos: {e}")


if __name__ == "__main__":
    view_database()
