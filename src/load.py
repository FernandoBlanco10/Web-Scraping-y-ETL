import pandas as pd
import mysql.connector
from mysql.connector import Error

def load_to_csv(df, filename="data/processed/books.csv"):
    """Guarda el DataFrame como CSV."""
    df.to_csv(filename, index=False, encoding="utf-8")

def load_csv_to_mysql(
    filename="data/processed/books.csv",
    host='localhost',
    database='books_db',
    user='root',
    password='0468'
):
    """Carga los datos del CSV a la base de datos MySQL y crea la tabla si no existe."""
    df = pd.read_csv(filename)
    try:
        conn = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        cursor = conn.cursor()
        # Crear la tabla si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                title VARCHAR(255) UNIQUE,
                price FLOAT,
                availability INT,
                rating INT,
                category VARCHAR(255),
                image_path VARCHAR(255)
            )
        """)
        # Insertar los datos
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT IGNORE INTO books (title, price, availability, rating, category, image_path)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    price=VALUES(price),
                    availability=VALUES(availability),
                    rating=VALUES(rating),
                    category=VALUES(category),
                    image_path=VALUES(image_path)
            """, (
                row['title'],
                row['price'],
                row['availability'],
                row['rating'],
                row['category'],
                row['image_path']
            ))
        conn.commit()
        cursor.close()
        conn.close()
        print("Datos cargados a la base de datos correctamente.")
    except Error as e:
        print(f"Error al cargar datos a MySQL: {e}")