import requests
from bs4 import BeautifulSoup
import pandas as pd

# Función para obtener la información "about" de cada autor
def get_author_about(author_url):
    response = requests.get(author_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    about_text = soup.select_one('.author-description').get_text(strip=True)
    return about_text

# Inicializar la URL base
base_url = "https://quotes.toscrape.com/"
page_url = "page/1/"

# Lista para almacenar las citas y la información asociada
data = []

# Bucle para iterar sobre las páginas
while page_url:
    response = requests.get(base_url + page_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extraer las citas y la información asociada
    quotes = soup.select('.quote')

    for quote in quotes:
        text = quote.select_one('.text').get_text(strip=True)
        author = quote.select_one('.author').get_text(strip=True)
        author_url = base_url + quote.select_one('.author + a')['href']
        tags = [tag.get_text(strip=True) for tag in quote.select('.tags .tag')]
        about = get_author_about(author_url)
        
        # Agregar los datos a la lista
        data.append({
            'quote': text,
            'author': author,
            'tags': ', '.join(tags),
            'about': about
        })

    # Verificar si hay una página siguiente
    next_page = soup.select_one('.pager .next a')
    page_url = next_page['href'] if next_page else None

# Crear un DataFrame con los datos
df = pd.DataFrame(data)

# Mostrar los datos en la consola
print(df)

# Opcional: guardar el DataFrame en un archivo CSV
df.to_csv('quotes.csv', index=False)

