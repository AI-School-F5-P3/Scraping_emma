import pytest
from src.database import Database
from src.models import Quote, Author
from config.config import DB_CONFIG
import logging

@pytest.fixture
def database():
    db = Database()
    db.clean_database()  # Llama a la función clean_database antes de cada prueba
    yield db
    db.clean_database()  # Asegura que la base de datos esté limpia después de cada prueba
    db.close()

def test_create_tables(database):
    # Verifica que las tablas existan
    
#   database.create_tables()
#   database.cursor.execute("SHOW TABLES")
#   tables = database.cursor.fetchall()
#   assert len(tables) == 4  # authors, quotes, tags, quote_tags
    database.create_tables()
    database.cursor.execute("SHOW TABLES")
    tables = database.cursor.fetchall()
    print("Tablas encontradas en la base de datos:", tables)  # Agregar registro para depuración
    tables = [table[0] for table in tables]
    assert "authors" in tables
    assert "quotes" in tables
    assert "tags" in tables
    assert "quote_tags" in tables

def test_insert_data(database):
    authors = {
        "Albert Einstein": Author("Albert Einstein", "Físico teórico alemán."),
    }
    quotes = [
        Quote("La vida es como andar en bicicleta. Para mantener el equilibrio, debes seguir moviéndote.", "Albert Einstein", ["vida", "movimiento"])
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
    database.cursor.execute("INSERT INTO authors (name, bio) VALUES (%s, %s)", ("Albert Einstein", "Físico teórico alemán."))
    database.connection.commit()

    author_name = "Albert Einstein"
    author_id = database.get_author_id(author_name)
    assert author_id is not None

    # Intentar obtener un autor que no existe
    non_existent_author = database.get_author_id("Non Existent Author")
    assert non_existent_author is None

def test_get_tag_id(database):
    # Primero, insertamos un tag
    database.cursor.execute("INSERT INTO tags (name) VALUES (%s)", ("vida",))
    database.connection.commit()

    tag_name = "vida"
    tag_id = database.get_tag_id(tag_name)
    assert tag_id is not None

    # Intentar obtener un tag que no existe
    non_existent_tag = database.get_tag_id("non_existent_tag")
    assert non_existent_tag is None