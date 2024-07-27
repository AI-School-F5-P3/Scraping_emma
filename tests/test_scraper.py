import logging
import pytest
from src.scraper import Scraper

@pytest.fixture
def scraper():
    """
    Crea una instancia del scraper con la URL base para las pruebas.

    Returns:
        Scraper: Instancia de la clase Scraper inicializada con la URL base.
    """
    return Scraper('https://quotes.toscrape.com/')

def test_scrape_quotes(scraper):
    """
    Verifica que el método scrape_quotes extraiga citas correctamente.

    Args:
        scraper (Scraper): Instancia del scraper.
    
    Raises:
        AssertionError: Si no se extraen citas.
    """
    try:
        logging.info("Iniciando test_scrape_quotes")
        scraper.scrape_quotes()
        assert len(scraper.quotes) > 0, "No se han extraído citas"
        logging.info(f"Se han extraído {len(scraper.quotes)} citas con éxito")
    except Exception as e:
        logging.error(f"Error en test_scrape_quotes: {str(e)}")
        raise

def test_scrape_authors(scraper):
    """
    Verifica que el método scrape_authors extraiga autores correctamente después de extraer citas.

    Args:
        scraper (Scraper): Instancia del scraper.
    
    Raises:
        AssertionError: Si no se extraen autores.
    """
    try:
        logging.info("Iniciando test_scrape_authors")
        scraper.scrape_quotes()
        scraper.scrape_authors()
        assert len(scraper.authors) > 0, "No se han extraído autores"
        logging.info(f"Se han extraído {len(scraper.authors)} autores con éxito")
    except Exception as e:
        logging.error(f"Error en test_scrape_authors: {str(e)}")
        raise

def test_quote_structure(scraper):
    """
    Verifica que las citas extraídas tengan la estructura correcta.

    Args:
        scraper (Scraper): Instancia del scraper.
    
    Raises:
        AssertionError: Si una cita no tiene la estructura esperada.
    """
    try:
        logging.info("Iniciando test_quote_structure")
        scraper.scrape_quotes()
        quote = scraper.quotes[0]
        assert hasattr(quote, 'text'), "Atributo 'text' no encontrado en la cita"
        assert hasattr(quote, 'author'), "Atributo 'author' no encontrado en la cita"
        assert hasattr(quote, 'tags'), "Atributo 'tas' no encontrado en la cita"
        logging.info("La estructura de la cita es corgrecta")
    except Exception as e:
        logging.error(f"Error en test_quote_structure: {str(e)}")
        raise

def test_author_structure(scraper):
    """
    Verifica que los autores extraídos tengan la estructura correcta.

    Args:
        scraper (Scraper): Instancia del scraper.
    
    Raises:
        AssertionError: Si un autor no tiene la estructura esperada.
    """
    try:
        logging.info("Iniciando test_author_structure")
        scraper.scrape_quotes()
        scraper.scrape_authors()
        author = next(iter(scraper.authors.values()))
        assert hasattr(author, 'name'), "Atributo 'name' no encontrado en el autor"
        assert hasattr(author, 'about'), "Atributo 'about' no encontrado en el autor"
        logging.info("La estructura del autor es correcta")
    except Exception as e:
        logging.error(f"Error en test_author_structure: {str(e)}")
        raise