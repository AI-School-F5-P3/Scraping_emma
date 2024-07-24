import pytest
from src.scraper import Scraper

@pytest.fixture
def scraper():
    return Scraper('https://quotes.toscrape.com/')

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
    assert hasattr(author, 'about'), "Atributo 'about' no encontrado para autor"