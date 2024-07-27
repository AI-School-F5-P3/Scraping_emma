import sqlite3
import mysql.connector
from mysql.connector import Error
import logging

class Database:
    """
    Clase para manejar las operaciones de la base de datos.

    Attributes:
        connection (mysql.connector.connection.MySQLConnection or sqlite3.Connection): Conexión a la base de datos.
        cursor (mysql.connector.cursor.MySQLCursor or sqlite3.Cursor): Cursor para ejecutar queries SQL.
        is_mysql (bool): Determina si la base de datos es MySQL o SQLite.
    """

    def __init__(self, **kwargs):
        self.config = kwargs
        self.connection = None
        self.cursor = None
        self.is_mysql = 'host' in kwargs  # Determina si es MySQL o SQLite
        self.connect() 

    def connect(self):
        """Establece la conexión a la base de datos MySQL o SQLite."""
        try:
            if self.is_mysql:
                self.connection = mysql.connector.connect(**self.config)
                if self.connection.is_connected():
                    self.cursor = self.connection.cursor()
                    logging.info("Conectado a la base de datos MySQL")
                else:
                    logging.error("No se pudo establecer la conexión a MySQL")
            else:
                self.connection = sqlite3.connect(self.config['database'])
                self.cursor = self.connection.cursor()
                logging.info("Conectado a la base de datos SQLite")
        except Error as e:
            logging.error(f"Error al conectarse a la base de datos: {e}")
            raise
        
    def create_tables(self):
        """
        Crea las tablas necesarias en la base de datos si no existen.

        Raises:
            Exception: Si ocurre un error al crear las tablas.
        """       
        try:
            if self.is_mysql:
                self._create_mysql_tables()
            else:
                self._create_sqlite_tables()
            self.connection.commit()
            logging.info("Tablas creadas con éxito")
        except Error as e:
            logging.error(f"Error creando tablas: {str(e)}")
            raise
        
    def _create_mysql_tables(self):
        """Crea las tablas necesarias en la base de datos MySQL."""
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
            logging.info("Tablas MySQL creadas con éxito")
        except Error as e:
            logging.error(f"Error creando tablas MySQL: {str(e)}")
            raise

    def _create_sqlite_tables(self):   
        """Crea las tablas necesarias en la base de datos SQLite."""
        try:
            self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS authors (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE,
                        about TEXT,
                        about_link TEXT
                    )
                """)
            self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS quotes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        text TEXT,
                        author_id INTEGER,
                        FOREIGN KEY (author_id) REFERENCES authors(id)
                    )
                """)
            self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tags (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE
                    )
                """)
            self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS quote_tags (
                        quote_id INTEGER,
                        tag_id INTEGER,
                        FOREIGN KEY (quote_id) REFERENCES quotes(id),
                        FOREIGN KEY (tag_id) REFERENCES tags(id)
                    )
                """)
            self.connection.commit()
            logging.info("Tablas SQLite creadas con éxito")
        except Error as e:
            logging.error(f"Error creando tablas SQLite: {str(e)}")
            raise
        
    def insert_data(self, quotes, authors):
        """
        Inserta los datos extraídos en la base de datos.

        Args:
            quotes (list): Lista de objetos Quote a insertar.
            authors (dict): Diccionario de objetos Author a insertar.

        Raises:
            Exception: Si ocurre un error al insertar los datos.
        """
        try:
            for author_name, author in authors.items():
                self._insert_author(author)

            for quote in quotes:
                self._insert_quote(quote)

            self.connection.commit()
            logging.info("Datos insertados con éxito")
        except Error as e:
            logging.error(f"Error al insertar datos: {str(e)}")
            self.connection.rollback()
            
    def _insert_author(self, author):
        """Inserta un autor en la base de datos si no existe."""    
        try:
            if self.is_mysql:
                query = """
                    INSERT INTO authors (name, about, about_link) 
                    VALUES (%s, %s, %s) 
                    ON DUPLICATE KEY UPDATE 
                    about = VALUES(about), about_link = VALUES(about_link)
                """
            else:
                query = """
                    INSERT OR REPLACE INTO authors (name, about, about_link)
                    VALUES (?, ?, ?)
                """
            self.cursor.execute(query, (author.name, author.about, author.about_link))
            logging.info(f"Autor insertado/actualizado: {author.name}")
        except Error as e:
            logging.error(f"Error al insertar autor {author.name}: {str(e)}")
            raise  
        
    def _insert_quote(self, quote):
        """Inserta una cita en la base de datos si no existe."""
        try:
            author_id = self.get_author_id(quote.author)
            if author_id:
                if self.is_mysql:
                    query = """
                        INSERT INTO quotes (text, author_id)
                        SELECT %s, %s
                        WHERE NOT EXISTS (
                            SELECT 1 FROM quotes
                            WHERE text = %s AND author_id = %s
                        )
                    """
                    self.cursor.execute(query, (quote.text, author_id, quote.text, author_id))
                else:
                    query = """
                        INSERT OR IGNORE INTO quotes (text, author_id)
                        VALUES (?, ?)
                    """
                    self.cursor.execute(query, (quote.text, author_id))
                quote_id = self.cursor.lastrowid
                if quote_id:
                    logging.info(f"Cita insertada: {quote.text[:30]}...")
                    for tag in quote.tags:
                        tag_id = self._insert_tag(tag)
                        self._insert_quote_tag(quote_id, tag_id)
                else:
                    logging.info(f"Cita ya existente: {quote.text[:30]}...")
            else:
                logging.warning(f"No se encontró el autor {quote.author} para la cita.")
        except Error as e:
            logging.error(f"Error al insertar cita: {str(e)}")
            raise
        
    def _insert_tag(self, tag):
        """Inserta una etiqueta en la base de datos si no existe."""
        try:
            if self.is_mysql:
                query = "INSERT IGNORE INTO tags (name) VALUES (%s)"
            else:
                query = "INSERT OR IGNORE INTO tags (name) VALUES (?)"
            self.cursor.execute(query, (tag,))
            self.connection.commit()
            return self.get_tag_id(tag)
        except Error as e:
            logging.error(f"Error al insertar tag {tag}: {str(e)}")
            raise
        
    def _insert_quote_tag(self, quote_id, tag_id):
        """Inserta la relación entre una cita y una etiqueta en la base de datos."""
        try:
            if self.is_mysql:
                query = "INSERT IGNORE INTO quote_tags (quote_id, tag_id) VALUES (%s, %s)"
            else:
                query = "INSERT OR IGNORE INTO quote_tags (quote_id, tag_id) VALUES (?, ?)"
            self.cursor.execute(query, (quote_id, tag_id))
            self.connection.commit()
            logging.info(f"Relación quote_tag insertada: quote_id={quote_id}, tag_id={tag_id}")
        except Error as e:
            logging.error(f"Error al insertar quote_tag: {str(e)}")
            raise

    def get_author_id(self, author_name):
        """Obtiene el ID de un autor por su nombre."""
        try:
            query = "SELECT id FROM authors WHERE name = ?" if not self.is_mysql else "SELECT id FROM authors WHERE name = %s"
            self.cursor.execute(query, (author_name,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Error as e:
            logging.error(f"Error obteniendo el ID del autor: {e}")
            return None

    def get_tag_id(self, tag_name):
        """Obtiene el ID de una etiqueta por su nombre."""
        try:
            query = "SELECT id FROM tags WHERE name = ?" if not self.is_mysql else "SELECT id FROM tags WHERE name = %s"
            self.cursor.execute(query, (tag_name,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Error as e:
            logging.error(f"Error obteniendo el ID del tag: {e}")
            return None    
            
    def fetch_one(self, query, params=None):
        """Ejecuta una consulta y retorna el primer resultado."""
        self.execute_query(query, params)
        return self.cursor.fetchone()
        
    def execute_query(self, query, params=None):
        """Ejecuta una consulta SQL."""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            logging.info(f"Consulta ejecutada: {query} con parámetros: {params}")
        except Error as e:
            logging.error(f"Error ejecutando la consulta: {e}")
            logging.error(f"Consulta: {query}")
            logging.error(f"Parámetros: {params}")
            raise
        
    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            logging.info("Conexión a la base de datos cerrada")