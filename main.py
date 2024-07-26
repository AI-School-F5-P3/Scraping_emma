import logging
import os
from config.config import LOG_CONFIG, DB_CONFIG, SCRAPE_URL, log_dir
from src.clean_data import clean_data
from src.scraper import Scraper
from src.database import Database
import streamlit as st

# Configuración del archivo de log
def setup_logging():
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logging.basicConfig(**LOG_CONFIG)

def main():
    setup_logging()
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

        # Streamlit frontend
        st.title("Quotes Database Viewer")
        
        # Mostrar citas
        st.header("Quotes")
        for quote in scraper.quotes:
            st.write(f'"{quote.text}" - {quote.author}')
            st.write(f"Tags: {', '.join(quote.tags)}")
            st.write("---")
        
        # Mostrar autores
        st.header("Authors")
        for author in scraper.authors.values():
            st.write(f"Name: {author.name}")
            st.write(f"About: {author.about[:200]}...")  # Mostrar solo los primeros 200 caracteres
            st.write(f"About link: {author.about_link}")
            st.write("---")

    except Exception as e:
        logging.error(f"Ha ocurrido un error: {str(e)}")

if __name__ == "__main__":
    main()