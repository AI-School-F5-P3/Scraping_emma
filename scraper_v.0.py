import requests                  # Para realizar solicitudes HTTP
from bs4 import BeautifulSoup    # Para analizar el HTML de la página
import re                        # Para realizar operaciones de limpieza de texto mediante expresiones regulares
import pandas as pd              # Para manejar y mostrar datos en formato tabular

'''
Descripción General

Este script está diseñado para extraer citas, autores y etiquetas de la página principal de quotes.toscrape.com y presentarlas en un DataFrame de pandas. Utiliza las bibliotecas requests para realizar solicitudes HTTP, BeautifulSoup para analizar el HTML y re para limpiar el texto extraído.
Requisitos

    Python 3.x
    requests
    beautifulsoup4
    pandas

'''
# URL del sitio a scrapear
url = "https://quotes.toscrape.com/"
response = requests.get(url)

# Crear un objeto BeautifulSoup para analizar el HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Lista para almacenar las citas extraídas
quotes = []

# Encontrar todos los elementos div con la clase 'quote'
'''
Encuentra todos los elementos div con la clase quote.
Limpia y extrae el texto de la cita, el autor y las etiquetas.
Almacena la información en una lista de diccionarios.
'''
for quote in soup.find_all('div', class_='quote'):
    # Extrae y limpia el texto de la cita
    text = quote.find('span', class_='text').get_text()
    text = text.strip()
    text = text.strip('"')
    text = re.sub(r'\s+', ' ', text)
    text = text.lower()

    # Extrae y limpia el nombre del autor
    author = quote.find('small', class_='author').get_text()
    author = author.strip()
    author = author.strip('"')
    author = re.sub(r'\s+', ' ', author)
    author = author.lower()

    # Extrae y limpia las etiquetas
    tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
    tags = [tag.strip() for tag in tags]
    tags = [tag.strip('"') for tag in tags]
    tags = [re.sub(r'\s+', ' ', tag) for tag in tags]
    tags = [tag.lower() for tag in tags]

    # Añadir la información extraída a la lista de citas
    quotes.append({
        'text': text,
        'author': author,
        'tags': tags
    })

# Crear un DataFrame a partir de la lista de citas
df = pd.DataFrame(quotes)

# Expandir las etiquetas en columnas separadas
df_expanded = df.explode('tags')

# Mostrar el DataFrame en formato de tabla
print(df_expanded)

