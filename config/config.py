# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin',
    'database': 'quotes_db'
}

# URL del sitio web a scrapear
SCRAPE_URL = 'https://quotes.toscrape.com/'

# Configuración de logging
LOG_CONFIG = {
    'filename': 'logs/scraper.log',
    'level': 'DEBUG',
    'format': '%(asctime)s:%(levelname)s:%(message)s',
    'encoding': 'utf-8'
}