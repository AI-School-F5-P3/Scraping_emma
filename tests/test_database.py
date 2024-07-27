#import logging
#from sqlite3 import Error
import pytest
import sqlite3
from src.database import Database
from src.models import Quote, Author
#from config.config import DB_CONFIG
import logging

@pytest.fixture
def database():
    # Usar SQLite en memoria para las pruebas
    db = Database(database=':memory:') 
    assert not db.is_mysql, "Test database should be SQLite, not MySQL"
    db.create_tables()
    yield db
    db.close()

def test_database_type(database):
    assert isinstance(database.connection, sqlite3.Connection), "Test database should be SQLite"
    
#@pytest.fixture
#def database():
 #   db = Database(
  #      host="localhost",
   #     user="root",
    #    password="admin",
     #   database="quotes_db"
   # )
    
    #try:
     #   db.clean_database()  # Llama a la función clean_database antes de cada prueba
    #except Exception as e:
     #   print(f"Error al limpiar la base de datos: {e}")
    #yield db
    #try:
    #    db.clean_database()  # Asegura que la base de datos esté limpia después de cada prueba
    #except Exception as e:
    #    print(f"Error al limpiar la base de datos: {e}")
    #db.close()
    
def test_create_tables(database):
    # Verifica que las tablas existan
    
#   database.create_tables()
#   database.cursor.execute("SHOW TABLES")
#   tables = database.cursor.fetchall()
#   assert len(tables) == 4  # authors, quotes, tags, quote_tags

    #database.create_tables()
    #database.cursor.execute("SHOW TABLES")
    # Verifica que las tablas existan
    database.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = database.cursor.fetchall()
    print("Tablas encontradas en la base de datos:", tables)  # Agregar registro para depuración
    tables = [table[0] for table in tables]
    assert "authors" in tables
    assert "quotes" in tables
    assert "tags" in tables
    assert "quote_tags" in tables

def test_insert_data(database):
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
    database.insert_data(quotes, authors)
    
    database.cursor.execute("SELECT COUNT(*) FROM authors")
    assert database.cursor.fetchone()[0] == 1
    
    database.cursor.execute("SELECT COUNT(*) FROM quotes")
    assert database.cursor.fetchone()[0] == 1
    
    database.cursor.execute("SELECT COUNT(*) FROM tags")
    assert database.cursor.fetchone()[0] == 2

def test_get_author_id(database):
    # Primero, insertamos un autor
    author_name = "Albert Einstein"
    about = "Físico teórico alemán."
    about_link = "https://quotes.toscrape.com//author/Albert-Einstein"
    
    # Primero, intentamos obtener el ID del autor
    author_id = database.get_author_id(author_name)
    
    if author_id is None:
        # Si el autor no existe, lo insertamos
        database.cursor.execute("INSERT INTO authors (name, about, about_link) VALUES (?, ?, ?)", 
                                (author_name, about, about_link))
        database.connection.commit()
        author_id = database.get_author_id(author_name)
    
        assert author_id is not None

def test_get_tag_id(database):
    # Primero, insertamos un tag
    database.cursor.execute("INSERT INTO tags (name) VALUES (?)", ("vida",))
    database.connection.commit()

    tag_name = "vida"
    tag_id = database.get_tag_id(tag_name)
    assert tag_id is not None

    # Intentar obtener un tag que no existe
    non_existent_tag = database.get_tag_id("non_existent_tag")
    assert non_existent_tag is None
    
def test_insertion(database):
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