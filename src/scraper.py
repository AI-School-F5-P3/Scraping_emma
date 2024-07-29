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
        logging.info(f"Scraper inicializado con URL: {url}")
    
    def scrape_quotes(self):
        """
        Extrae todas las Frases de la página principal.

        Raises:
            Exception: Si ocurre un error durante el scraping.
        """
        try:
            logging.info(f"Iniciando scrape de Frases desde {self.url}")
            page = 1
            while True:
                response = requests.get(f"{self.url}/page/{page}/")
                if response.status_code != 200:
                    logging.warning(f"Finalizada la extracción de Frases en la página {page}. Código de estado: {response.status_code}")
                    break
                soup = BeautifulSoup(response.text, 'html.parser')
                quote_divs = soup.find_all('div', class_='quote')
                if not quote_divs:
                    logging.info(f"No se encontraron más Frases en la página {page}")
                    break
                for quote_div in quote_divs:
                    text = quote_div.find('span', class_='text').text.strip()
                    author = quote_div.find('small', class_='author').text.strip()
                    tags = [tag.text for tag in quote_div.find_all('a', class_='tag')]
                    author_about_link = self.url + quote_div.find('a')['href']
                    self.quotes.append(Quote(text, author, tags, author_about_link))
                page += 1
            logging.info(f"Se han extraído {len(self.quotes)} Frases con éxito")
        except requests.RequestException as e:
            logging.error(f"Error en la solicitud HTTP al extraer Frases: {e}")
            raise
        except Exception as e:
            logging.error(f"Error inesperado al extraer Frases: {e}")
            raise

    def scrape_authors(self):
        """
        Extrae la información de los autores de las Frases.

        Raises:
            RequestException: Si hay un problema al acceder a la página de un autor.
            Exception: Para cualquier otro error inesperado.
        """ 
        try:
            logging.info("Iniciando extracción de información de autores")
            for quote in self.quotes:
                if quote.author not in self.authors:
                    try:
                        response = requests.get(quote.author_about_link)
                        response.raise_for_status()
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        name = quote.author
                        born_date = soup.find('span', class_='author-born-date')
                        born_date = born_date.text.strip() if born_date else "Unknown"
                        born_location = soup.find('span', class_='author-born-location')
                        born_location = born_location.text.strip() if born_location else "Unknown"
                        description = soup.find('div', class_='author-description')
                        description = description.text.strip() if description else "No description available"
                        
                        about = f"Born: {born_date} in {born_location}\n\n{description}"
                        self.authors[quote.author] = Author(name, about, quote.author_about_link)
                    except requests.RequestException as e:
                        logging.error(f"Error en la solicitud HTTP al extraer información del autor {quote.author}: {e}")
                        raise
                    except Exception as e:
                        logging.error(f"Error inesperado al extraer información del autor {quote.author}: {e}")
                        raise
            logging.info(f"Se han extraído {len(self.authors)} autores con éxito")
        except Exception as e:
            logging.error(f"Error extrayendo autores: {e}")
            raise
