# Librerías utilizadas:
# - urllib.parse: para unir URLs de manera segura (urljoin)
# - selenium: para automatizar la navegación en el navegador y obtener contenido dinámico
# - webdriver_manager: para gestionar automáticamente la instalación del driver de Chrome
# - bs4 (BeautifulSoup): para analizar (parsear) el contenido HTML y extraer información
# - time: para introducir pausas y esperar la carga de la página
# - os: para manejar rutas y crear carpetas (comentado en este caso)
# - requests: para realizar peticiones HTTP y obtener contenido adicional de las páginas
# - re: para limpiar nombres de archivos utilizando expresiones regulares (comentado en este caso)

from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import os
import requests
import re

def extract_books(url, min_books):
    """
    Función para extraer información de libros desde un sitio web.

    Parámetros:
    -----------
    url : str
        URL inicial del catálogo de libros.
    min_books : int
        Número mínimo de libros a extraer antes de detener el proceso.

    Retorna:
    --------
    books : list[dict]
        Lista de diccionarios, cada uno con la información de un libro.
    """

    # --- Configuración del navegador (Selenium) ---
    # Se usa Chrome en modo "headless" (sin abrir ventana)
    options = Options()
    options.add_argument("--headless")

    # Inicia el navegador usando webdriver_manager para manejar la instalación del driver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        options=options
    )

    # Cargar la URL inicial
    driver.get(url)
    time.sleep(3)  # Espera para asegurar que la página se haya cargado completamente

    books = []        # Lista donde se almacenará la información de los libros
    page_url = url    # URL actual (se actualizará para la paginación)

    # --- Bucle para recorrer páginas y extraer libros hasta alcanzar el mínimo requerido ---
    while len(books) < min_books:
        # Abrir la página actual y esperar su carga
        driver.get(page_url)
        time.sleep(3)

        # --- Parseo del HTML con BeautifulSoup ---
        # driver.page_source obtiene el código HTML ya renderizado por Selenium
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # --- Extracción de datos de cada libro ---
        for article in soup.select(".product_pod"):
            # Título del libro
            title = article.h3.a['title']
            # Precio
            price = article.select_one(".price_color").text
            # Calificación (por ejemplo: Three, Four, Five stars)
            rating = article.p['class'][1]
            # URL de la imagen (reemplazando la ruta relativa por absoluta)
            img_url = article.img['src'].replace('../../', 'https://books.toscrape.com/')
            # URL de la página individual del libro
            book_href = urljoin(page_url, article.h3.a['href'])
            
            # --- Obtención de información adicional desde la página individual del libro ---
            book_resp = requests.get(book_href)
            book_soup = BeautifulSoup(book_resp.content, 'html.parser')

            # Categoría (extraída del breadcrumb)
            category = book_soup.select('ul.breadcrumb li')[2].text.strip()

            # Disponibilidad (texto dentro del elemento .availability)
            availability_text = book_soup.select_one('.availability').text.strip()

            # --- Manejo de imágenes (comentado) ---
            # Aquí se podría descargar la imagen y guardarla en un directorio
            # safe_title = re.sub(r'[\\/*?:"<>|,]', "_", title)
            # img_name = safe_title.replace(" ", "_") + ".jpg"
            img_path = None  # Se deja como None para mantener la clave en el diccionario
            
            # --- Agregar la información del libro a la lista ---
            books.append({
                "title": title,
                "price": price,
                "availability": availability_text,
                "rating": rating,
                "category": category,
                "image_path": img_path
            })

            # Romper el bucle si ya se alcanzó el mínimo requerido
            if len(books) >= min_books:
                break

        # --- Navegación a la siguiente página ---
        next_btn = soup.select_one("li.next > a")
        if next_btn:
            # Obtener URL absoluta de la siguiente página
            next_href = next_btn['href']
            base_url = page_url.rsplit('/', 1)[0]
            page_url = f"{base_url}/{next_href}"
        else:
            # No hay más páginas para recorrer
            break

    # Cerrar el navegador para liberar recursos
    driver.quit()

    # Retornar la lista de libros
    return books