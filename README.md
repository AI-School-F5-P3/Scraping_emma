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

1. Iniciar la aplicación Streamlit:  ***streamlit run app.py**
2. Abrir un navegador web y acceder a la URL proporcionada por Streamlit: ***'http://localhost:8501'***.
3. Utilizar el menú lateral para navegar entre las diferentes funcionalidades de la aplicación.


## Pruebas

Ejecutar las pruebas con pytest:
- ***pytest***

## Estructura del Proyecto

- **"app.py":** Script principal de la aplicación Streamlit.
- **"src/"**: Directorio con módulos de código fuente.
- **"database.py":** Módulo para interactuar con la base de datos.
- **"models.py":** Definiciones de modelos de datos.
- **"scraper.py":** Módulo para web scraping.
- **"config/":** Directorio de configuración.
- **"config.py":** Archivo de configuración con parámetros de la base de datos y logging.
- **"tests/"**: Contiene las pruebas unitarias
- **"logs/"**: Almacena los logs del scraper
- **"main.py"**: Script principal para ejecutar el proyecto
- **"update_database.py**: Script para actualizar automáticamente la BBDD con nuevos datos e intervalos regulares
- **"requirements.txt`:** Lista de dependencias del proyecto.

## Actualización Automática de Datos

El proyecto incluye un script ***update_database.py*** que permite actualizar automáticamente la base de datos con nuevos datos a intervalos regulares. 
Para utilizarlo:

1. Asegurar el script tenga los permisos necesarios para ejecutarse.
2. Configurar el intervalo de actualización en el script según necesidades.
3. Ejecutar el script:
- ***python update_database.py &*** 