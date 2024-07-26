import mysql.connector
from mysql.connector import Error
import logging

from src.models import Author, Quote

class Database:
    def __init__(self, host, user, password, database):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print("Conectado a la base de datos MySQL")
        except Error as e:
            print(f"Error al conectarse a MySQL: {e}")

    def create_tables(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS authors (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) UNIQUE,
                    about TEXT,
                    about_link VARCHAR(255)
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS quotes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    text VARCHAR(1000),
                    author_id INT,
                    UNIQUE KEY unique_text (text(255)),
                    FOREIGN KEY (author_id) REFERENCES authors(id)
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS tags (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) UNIQUE
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS quote_tags (
                    quote_id INT,
                    tag_id INT,
                    FOREIGN KEY (quote_id) REFERENCES quotes(id),
                    FOREIGN KEY (tag_id) REFERENCES tags(id)
                )
            """)
            self.connection.commit()
            logging.info("Tablas creadas con éxito")
        except Error as e:
            logging.error(f"Error creando tablas: {str(e)}")
            raise

    def insert_data(self, quotes, authors):
        try:
            for author_name, author in authors.items():
                if isinstance(author, Author):  # Asegúrate de que 'author' es una instancia de Author

                        self.cursor.execute("""
                        INSERT INTO authors (name, about, about_link)
                        VALUES (%s, %s, %s)
                        ON DUPLICATE KEY UPDATE about = VALUES(about), about_link = VALUES(about_link)
                        """, (author.name, author.about, author.about_link))
                        self.connection.commit()
                else:
                    logging.error(f"El autor {author_name} no es una instancia de Author: {author}")

            for quote in quotes:
                if isinstance(quote, Quote):  # Asegúrate de que 'quote' es una instancia de Quote
                    author_id = self.get_author_id(quote.author)
                    if author_id:
                        self.cursor.execute("""
                        INSERT INTO quotes (text, author_id)
                        VALUES (%s, %s)
                        ON DUPLICATE KEY UPDATE author_id = VALUES(author_id)
                        """, (quote.text, author_id))
                        quote_id = self.cursor.lastrowid
                        
                        for tag in quote.tags:
                            tag_id = self.get_or_create_tag(tag)
                            self.cursor.execute("""
                            INSERT INTO quote_tags (quote_id, tag_id)
                            VALUES (%s, %s)
                            """, (quote_id, tag_id))
                    else:
                        logging.warning(f"No se encontró el autor {quote.author} para la cita.")
                else:
                    logging.error(f"La cita {quote} no es una instancia de Quote: {quote}")
            
            self.connection.commit()
            logging.info("Datos insertados con éxito")
        except Error as e:
            logging.error(f"Error insertando datos: {e}")
            self.connection.rollback()
            raise
        
    def get_author_id(self, author_name):
        try:
            self.cursor.execute("SELECT id FROM authors WHERE name = %s", (author_name,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Error as e:
            logging.error(f"Error obteniendo el ID del autor: {e}")
            return None

    def get_or_create_tag(self, tag_name):
        self.cursor.execute("SELECT id FROM tags WHERE name = %s", (tag_name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            self.cursor.execute("INSERT INTO tags (name) VALUES (%s)", (tag_name,))
            return self.cursor.lastrowid

    def close(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            logging.info("Conexión a la base de datos cerrada")