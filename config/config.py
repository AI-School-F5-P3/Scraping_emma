from dotenv import load_dotenv
import os

load_dotenv()

# Obtener el directorio del proyecto
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_TYPE = os.getenv('DB_TYPE', 'mysql')
DB_NAME = os.getenv('DB_NAME', 'quotes_db')

if DB_TYPE == 'mysql':
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME', 'quotes_db')
    }
else:
    DB_CONFIG = {
        'database': os.getenv('DB_NAME', 'quotes_test.db')
    }

SCRAPE_URL = os.getenv('SCRAPE_URL')

# Configuración de logs
log_dir = os.path.join(project_dir, 'logs')
os.makedirs(log_dir, exist_ok=True)

LOG_CONFIG = {
    'level': os.getenv('LOG_LEVEL', 'INFO'),
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'filename': os.path.join('logs', 'scraping.log'),
    'filemode': 'a',
    'encoding': 'utf-8'  # Añade esta línea para especificar la codificación
}

