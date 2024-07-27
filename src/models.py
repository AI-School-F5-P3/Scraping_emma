import logging
class Quote:
    """
    Representa una cita extraída de la web.

    Attributes:
        text (str): El texto de la cita.
        author (str): El autor de la cita.
        tags (list): Lista de etiquetas asociadas a la cita.
        author_about_link (str): Enlace a la biografía del autor.
    """
    def __init__(self, text, author, tags, author_about_link):
        self.text = text
        self.author = author
        self.tags = tags
        self.author_about_link = author_about_link
        logging.info(f"Quote creada: {self.text[:30]}... por {self.author}")

class Author:
    """
    Representa un autor de las citas.

    Attributes:
        name (str): El nombre del autor.
        about (str): La biografía del autor.
        about_link (str): Enlace a la biografía del autor.
    """
    def __init__(self, name, about, about_link):
        self.name = name
        self.about = about
        self.about_link = about_link
        logging.info(f"Autor creado: {self.name}")