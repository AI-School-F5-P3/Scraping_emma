import pytest
from src.database import Database
from src.models import Quote, Author
from config.config import DB_CONFIG
import logging

@pytest.fixture
def database():
    db = Database(
        host="localhost",
        user="root",
        password="admin",
        database="quotes_db"
    )
    db.create_tables()
    yield db
    db.connection.close()
    
@pytest.fixture(autouse=True)
def clean_database(database):
    database.cursor.execute("DELETE FROM quote_tags")
    database.cursor.execute("DELETE FROM quotes")
    database.cursor.execute("DELETE FROM authors")
    database.cursor.execute("DELETE FROM tags")
    database.connection.commit()

def test_create_tables(database):
    # Verifica que las tablas existan
    database.cursor.execute("SHOW TABLES")
    tables = database.cursor.fetchall()
    assert len(tables) == 4  # authors, quotes, tags, quote_tags

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