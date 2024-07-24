import pytest
from src.scraper import Scraper
from config.config import SCRAPE_URL  # Asegúrate de importar la URL de scraping

@pytest.fixture
def scraper():
    return Scraper() # Asume que Scraper no necesita argumentos en el constructor

def test_scrape_quotes(scraper):
    scraper.scrape_quotes()
    assert len(scraper.quotes) > 0, "No se han extraído citas"

def test_scrape_authors(scraper):
    scraper.scrape_quotes()
    scraper.scrape_authors()
    assert len(scraper.authors) > 0, "No se han extraido autores"

def test_quote_structure(scraper):
    scraper.scrape_quotes()
    quote = scraper.quotes[0]
    assert hasattr(quote, 'text'), "Atributo 'text' no encontrado para cita"
    assert hasattr(quote, 'author'), "Atributo 'text' no encontrado para autor"
    assert hasattr(quote, 'tags'), "Atributo 'text' no encontrado para etiqueta"

def test_author_structure(scraper):
    scraper.scrape_quotes()
    scraper.scrape_authors()
    author = next(iter(scraper.authors.values()))
    assert hasattr(author, 'name'), "Atributo 'name'  no encontrado para autor"
    assert hasattr(author, 'bio'), "Atributo 'bio' no encontrado para autor"