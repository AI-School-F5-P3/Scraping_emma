import sqlite3
import mysql.connector
from mysql.connector import Error
import logging

from config.config import DB_CONFIG

#from src.models import Author, Quote

class Database:
    def __init__(self, host, user, password, database):
        if 'host' in DB_CONFIG:  # Check if using MySQL
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
        else:  # Using SQLite
            self.connection = sqlite3.connect(DB_CONFIG['database'])
    
    def clean_database(self):
        tables = ["quote_tags", "tags", "quotes", "authors"]
        self.execute_query("SET FOREIGN_KEY_CHECKS = 0")
        for table in tables:
            self.execute_query(f"TRUNCATE TABLE {table}")
        self.execute_query("SET FOREIGN_KEY_CHECKS = 1")
        logging.info("Se han limpiado todas las tablas")
        
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
        for author_name, author in authors.items():
            self.execute_query("""
                INSERT INTO authors (name, about, about_link)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE about = VALUES(about), about_link = VALUES(about_link)
            """, (author.name, author.about, author.about_link))

        for quote in quotes:
            author_id = self.fetch_one("SELECT id FROM authors WHERE name = %s", (quote.author,))[0]
            if author_id:
                self.cursor.execute("""
                INSERT IGNORE INTO quotes (text, author_id)
                VALUES (%s, %s)
                """, (quote.text, author_id))
                quote_id = self.cursor.lastrowid
                
                
                for tag in quote.tags:
                    self.execute_query("INSERT IGNORE INTO tags (name) VALUES (%s)", (tag,))
                    tag_id = self.fetch_one("SELECT id FROM tags WHERE name = %s", (tag,))[0]
                    self.execute_query("INSERT IGNORE INTO quote_tags (quote_id, tag_id) VALUES (%s, %s)", (quote_id, tag_id))
            else:
                logging.warning(f"No se encontró el autor {quote.author} para la cita.")
            
            self.connection.commit()
            logging.info("Datos insertados con éxito")

        logging.info("Datos insertados con éxito")

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

    def get_tag_id(self, tag_name):
        query = "SELECT id FROM tags WHERE name = %s"
        result = self.fetch_one(query, (tag_name,))
        return result[0] if result else None
    
    def fetch_one(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchone()
    
    def execute_query(self, query, params=None):
        self.cursor.execute(query, params or ())
        self.connection.commit()
        
    def close(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            logging.info("Conexión a la base de datos cerrada")