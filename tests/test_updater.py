# src/updater.py
import logging
from src.database import Database
from src.scraper import Scraper
from config.config import LOG_CONFIG

def setup_logging():
    logging.basicConfig(**LOG_CONFIG)

def update_database():
    setup_logging()
    try:
        scraper = Scraper()
        scraper.scrape_quotes()
        scraper.scrape_authors()

        db = Database()
        db.create_tables()
        db.insert_data(scraper.quotes, scraper.authors)
        db.close()
        logging.info("Actualización de la base de datos completada con éxito")
    except Exception as e:
        logging.error(f"Se produjo un error durante la actualización: {e}")
