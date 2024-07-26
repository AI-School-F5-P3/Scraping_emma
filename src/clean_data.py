import re
from html import unescape

from src.models import Author, Quote

def clean_text(text):
    """
    Limpia el texto eliminando espacios extra, caracteres especiales y decodificando entidades HTML.
    """
    # Decodificar entidades HTML
    text = unescape(text)
    # Eliminar espacios extra
    text = ' '.join(text.split())
    # Eliminar caracteres especiales, manteniendo puntuación básica
    text = re.sub(r'[^\w\s.,!?"-]', '', text)
    return text.strip()

def clean_author_name(name):
    """
    Limpia el nombre del autor, asegurándose de que esté en un formato consistente.
    """
    # Eliminar títulos comunes
    name = re.sub(r'^(Mr\.|Mrs\.|Ms\.|Dr\.|Prof\.)\s+', '', name)
    # Asegurarse de que cada palabra comience con mayúscula
    name = ' '.join(word.capitalize() for word in name.split())
    return clean_text(name)

def clean_tags(tags):
    """
    Limpia la lista de tags, eliminando duplicados y asegurando un formato consistente.
    """
    cleaned_tags = [clean_text(tag.lower()) for tag in tags]
    return list(set(cleaned_tags))  # Eliminar duplicados

def clean_url(url):
    """
    Asegura que la URL esté en un formato correcto.
    """
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    return url.strip()

def clean_data(quotes, authors):
    """
    Limpia todos los datos antes de la inserción en la base de datos.
    """
    cleaned_quotes = []
    cleaned_authors = {}

    for quote in quotes:
        cleaned_quote = Quote(
            text=clean_text(quote.text),
            author=clean_author_name(quote.author),
            tags=clean_tags(quote.tags),
            author_about_link=clean_url(quote.author_about_link)
        )
        cleaned_quotes.append(cleaned_quote)

    for author in authors:  # Cambiado de authors.items() a authors
        cleaned_author = Author(
            name=clean_author_name(author.name),
            about=clean_text(author.about),
            about_link=clean_url(author.about_link)
        )
        cleaned_authors[cleaned_author.name] = cleaned_author

    return cleaned_quotes, cleaned_authors