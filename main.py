import logging
import os
from config.config import LOG_CONFIG, DB_CONFIG, SCRAPE_URL
from src.clean_data import clean_data
from src.scraper import Scraper
from src.database import Database
import streamlit as st

# Configuración del archivo de log
def setup_logging():

    logging.basicConfig(**LOG_CONFIG)

def main():
    setup_logging()
    db = None
    try:
        scraper = Scraper(SCRAPE_URL)
        scraper.scrape_quotes()
        scraper.scrape_authors()
        
        # Limpiar los datos antes de insertarlos
        cleaned_quotes, cleaned_authors = clean_data(scraper.quotes, scraper.authors.values())

        db = Database(**DB_CONFIG)
        db.create_tables()
        db.insert_data(cleaned_quotes, cleaned_authors)
        #db.insert_data(scraper.quotes, scraper.authors)
        db.close()

        logging.info("Extracción y almacenamiento de datos completados con éxito")

    except Exception as e:
        logging.error(f"Ha ocurrido un error: {str(e)}")
    finally:
        if db:
            db.close()

if __name__ == "__main__":
    main()