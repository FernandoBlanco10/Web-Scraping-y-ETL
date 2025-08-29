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
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(3) # Espera que cargue la pagina
    
    books = []
    page_url = url

    while len(books) < min_books:
        
        driver.get(page_url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        for article in soup.select(".product_pod"):
            title = article.h3.a['title']
            price = article.select_one(".price_color").text
            rating = article.p['class'][1]
            img_url = article.img['src'].replace('../../', 'https://books.toscrape.com/')
            book_href = urljoin(page_url, article.h3.a['href'])
            
            # Accede a la página individual del libro
            book_resp = requests.get(book_href)
            book_soup = BeautifulSoup(book_resp.content, 'html.parser')
            
            # Extrae la categoría desde el breadcrumb
            category = book_soup.select('ul.breadcrumb li')[2].text.strip()
            
            # Extrae la disponibilidad y el número de disponibles
            availability_text = book_soup.select_one('.availability').text.strip()
            
            # img_data = requests.get(img_url).content
            # safe_title = re.sub(r'[\\/*?:"<>|,]', "_", title)
            # img_name = safe_title.replace(" ", "_") + ".jpg"
            img_path = None # Si quieres mantener la clave en el diccionario
            # os.makedirs("images", exist_ok=True)
            # with open(img_path, 'wb') as handler:
            #     handler.write(img_data)
            
            books.append({
                "title": title,
                "price": price,
                "availability": availability_text,
                "rating": rating,
                "category": category,
                "image_path": img_path
            })
            if len(books) >= min_books:
                break
        
        # Buscar el enlace a la siguiente página
        next_btn = soup.select_one("li.next > a")
        if next_btn:
            next_href = next_btn['href']
            # Construir la URL absoluta para la siguiente página
            base_url = page_url.rsplit('/', 1)[0]
            page_url = f"{base_url}/{next_href}"
        else:
            break

    driver.quit()
    return books