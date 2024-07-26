from dotenv import load_dotenv
import os

load_dotenv()

DB_TYPE = os.getenv('DB_TYPE', 'mysql')
DB_NAME = os.getenv('DB_NAME', 'quotes_db')

if DB_TYPE == 'sqlite':
    DB_CONFIG = {
        'database': DB_NAME
    }
else:
    DB_CONFIG = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': DB_NAME
    }

SCRAPE_URL = os.getenv('SCRAPE_URL')

project_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(project_dir, 'logs')

LOG_CONFIG = {
    'level': os.getenv('LOG_LEVEL', 'INFO'),
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'filename': os.path.join('logs', 'scraping.log'),
    'filemode': 'a',
    'encoding': 'utf-8'  # Añade esta línea para especificar la codificación
}

