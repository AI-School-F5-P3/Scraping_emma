from dotenv import load_dotenv
import os

'''
En este archivo se realizan las siguentes operaciones:
- Cargar variables de entorno.
- Configurar la base de datos y la URL de scraping.
- Implementar una configuración de logging más robusta con handlers para 
archivo y consola.
'''
load_dotenv()

# Obtener el directorio del proyecto
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configuración de la base de datos
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'admin'),
    'database': os.getenv('DB_NAME', 'quotes_db')
}

# # URL del sitio web a scrapear
SCRAPE_URL = os.getenv('SCRAPE_URL', 'https://quotes.toscrape.com/')

# Configuración mejorada de logs
LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/scraping.log',
            'mode': 'a',
            'formatter': 'standard',
            'encoding': 'utf-8',
        
        }
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True
        }
    }
}


