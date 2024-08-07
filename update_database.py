import time
import schedule
import logging
from src.scraper import Scraper
from src.database import Database
from src.clean_data import clean_data
from config.config import DB_CONFIG, SCRAPE_URL, LOG_CONFIG


def update_database():
    '''
    Esta función:
    1. Inicializa el scraper y obtiene nuevos datos.
    2. Limpia los datos obtenidos.
    3. Conecta a la base de datos e inserta los nuevos datos.
    '''
    logging.info("Iniciando actualización de la base de datos")
    
    try:
        # Inicializar el scraper y obtener nuevos datos
        scraper = Scraper(SCRAPE_URL)
        scraper.scrape_quotes()
        scraper.scrape_authors()
        
        # Limpiar los nuevos datos
        cleaned_quotes, cleaned_authors = clean_data(scraper.quotes, scraper.authors.values())
        
        # Conectar a la base de datos e insertar los nuevos datos
        db = Database(**DB_CONFIG)
        db.insert_data(cleaned_quotes, cleaned_authors)
        
        logging.info("Actualización de la base de datos completada con éxito")
    except Exception as e:
        logging.error(f"Error durante la actualización de la base de datos: {str(e)}")
    finally:
        if 'db' in locals():
            db.close()

def run_scheduler():
    '''
    Esta función:
    1. Programa la ejecución de update_database() cada 24 horas (o en el intervalo de tiempo que interese).
    '''
    schedule.every(1).minute.do(update_database)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    logging.info("Iniciando el programador de actualizaciones")
    run_scheduler()