# Proyecto Web Scraping

Este proyecto realiza web scraping en el sitio quotes.toscrape.com para extraer Frases, autores y etiquetas, y almacenarlos en una base de datos MySQL.

## Requisitos

- Python 3.11
- MySQL

## Instalación

1. Clonar el repositorio:
- ***git clone https://github.com/AI-School-F5-P3/Scraping_emma.git***

2. Crear un entorno virtual e instalar las dependencias:
- ***python -m venv venv***
- ***venv\Scripts\activate***
- ***pip install -r requirements.txt***


3. Configurar la base de datos:
- Crear una base de datos MySQL llamada ***"quotes_db"***
- Actualizar los datos de conexión en ***"config/config.py"***

## Uso

Ejecutar el script principal:
- ***python main.py***

## Pruebas

Ejecutar las pruebas con pytest:
- ***pytest***

## Estructura del Proyecto

- **"src/"**: Contiene el código fuente del proyecto
- **"tests/"**: Contiene las pruebas unitarias
- **"config/"**: Contiene la configuración del proyecto
- **"logs/"**: Almacena los logs del scraper
- **"main.py"**: Script principal para ejecutar el proyecto

## Contribuir

Si deseas contribuir al proyecto, por favor:

1. Haz un fork del repositorio
2. Crea una nueva rama (***"git checkout -b feature/AmazingFeature"***)
3. Haz commit de tus cambios (***"git commit -m 'Add some AmazingFeature'"***)
4. Haz push a la rama (***"git push origin feature/AmazingFeature"***)
5. Abre un Pull Request

## Licencia

Distribuido bajo la licencia MIT. Ver ***"LICENSE"*** para más información.