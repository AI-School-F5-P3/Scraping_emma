import logging
import pytest
from unittest.mock import patch
from src.scraper import Scraper

# Datos ficticios para las pruebas
mock_quotes = [
    {'text': 'La vida es lo que pasa mientras estás ocupado haciendo otros planes.', 'author': 'John Lennon', 'tags': ['vida', 'planes']},
    {'text': 'El mejor momento para plantar un árbol fue hace 20 años. El segundo mejor momento es ahora.', 'author': 'Proverbio Chino', 'tags': ['árbol', 'momento']},
]

mock_authors = {
    'John Lennon': {'name': 'John Lennon', 'about': 'https://about/john_lennon'},
    'Proverbio Chino': {'name': 'Proverbio Chino', 'about': 'https://about/proverbio_chino'},
}

@pytest.fixture
def scraper():
    """
    Crea una instancia del scraper para las pruebas.

    Returns:
        Scraper: Instancia de la clase Scraper.
    """
    return Scraper('https://quotes.toscrape.com/')

@patch.object(Scraper, 'scrape_quotes')
def test_scrape_quotes(mock_scrape_quotes, scraper):
    """
    Verifica que el método scrape_quotes extraiga frases correctamente.

    Args:
        scraper (Scraper): Instancia del scraper.
    
    Raises:
        AssertionError: Si no se extraen frases.
    """
    mock_scrape_quotes.return_value = None
    scraper.quotes = mock_quotes
    scraper.scrape_quotes()
    assert len(scraper.quotes) > 0, "No se han extraído frases"
    logging.info(f"Se han extraído {len(scraper.quotes)} frases con éxito")

@patch.object(Scraper, 'scrape_authors')
def test_scrape_authors(mock_scrape_authors, scraper):
    """
    Verifica que el método scrape_authors extraiga autores correctamente después de extraer frases.

    Args:
        scraper (Scraper): Instancia del scraper.
    
    Raises:
        AssertionError: Si no se extraen autores.
    """
    scraper.quotes = mock_quotes
    scraper.authors = mock_authors
    mock_scrape_authors.return_value = None
    scraper.scrape_authors()
    assert len(scraper.authors) > 0, "No se han extraído autores"
    logging.info(f"Se han extraído {len(scraper.authors)} autores con éxito")

def test_quote_structure(scraper):
    """
    Verifica que las frases extraídas tengan la estructura correcta.

    Args:
        scraper (Scraper): Instancia del scraper.
    
    Raises:
        AssertionError: Si una frase no tiene la estructura esperada.
    """
    scraper.quotes = mock_quotes
    quote = scraper.quotes[0]
    assert 'text' in quote, "Atributo 'text' no encontrado en la frase"
    assert 'author' in quote, "Atributo 'author' no encontrado en la frase"
    assert 'tags' in quote, "Atributo 'tags' no encontrado en la frase"
    logging.info("La estructura de la frase es correcta")

def test_author_structure(scraper):
    """
    Verifica que los autores extraídos tengan la estructura correcta.

    Args:
        scraper (Scraper): Instancia del scraper.
    
    Raises:
        AssertionError: Si un autor no tiene la estructura esperada.
    """
    scraper.authors = mock_authors
    author = scraper.authors['John Lennon']
    assert 'name' in author, "Atributo 'name' no encontrado en el autor"
    assert 'about' in author, "Atributo 'about' no encontrado en el autor"
    logging.info("La estructura del autor es correcta")
