import pandas as pd
import re

def transform_books(books):
    df = pd.DataFrame(books)
    df['price'] = df['price'].replace('£', '', regex=True).astype(float)
    df['rating'] = df['rating'].map({
        'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5
    })
    
    df['availability'] = df['availability'].str.extract(r'(\d+)').astype(float).fillna(0).astype(int)
    
    df.drop_duplicates(subset=['title'], inplace=True)
    return df