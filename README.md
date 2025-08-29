# Web Scraping y ETL: Análisis de Libros

Este proyecto realiza un proceso completo de **Extracción, Transformación y Carga (ETL)** de datos de libros desde el sitio [Books to Scrape](https://books.toscrape.com/). El objetivo es obtener información detallada sobre los libros, limpiarla y analizarla para obtener insights útiles.

---

## 📌 Descripción

El proyecto está diseñado para:

- **Extraer** datos de libros desde una página web utilizando técnicas de web scraping.
- **Transformar** los datos para limpiarlos y estructurarlos adecuadamente.
- **Cargar** los datos procesados en un formato adecuado para su análisis y visualización.

---

## 🛠️ Tecnologías Usadas

- **Python 3**  
- **Selenium** → Automatización del navegador y extracción de datos.  
- **BeautifulSoup** → Parseo y scraping de HTML.  
- **Pandas** → Limpieza y manipulación de datos.  
- **NumPy** → Operaciones numéricas y estadísticas.  
- **Matplotlib y Seaborn** → Visualización de datos.  
- **MySQL** (opcional) → Carga de datos procesados a base de datos.  
- **Jupyter Notebook** → Análisis exploratorio interactivo.

---

## 📂 Estructura del Proyecto

```plaintext
Web-Scraping-y-ETL/
├── data/
│   ├── raw/              # Datos crudos extraídos
│   └── processed/        # Datos procesados listos para análisis
├── notebook/             # Jupyter Notebooks para análisis exploratorio
├── src/                  # Código fuente del scraper y procesamiento
│   ├── extract.py        # Funciones para extracción de datos
│   ├── transform.py      # Funciones para transformación de datos
│   └── load.py           # Funciones para carga de datos
├── .gitignore            # Archivos y carpetas a ignorar por Git
├── requirements.txt      # Dependencias del proyecto
└── README.md             # Documentación del proyecto
```
## 🛠️ Requisitos

Para ejecutar este proyecto, necesitas tener instaladas las siguientes dependencias:
`pip install -r requirements.txt`

## 🚀 Uso

- Extracción de datos: Ejecuta el script de extracción para obtener los datos de los libros.
- Transformación de datos: Utiliza las funciones de transformación para limpiar y estructurar los datos.
- Carga de datos: Guarda los datos procesados en el formato deseado (CSV, base de datos, etc.).
- Análisis: Abre el notebook en notebook/ para realizar un análisis exploratorio y visualizar los datos.

## 📊 Análisis Exploratorio

En el Jupyter Notebook proporcionado, se realizan los siguientes análisis:

- Distribución de precios de los libros.
- Relación entre precio y rating.
- Identificación de los libros más caros y más baratos.
- Análisis de la disponibilidad de los libros por categoría.
