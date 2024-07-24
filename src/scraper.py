import requests
from bs4 import BeautifulSoup
import logging
from .models import Quote, Author

class Scraper:
    """
    Clase para realizar web scraping en quotes.toscrape.com.

    Attributes:
        url (str): La URL base del sitio web a scrapear.
        quotes (list): Lista de objetos Quote extraídos.
        authors (dict): Diccionario de objetos Author extraídos.
    """

    def __init__(self, url):
        self.url = url
        self.quotes = []
        self.authors = {}

    def scrape_quotes(self):
        """
        Extrae todas las citas de la página principal.

        Raises:
            Exception: Si ocurre un error durante el scraping.
        """
        try:
            response = requests.get(self.url)
            soup = BeautifulSoup(response.text, 'html.parser')
            quote_divs = soup.find_all('div', class_='quote')

            for quote_div in quote_divs:
                text = quote_div.find('span', class_='text').text.strip()
                author = quote_div.find('small', class_='author').text.strip()
                tags = [tag.text for tag in quote_div.find_all('a', class_='tag')]
                self.quotes.append(Quote(text, author, tags))

            logging.info(f"Se han extraído {len(self.quotes)} citas con éxito")
        except Exception as e:
            logging.error(f"Error extrayendo citas: {str(e)}")
            raise

    def scrape_authors(self):
        try:
            for quote in self.quotes:
                if quote.author not in self.authors:
                    author_url = self.url + 'author/' + quote.author.replace(' ', '-')
                    response = requests.get(author_url)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    name = quote.author  # Usamos el nombre que ya tenemos
                    
                    # Usamos .get() para manejar casos donde el elemento no existe
                    born_date = soup.find('span', class_='author-born-date')
                    born_date = born_date.text.strip() if born_date else "Unknown"
                    
                    born_location = soup.find('span', class_='author-born-location')
                    born_location = born_location.text.strip() if born_location else "Unknown"
                    
                    description = soup.find('div', class_='author-description')
                    description = description.text.strip() if description else "No description available"

                    # Combinar toda la información en un solo campo 'about'
                    about = f"Born: {born_date} in {born_location}\n\n{description}"

                    self.authors[quote.author] = Author(name, about)

            logging.info(f"Se han extraído {len(self.authors)} autores con éxito")
        except Exception as e:
            logging.error(f"Error extrayendo autores: {str(e)}")
            raise