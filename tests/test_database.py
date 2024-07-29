from sqlite3 import Error
import pytest
import sqlite3
from src.database import Database
from src.models import Quote, Author
import logging
import logging.config
from config.config import LOG_CONFIG

logging.config.dictConfig(LOG_CONFIG)

@pytest.fixture
def database():
    """
    Configura una base de datos SQLite en memoria para las pruebas unitarias.

    Yields:
        Database: Instancia de la clase Database conectada a una base de datos en memoria.
    """
    db = Database(database=':memory:') 
    db.create_tables()
    yield db
    db.close()

def test_database_type(database):
    """
    Verifica que la base de datos de prueba sea una instancia de sqlite3.Connection.

    Args:
        database (Database): Instancia de la base de datos de prueba.
    """    
    assert isinstance(database.connection, sqlite3.Connection), "La base de datos de prueba debe ser SQLite"
    
    
def test_create_tables(database):
    """
    Verifica que las tablas necesarias se hayan creado correctamente.

    Args:
        database (Database): Instancia de la base de datos de prueba.
    """
    try:
        database.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = database.cursor.fetchall()
        tables = [table[0] for table in tables]
        assert "authors" in tables
        assert "quotes" in tables
        assert "tags" in tables
        assert "quote_tags" in tables
        logging.info("Verificación correcta para la creacción de tablas.")
    except Error as e:
        logging.error(f"Error verificando la creación de tablas: {str(e)}")
        raise

def test_insert_data(database):
    """
    Inserta datos en la base de datos y verifica que se hayan insertado correctamente.

    Args:
        database (Database): Instancia de la base de datos de prueba.
    """
    authors = {
        "Albert Einstein": Author(
            "Albert Einstein", 
            "Físico teórico alemán.", 
            "https://quotes.toscrape.com/author/Albert-Einstein"
        ),
    }
    quotes = [
        Quote("La vida es como andar en bicicleta. Para mantener el equilibrio, debes seguir moviéndote.", 
            "Albert Einstein", 
            ["vida", "movimiento"],
            "https://quotes.toscrape.com/author/Albert-Einstein"
        )
    ]
    try:
        database.insert_data(quotes, authors)
        
        # Verificar que los datos se insertaron correctamente
        database.cursor.execute("SELECT COUNT(*) FROM authors")
        assert database.cursor.fetchone()[0] == 1
        
        database.cursor.execute("SELECT COUNT(*) FROM quotes")
        assert database.cursor.fetchone()[0] == 1
        
        database.cursor.execute("SELECT COUNT(*) FROM tags")
        assert database.cursor.fetchone()[0] == 2
        logging.info("Verificación corecta para la inserción de datos.")
    except Error as e:
        logging.error(f"Error insertando datos: {str(e)}")
        raise

def test_get_author_id(database):
    """
    Verifica la obtención del ID de un autor en la base de datos.

    Args:
        database (Database): Instancia de la base de datos de prueba.
    """
    author_name = "Albert Einstein"
    about = "Físico teórico alemán."
    about_link = "https://quotes.toscrape.com//author/Albert-Einstein"
    
    try:
        # Primero, intentamos obtener el ID del autor
        author_id = database.get_author_id(author_name)
        
        if author_id is None:
            # Si el autor no existe, lo insertamos
            database.cursor.execute("INSERT INTO authors (name, about, about_link) VALUES (?, ?, ?)", 
                                    (author_name, about, about_link))
            database.connection.commit()
            author_id = database.get_author_id(author_name)
            assert author_id is not None
    except Error as e:
        logging.error(f"Error obteniendo ID del autor: {str(e)}")
        raise

def test_get_tag_id(database):
    """
    Verifica la obtención del ID de una etiqueta en la base de datos.

    Args:
        database (Database): Instancia de la base de datos de prueba.
    """
    tag_name = "vida"
    try: 
        # Primero, insertamos un tag
        database.cursor.execute("INSERT INTO tags (name) VALUES (?)", (tag_name,))        
        database.connection.commit()
        tag_id = database.get_tag_id(tag_name)
        assert tag_id is not None

        # Intentar obtener un tag que no existe
        non_existent_tag = database.get_tag_id("non_existent_tag")
        assert non_existent_tag is None
        assert non_existent_tag is None
    except Error as e:
        logging.error(f"Error obteniendo ID de la etiqueta: {str(e)}")
        raise
    
def test_insertion(database):
    """
    Prueba la inserción de un autor en la base de datos.

    Args:
        database (Database): Instancia de la base de datos de prueba.
    """
    try:
        if database.is_mysql:
            database.cursor.execute("INSERT INTO authors (name, about, about_link) VALUES (%s, %s, %s)", 
                                ("Test Author", "Test About", "http://test.com"))
        else:
            database.cursor.execute("INSERT INTO authors (name, about, about_link) VALUES (?, ?, ?)", 
                                ("Test Author", "Test About", "http://test.com"))
        database.connection.commit()
        logging.info("Inserción de prueba exitosa")
    except Error as e:
        logging.error(f"Error en inserción de prueba: {str(e)}")
        database.connection.rollback()