# Proyecto Web Scraping

Este proyecto realiza una aplicacion Web desarrollada con Streamlit para extraer, limpiar y gestionar citas de la web ***'quotes.toscrape.com'***. Los datos se almacenan en una base de datos MySQL y se muestran en una interfaz fácil de usar. 

La realización de test unitarios se realiza a través de SQLite.

## Requisitos

- **Software:** Python 3.11, pip
- **Dependencias:** Lista de bibliotecas como streamlit, pandas, mysql-connector-python, etc.

## Instalación

1. Clonar el repositorio:
- ***git clone https://github.com/AI-School-F5-P3/Scraping_emma.git***

2. Crear un entorno virtual e instalar las dependencias:
- ***python -m venv venv***
- ***venv\Scripts\activate***
- ***pip install -r requirements.txt***

## Configuración
1. **Variables de Entorno:** Configuración de variables para la conexión a la base de datos y URL de scraping, utilizando ***'.env'***.
3. **Configurar la base de datos:**
- Crear una base de datos MySQL llamada ***"quotes_db"***
- Actualizar los datos de conexión en ***"config/config.py"***


## Uso

Ejecutar el script principal:
- ***python main.py***

Ejecutar la aplicación:
- ***streamlit run app.py**

## Pruebas

Ejecutar las pruebas con pytest:
- ***pytest***

## Estructura del Proyecto

- **"src/"**: Contiene el código fuente del proyecto
- **"tests/"**: Contiene las pruebas unitarias
- **"config/"**: Contiene la configuración del proyecto
- **"logs/"**: Almacena los logs del scraper
- **"main.py"**: Script principal para ejecutar el proyecto
- **"app.py"**: Archivo principal de una aplicación desarrollada en Streamlit para la visualización y gestión de citas extraídas de la web.


