# Librerías utilizadas:
# - pandas (pd): para leer y escribir archivos CSV de manera eficiente.
# - mysql.connector: para conectarse a bases de datos MySQL y ejecutar sentencias SQL.
# - mysql.connector.Error: para manejar errores específicos en la conexión o ejecución de consultas.

import pandas as pd
import mysql.connector
from mysql.connector import Error

def load_to_csv(df, filename="data/processed/books.csv"):
    """
    Guarda un DataFrame en un archivo CSV.

    Parámetros:
    -----------
    df : pandas.DataFrame
        DataFrame que contiene los datos a almacenar.
    filename : str, opcional
        Ruta donde se guardará el archivo CSV. Por defecto, "data/processed/books.csv".

    Proceso:
    --------
    - Utiliza pandas.DataFrame.to_csv() para exportar los datos.
    - Se omite el índice del DataFrame (index=False).
    - Se utiliza codificación UTF-8 para evitar problemas con caracteres especiales.
    """
    df.to_csv(filename, index=False, encoding="utf-8")

def load_csv_to_mysql(
    filename="data/processed/books.csv",
    host='localhost',
    database='books_db',
    user='root',
    password='0468'
):
    """
    Carga los datos de un archivo CSV a una base de datos MySQL.
    Si la tabla no existe, la crea automáticamente.

    Parámetros:
    -----------
    filename : str, opcional
        Ruta del archivo CSV que contiene los datos procesados.
    host : str, opcional
        Dirección del servidor MySQL. Por defecto 'localhost'.
    database : str, opcional
        Nombre de la base de datos destino. Por defecto 'books_db'.
    user : str, opcional
        Usuario de conexión a la base de datos. Por defecto 'root'.
    password : str, opcional
        Contraseña del usuario de la base de datos. Por defecto '0468'.

    Proceso:
    --------
    1. Lee el CSV usando pandas.
    2. Establece conexión con MySQL mediante mysql.connector.connect().
    3. Crea la tabla 'books' si no existe, con las columnas:
        - title (texto único)
        - price (float)
        - availability (int)
        - rating (int)
        - category (texto)
        - image_path (texto)
    4. Inserta los registros del CSV en la tabla:
        - Usa INSERT IGNORE para evitar errores en registros duplicados.
        - Usa ON DUPLICATE KEY UPDATE para actualizar datos ya existentes.
    5. Confirma los cambios (commit) y cierra la conexión.

    Manejo de errores:
    ------------------
    - Captura excepciones de tipo mysql.connector.Error.
    - Imprime un mensaje descriptivo en caso de error.
    """

    # 1. Leer archivo CSV en un DataFrame
    df = pd.read_csv(filename)

    try:
        # 2. Conectar a la base de datos MySQL
        conn = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        cursor = conn.cursor()

        # 3. Crear tabla si no existe
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

        # 4. Insertar registros fila por fila
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

        # 5. Confirmar cambios y cerrar conexión
        conn.commit()
        cursor.close()
        conn.close()
        print("Datos cargados a la base de datos correctamente.")

    except Error as e:
        print(f"Error al cargar datos a MySQL: {e}")