import mysql.connector
from mysql.connector import Error
import logging

class Database:
    """
    Clase para manejar las operaciones de la base de datos.

    Attributes:
        connection (mysql.connector.connection.MySQLConnection): Conexión a la base de datos MySQL.
        cursor (mysql.connector.cursor.MySQLCursor): Cursor para ejecutar queries SQL.
    """

    def __init__(self, host, user, password, database):
        """
        Inicializa la conexión a la base de datos.

        Args:
            host (str): Hostname del servidor MySQL.
            user (str): Nombre de usuario de MySQL.
            password (str): Contraseña de MySQL.
            database (str): Nombre de la base de datos.

        Raises:
            mysql.connector.Error: Si hay un problema al conectar con la base de datos.
        """
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

    def clean_database(self):
        try:
            # Desactivar la verificación de claves foráneas
            self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            
            # Lista de tablas a limpiar
            tables = ["quote_tags", "tags", "quotes", "authors"]
            
            for table in tables:
                self.cursor.execute(f"TRUNCATE TABLE {table}")
                print(f"Tabla {table} truncada con éxito")
            
            # Reactivar la verificación de claves foráneas
            self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            
            self.connection.commit()
            print("Se han limpiado todas las tablas")
            
        except Error as e:
            print(f"Error limpiando base de datos: {e}")
            # En caso de error, asegúrate de reactivar la verificación de claves foráneas
            self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            self.connection.rollback()

        
    def create_tables(self):
        """
        Crea las tablas necesarias en la base de datos si no existen.

        Raises:
            Exception: Si ocurre un error al crear las tablas.
        """
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS authors (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) UNIQUE,
                    about TEXT
                ) 
            """)
            logging.info("Tabla authors creada o ya existe.")
                        
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS quotes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    text VARCHAR(1000),
                    author_id INT,
                    UNIQUE KEY unique_text (text(255)),
                    FOREIGN KEY (author_id) REFERENCES authors(id)
                ) 
            """)
            logging.info("Tabla quotes creada o ya existe.")     
            
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS tags (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) UNIQUE
                ) 
            """)
            logging.info("Tabla tags creada o ya existe.")       

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS quote_tags (
                    quote_id INT,
                    tag_id INT,
                    FOREIGN KEY (quote_id) REFERENCES quotes(id),
                    FOREIGN KEY (tag_id) REFERENCES tags(id)
                ) 
            """)
            logging.info("Tabla quote_tags creada o ya existe.")   

            self.connection.commit()
            logging.info("Tablas creadas con éxito")
        except Error as e:
            logging.error(f"Error creando tablas: {str(e)}")
            raise
        
    def get_author_id(self, author_name):
        try:
            self.cursor.execute("SELECT id FROM authors WHERE name = %s", (author_name,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Error as e:
            logging.error(f"Error obteniendo el ID del autor: {e}")
            return None

    def get_tag_id(self, tag_name):
        try:
            self.cursor.execute("SELECT id FROM tags WHERE name = %s", (tag_name,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Error as e:
            logging.error(f"Error obteniendo el ID del tag: {e}")
            return None

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
                # Inserta autor si no existe
                try:
                    self.cursor.execute("""
                    INSERT INTO authors (name, about) 
                    VALUES (%s, %s) 
                    ON DUPLICATE KEY UPDATE about = VALUES(about)
                    """, (author.name, author.about))
                    logging.debug(f"Autor insertado/actualizado: {author.name}")                    
                    self.connection.commit()
                    
                    self.cursor.execute("SELECT id FROM authors WHERE name = %s", (author.name,))
                    result = self.cursor.fetchone()
                    if result:
                        author_id = result[0]
                    else:
                        logging.warning(f"No se pudo obtener el ID para el autor {author.name}")
                        continue
                except Error as e:
                    logging.error(f"Error insertando autor {author_name}: {e}")
                    continue

            for quote in quotes:
                try:
                    self.cursor.execute("SELECT id FROM authors WHERE name = %s", (quote.author,))
                    result = self.cursor.fetchone()
                    if result:
                        author_id = result[0]
                    else:
                        logging.warning(f"No se encontró el autor {quote.author} para la cita.")
                        continue

                    self.cursor.execute("SELECT id FROM quotes WHERE text = %s", (quote.text,))
                    existing_quote = self.cursor.fetchone()
                    if not existing_quote:
                        self.cursor.execute("INSERT INTO quotes (text, author_id) VALUES (%s, %s)", (quote.text, author_id))
                        quote_id = self.cursor.lastrowid

                        for tag in quote.tags:
                            self.cursor.execute("INSERT IGNORE INTO tags (name) VALUES (%s)", (tag,))
                            self.cursor.execute("SELECT id FROM tags WHERE name = %s", (tag,))
                            tag_id = self.cursor.fetchone()[0]
                            self.cursor.execute("INSERT INTO quote_tags (quote_id, tag_id) VALUES (%s, %s)", (quote_id, tag_id))
                            logging.debug(f"Cita insertada: {quote.text[:30]}...")
                            
                except Error as e:
                    logging.error(f"Error insertando cita: {e}")
                    continue

            self.connection.commit()
            logging.info("Datos insertados con éxito")
        except Error as e:
            logging.error(f"Error insertando datos: {e}")
            raise


    def close(self):
        """Cierra la conexión a la base de datos."""
        if hasattr(self, 'cursor') and self.cursor is not None:
            self.cursor.close()
        if hasattr(self, 'connection') and self.connection is not None:
            self.connection.close()
        logging.info("Conexión a la base de datos cerrada")