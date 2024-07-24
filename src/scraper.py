import requests
from bs4 import BeautifulSoup
import logging
from .models import Quote, Author
from config.config import SCRAPE_URL
class Scraper:
    """
    Clase para realizar web scraping en quotes.toscrape.com.

    Attributes:
        url (str): La URL base del sitio web a scrapear.
        quotes (list): Lista de objetos Quote extraídos.
        authors (dict): Diccionario de objetos Author extraídos.
    """

    def __init__(self):
        self.url = SCRAPE_URL
        self.quotes = []
        self.authors = {}

    def scrape_quotes(self):
        """
        Extrae todas las citas de la página principal.

        Raises:
            Exception: Si ocurre un error durante el scraping.
        """
        try:
            # Hacer una solicitud HTTP a la página web
            response = requests.get(self.url)
            response.raise_for_status()
            
            # Parsear el HTML con BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            quote_divs = soup.find_all('div', class_='quote')

            # Extraer las frases y la información asociada
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
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')
                    author_description = soup.find('div', class_='author-description')
                    if author_description:
                        about = author_description.text.strip()
                    else:
                        about = "Biografía no disponible"
                    self.authors[quote.author] = Author(quote.author, about)

            logging.info(f"Se han extraído {len(self.authors)} autores con éxito")
        except Exception as e:
            logging.error(f"Error extrayendo autores: {str(e)}")
            raise