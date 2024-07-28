import logging
import logging.config
import os
from config.config import LOG_CONFIG, DB_CONFIG, SCRAPE_URL
from src.clean_data import clean_data
from src.scraper import Scraper
from src.database import Database


def setup_logging():
    """
    Configura el sistema de logging usando la configuración especificada en LOG_CONFIG.
    """
    logging.config.dictConfig(LOG_CONFIG)

def main():
    """
    Punto de entrada principal del programa.

    Realiza las siguientes tareas:
        1. Configura el logging.
        2. Realiza el web scraping para obtener Frases y autores.
        3. Limpia los datos obtenidos.
        4. Inserta los datos limpios en la base de datos.
    
    En caso de errores, los mismos son registrados y la conexión a la base de datos se cierra adecuadamente.
    """
    setup_logging()
    db = None
    try:
        logging.info("Iniciando el proceso de scraping")
        scraper = Scraper(SCRAPE_URL)
        scraper.scrape_quotes()
        scraper.scrape_authors()
        logging.info("Scraping completado")
        
        logging.info("Iniciando la limpieza de datos")
        cleaned_quotes, cleaned_authors = clean_data(scraper.quotes, scraper.authors.values())
        logging.info("Limpieza de datos completada")

        logging.info("Conectando a la base de datos")
        db = Database(**DB_CONFIG)
        db.create_tables()
        logging.info("Tablas creadas en la base de datos")

        logging.info("Insertando datos en la base de datos")
        db.insert_data(cleaned_quotes, cleaned_authors)
        logging.info("Extracción y almacenamiento de datos completados con éxito")

    except Exception as e:
        logging.error(f"Ha ocurrido un error: {str(e)}")
    finally:
        if db:
            db.close()

if __name__ == "__main__":
    main()