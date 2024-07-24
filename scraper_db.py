import requests
from bs4 import BeautifulSoup
import mysql.connector
import re

# Función para limpiar texto
def clean_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# Función para obtener la información "about" de cada autor
def get_author_about(author_url):
    response = requests.get(author_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    about_text = soup.select_one('.author-description').get_text(strip=True)
    about_text = clean_text(about_text)
    return about_text

# Configuración de la conexión a la base de datos MySQL
conn = mysql.connector.connect(
    host='localhost',  # Reemplaza con tu host
    user='root',  # Reemplaza con tu usuario
    password='admin',  # Reemplaza con tu contraseña
    database='quotes_db'  # Reemplaza con tu base de datos
)
cursor = conn.cursor()

# Inicializar la URL base
base_url = "https://quotes.toscrape.com/"
page_url = "page/1/"

# Diccionario para almacenar los autores ya insertados
authors_cache = {}
# Diccionario para almacenar los tags ya insertados
tags_cache = {}

# Bucle para iterar sobre las páginas
while page_url:
    response = requests.get(base_url + page_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extraer las citas y la información asociada
    quotes = soup.select('.quote')

    for quote in quotes:
        text = quote.select_one('.text').get_text(strip=True)
        text = clean_text(text)
        author_name = quote.select_one('.author').get_text(strip=True)
        author_name = clean_text(author_name)
        author_url = base_url + quote.select_one('.author + a')['href']
        tags = [tag.get_text(strip=True) for tag in quote.select('.tags .tag')]
        
        # Insertar o actualizar la información del autor
        if author_name not in authors_cache:
            about = get_author_about(author_url)
            cursor.execute('''
            INSERT INTO authors (name, about)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE about = VALUES(about)
            ''', (author_name, about))
            conn.commit()
            cursor.execute('SELECT id FROM authors WHERE name = %s', (author_name,))
            author_id = cursor.fetchone()[0]
            authors_cache[author_name] = author_id
        else:
            author_id = authors_cache[author_name]

        # Insertar la cita
        cursor.execute('''
        INSERT INTO quotes (text, author_id)
        VALUES (%s, %s)
        ''', (text, author_id))
        conn.commit()
        quote_id = cursor.lastrowid

        # Insertar los tags y la relación con la cita
        for tag_name in tags:
            if tag_name not in tags_cache:
                cursor.execute('''
                INSERT INTO tags (name)
                VALUES (%s)
                ON DUPLICATE KEY UPDATE name = VALUES(name)
                ''', (tag_name,))
                conn.commit()
                cursor.execute('SELECT id FROM tags WHERE name = %s', (tag_name,))
                tag_id = cursor.fetchone()[0]
                tags_cache[tag_name] = tag_id
            else:
                tag_id = tags_cache[tag_name]

            cursor.execute('''
            INSERT INTO quote_tags (quote_id, tag_id)
            VALUES (%s, %s)
            ''', (quote_id, tag_id))
            conn.commit()

    # Verificar si hay una página siguiente
    next_page = soup.select_one('.pager .next a')
    page_url = next_page['href'] if next_page else None

# Cerrar la conexión a la base de datos
conn.close()

