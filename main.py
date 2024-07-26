import logging
from config.config import DB_CONFIG, SCRAPE_URL, LOG_CONFIG
from src.scraper import Scraper
from src.database import Database
import streamlit as st

def setup_logging():
    logging.basicConfig(**LOG_CONFIG)

def main():
    setup_logging()
    try:
        scraper = Scraper(SCRAPE_URL)
        scraper.scrape_quotes()
        scraper.scrape_authors()

        db = Database(**DB_CONFIG)
        db.create_tables()
        db.insert_data(scraper.quotes, scraper.authors)
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