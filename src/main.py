from extract import extract_books
from transform import transform_books
from load import load_to_csv, load_csv_to_mysql

def main():
    url = "https://books.toscrape.com/catalogue/category/books_1/index.html"
    books = extract_books(url, min_books=500)
    print(f"Libros extraídos: {len(books)}")
    print("Primeros 3 libros:")
    for book in books[:3]:
        print(book)
    df = transform_books(books)
    print(df.info())
    load_to_csv(df)
    load_csv_to_mysql()
    
if __name__ == "__main__":
    print("Iniciando proceso ETL...")
    main()