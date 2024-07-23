class Quote:
    """
    Representa una cita extraída de la web.

    Attributes:
        text (str): El texto de la cita.
        author (str): El autor de la cita.
        tags (list): Lista de etiquetas asociadas a la cita.
    """

    def __init__(self, text, author, tags):
        self.text = text
        self.author = author
        self.tags = tags


class Author:
    """
    Representa un autor de citas.

    Attributes:
        name (str): El nombre del autor.
        bio (str): La biografía del autor.
    """

    def __init__(self, name, bio):
        self.name = name
        self.bio = bio