# Librerías utilizadas:
# - pandas (pd): para crear y manipular estructuras de datos tipo DataFrame
# - re: para usar expresiones regulares en la limpieza de texto

import pandas as pd
import re

def transform_books(books):
    """
    Transforma y limpia los datos de libros extraídos, convirtiéndolos
    en un DataFrame de pandas listo para análisis o almacenamiento.

    Parámetros:
    -----------
    books : list[dict]
        Lista de diccionarios con información de libros. Cada diccionario
        debe contener las claves:
        - 'title'
        - 'price'
        - 'rating'
        - 'availability'
        - 'category'
        - 'image_path'

    Proceso:
    --------
    1. Convierte la lista de diccionarios en un DataFrame.
    2. Limpia y transforma la columna 'price':
       - Elimina el símbolo '£'.
       - Convierte los valores a tipo float.
    3. Convierte la columna 'rating' de texto a valores numéricos (1 a 5).
    4. Extrae el número de libros disponibles de la columna 'availability':
       - Usa una expresión regular para encontrar números en el texto.
       - Convierte valores nulos en 0 y los transforma a tipo entero.
    5. Elimina registros duplicados basándose en el título del libro.

    Retorna:
    --------
    df : pandas.DataFrame
        DataFrame limpio y transformado, listo para análisis o exportación.
    """

    # 1. Convertir la lista de diccionarios a un DataFrame de pandas
    df = pd.DataFrame(books)

    # 2. Limpiar y transformar los precios
    # - Se elimina el símbolo '£' usando regex
    # - Se convierten los valores resultantes a float
    df['price'] = df['price'].replace('£', '', regex=True).astype(float)

    # 3. Convertir las calificaciones textuales a valores numéricos
    df['rating'] = df['rating'].map({
        'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5
    })

    # 4. Extraer número de disponibilidad con regex y convertir a entero
    df['availability'] = (
        df['availability']
        .str.extract(r'(\d+)')       # Extrae dígitos de la cadena
        .astype(float)               # Convierte a float para manejar valores nulos
        .fillna(0)                   # Sustituye valores nulos por 0
        .astype(int)                 # Convierte a entero final
    )

    # 5. Eliminar duplicados por título
    df.drop_duplicates(subset=['title'], inplace=True)

    # Retornar DataFrame limpio
    return df