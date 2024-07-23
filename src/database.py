import mysql.connector
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
        """
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

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
                    bio TEXT
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
        except mysql.connector.Error as err:
            logging.error(f"Error creando tablas: {str(err)}")
            raise
        
    def get_author_id(self, author_name):
        try:
            self.cursor.execute("SELECT id FROM authors WHERE name = %s", (author_name,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as err:
            logging.error(f"Error obteniendo el ID del autor: {err}")
            return None

    def get_tag_id(self, tag_name):
        try:
            self.cursor.execute("SELECT id FROM tags WHERE name = %s", (tag_name,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as err:
            logging.error(f"Error obteniendo el ID del tag: {err}")
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
                    self.cursor.execute("INSERT IGNORE INTO authors (name, bio) VALUES (%s, %s)", (author.name, author.bio))
                    self.cursor.execute("SELECT id FROM authors WHERE name = %s", (author.name,))
                    author_id = self.cursor.fetchone()[0]
                except mysql.connector.Error as err:
                    logging.error(f"Error insertando autor {author_name}: {err}")
                    continue
                
            for quote in quotes:
                # Verificar si la cita ya existe
                    for tag in quote.tags:
                        # Inserta tag si no existe y obtiene su ID
                        try:
                            self.cursor.execute("SELECT id FROM authors WHERE name = %s", (quote.author,))
                            author_id = self.cursor.fetchone()[0]
                            
                            self.cursor.execute("SELECT id FROM quotes WHERE text = %s", (quote.text,))
                            existing_quote = self.cursor.fetchone()

                            if not existing_quote:
                                self.cursor.execute("INSERT INTO quotes (text, author_id) VALUES (%s, %s)", (quote.text, author_id))
                                quote_id = self.cursor.lastrowid

                                for tag in quote.tags:
                                    # Inserta tag si no existe y obtiene su ID
                                    self.cursor.execute("INSERT IGNORE INTO tags (name) VALUES (%s)", (tag,))
                                    self.cursor.execute("SELECT id FROM tags WHERE name = %s", (tag,))
                                    tag_id = self.cursor.fetchone()[0]
                                    self.cursor.execute("INSERT INTO quote_tags (quote_id, tag_id) VALUES (%s, %s)", (quote_id, tag_id))
                        except mysql.connector.Error as err:
                            logging.error(f"Error insertando cita: {err}")
                            continue
                        
            self.connection.commit()
            logging.info("Datos insertados con éxito")
        except mysql.connector.Error as err:
            logging.error(f"Error insertando datos: {err}")
            raise

    def close(self):
        """Cierra la conexión a la base de datos."""
        self.cursor.close()
        self.connection.close()
