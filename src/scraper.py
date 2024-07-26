import requests
from bs4 import BeautifulSoup
import logging
from .models import Quote, Author

class Scraper:
    def __init__(self, url):
        self.url = url
        self.quotes = []
        self.authors = {}
        logging.info(f"Scraper inicializado con URL: {url}")
    
    def scrape_quotes(self):
        try:
            logging.info(f"Iniciando scrape de citas desde {self.url}")
            page = 1
            while True:
                response = requests.get(f"{self.url}/page/{page}/")
                if response.status_code != 200:
                    break
                soup = BeautifulSoup(response.text, 'html.parser')
                quote_divs = soup.find_all('div', class_='quote')
                if not quote_divs:
                    break
                for quote_div in quote_divs:
                    text = quote_div.find('span', class_='text').text.strip()
                    author = quote_div.find('small', class_='author').text.strip()
                    tags = [tag.text for tag in quote_div.find_all('a', class_='tag')]
                    author_about_link = self.url + quote_div.find('a')['href']
                    self.quotes.append(Quote(text, author, tags, author_about_link))
                    logging.debug(f"Cita extraída: {text[:30]}...")
                page += 1
            logging.info(f"Se han extraído {len(self.quotes)} citas con éxito")
        except Exception as e:
            logging.error(f"Error al extraer citas: {str(e)}")
            raise

    def scrape_authors(self):
        try:
            logging.info("Iniciando scrape de autores")
            for quote in self.quotes:
                if quote.author not in self.authors:
                    response = requests.get(quote.author_about_link)
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
                    logging.debug(f"Autor extraído: {name}")
            
            logging.info(f"Se han extraído {len(self.authors)} autores con éxito")
        except Exception as e:
            logging.error(f"Error extrayendo autores: {str(e)}")
            raise