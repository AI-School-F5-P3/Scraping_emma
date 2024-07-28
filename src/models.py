import logging
class Quote:
    """
    Representa una Frase extraída de la web.

    Attributes:
        text (str): El texto de la Frase.
        author (str): El autor de la Frase.
        tags (list): Lista de etiquetas asociadas a la Frase.
        author_about_link (str): Enlace a la biografía del autor.
    """
    def __init__(self, text, author, tags, author_about_link):
        self.text = text
        self.author = author
        self.tags = tags
        self.author_about_link = author_about_link
        logging.info(f"Frase creada: {self.text[:30]}... por {self.author}")

class Author:
    """
    Representa un autor de las Frases.

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