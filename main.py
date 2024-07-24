import logging
from config.config import DB_CONFIG, SCRAPE_URL, LOG_CONFIG
from src.scraper import Scraper
from src.database import Database
import schedule
import time
from src.updater import update_database

def setup_logging():
    """Configura el sistema de logging."""
    logging.basicConfig(**LOG_CONFIG)

def main():
    """Función principal que ejecuta el proceso de scraping y almacenamiento."""
    setup_logging()

    try:
        # Iniciar el scraper
        scraper = Scraper(SCRAPE_URL)
        scraper.scrape_quotes()
        scraper.scrape_authors()

        # Iniciar la base de datos y almacenar los datos
        db = Database(**DB_CONFIG)
        db.create_tables()
        db.insert_data(scraper.quotes, scraper.authors)
        db.close()
        
        # Automatizar la base de datos
        schedule.every().day.at("00:00").do(update_database)
        while True:
            schedule.run_pending()
            time.sleep(1)
            
        logging.info("Extracción y almacenamiento de datos completados con éxito")
    except Exception as e:
        logging.error(f"Ha ocurrido un error al extraer y almacenar los datos: {str(e)}")

if __name__ == "__main__":
    main()