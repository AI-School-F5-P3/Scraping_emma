import streamlit as st
import logging
from src.database import Database
from config.config import DB_CONFIG

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Inicializando BBDD
try:
    db = Database(
        host='localhost',
        user='root',
        password='admin',
        database='quotes_db'
    )
except Exception as e:
    st.error(f"Error al inicializar la base de datos: {e}")
    logging.error(f"Error al inicializar la base de datos: {e}")

# Streamlit app layout
st.title("Buscador Frases")

# Inicializar el estado de la sesión si no existe
if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'selected_tag' not in st.session_state:
    st.session_state.selected_tag = None

# Funciones para cambiar el estado de la sesión
def set_page_tag_quotes(tag):
    st.session_state.page = 'tag_quotes'
    st.session_state.selected_tag = tag

def set_page_main():
    st.session_state.page = 'main'
    st.session_state.selected_tag = None

# Funciones para obtener datos de la base de datos
def fetch_all_authors():
    query = "SELECT * FROM authors"
    return db.fetch_all(query)

def fetch_author_by_id(author_id):
    query = "SELECT * FROM authors WHERE id = %s"
    return db.fetch_one(query, (author_id,))

def fetch_all_quotes():
    query = "SELECT * FROM quotes"
    return db.fetch_all(query)

def fetch_quote_by_id(quote_id):
    query = "SELECT * FROM quotes WHERE id = %s"
    return db.fetch_one(query, (quote_id,))

def fetch_quotes_by_author(author_id):
    query = "SELECT * FROM quotes WHERE author_id = %s"
    return db.fetch_all(query, (author_id,))

def fetch_tags_by_quote(quote_id):
    query = """
    SELECT tags.id, tags.name FROM tags
    JOIN quote_tags ON tags.id = quote_tags.tag_id
    WHERE quote_tags.quote_id = %s
    """
    return db.fetch_all(query, (quote_id,))

def fetch_quotes_by_tag(tag_id):
    query = """
    SELECT quotes.* FROM quotes
    JOIN quote_tags ON quotes.id = quote_tags.quote_id
    WHERE quote_tags.tag_id = %s
    """
    return db.fetch_all(query, (tag_id,))

def fetch_top_5_quotes():
    query = "SELECT * FROM quotes ORDER BY id DESC LIMIT 5"
    return db.fetch_all(query)

def fetch_top_5_authors():
    query = """
    SELECT authors.*, COUNT(quotes.id) as quote_count
    FROM authors
    LEFT JOIN quotes ON authors.id = quotes.author_id
    GROUP BY authors.id
    ORDER BY quote_count DESC
    LIMIT 5
    """
    return db.fetch_all(query)

def fetch_top_5_tags():
    query = """
    SELECT tags.*, COUNT(quote_tags.quote_id) as usage_count
    FROM tags
    LEFT JOIN quote_tags ON tags.id = quote_tags.tag_id
    GROUP BY tags.id
    ORDER BY usage_count DESC
    LIMIT 5
    """
    return db.fetch_all(query)

# Sidebar para navegación principal
main_menu = ["Lista Frases", "Frase","Lista Autores", "Autor",  "TOP 5"]
main_choice = st.sidebar.selectbox("Menu", main_menu)

# Función para mostrar frases por etiqueta
def show_quotes_by_tag(tag_id, tag_name):
    st.subheader(f"Frases con la etiqueta: {tag_name}")
    try:
        tag_quotes = fetch_quotes_by_tag(tag_id)
        for quote in tag_quotes:
            author = fetch_author_by_id(quote[2])
            author_name = author[1] if author else "Autor desconocido"
            st.markdown(f"**Frase:** '{quote[1]}'")
            st.markdown(f"**Autor:** {author_name}")
            st.markdown("---")
        if st.button("Volver a la lista de frases"):
            set_page_main()
            #st.rerun()
    except Exception as e:
        st.error(f"Error buscando frases por etiqueta: {e}")
        logging.error(f"Error buscando frases por etiqueta: {e}")
        
# Función para mostrar etiquetas como botones
def show_tag_buttons(tags, quote_id):
    tag_cols = st.columns(len(tags))
    for i, tag in enumerate(tags):
        if tag_cols[i].button(tag[1], key=f"tag_{quote_id}_{tag[0]}"):
            set_page_tag_quotes(tag)
            #st.rerun()
            
# Lógica principal de la aplicación
if st.session_state.page == 'tag_quotes':
    show_quotes_by_tag(st.session_state.selected_tag[0], st.session_state.selected_tag[1])
else:
    if main_choice == "Lista Frases":
        st.subheader("Lista Frases")
        try:
            quotes = fetch_all_quotes()
            quotes_per_page = 5
            total_quotes = len(quotes)    
            total_pages = (total_quotes + quotes_per_page - 1) // quotes_per_page
            selected_page = st.selectbox("Selecciona página", range(1, total_pages + 1))
            start = (selected_page - 1) * quotes_per_page
            end = start + quotes_per_page
        
            for quote in quotes[start:end]:
                author = fetch_author_by_id(quote[2])
                author_name = author[1] if author else "Autor desconocido"
                about_author = author[3] if author else ""
                tags = fetch_tags_by_quote(quote[0])
                
                st.markdown(f"**Frase:** '{quote[1]}'")
                st.markdown(f"**Autor:** {author_name} - [About]({about_author})")
                
                show_tag_buttons(tags, quote[0])
                
                st.markdown("---")

        except Exception as e:
            st.error(f"Error buscando Frases: {e}")
            logging.error(f"Error buscando Frases: {e}")

    elif main_choice == "Frase":
        st.subheader("Consultar Frase")
        quote_id = st.number_input("Introduzca ID de Frase", min_value=1)
        if st.button("Consultar Frase"):
            try:
                quote = fetch_quote_by_id(quote_id)
                if quote:
                    author = fetch_author_by_id(quote[2])
                    author_name = author[1] if author else "Autor desconocido"
                    about_author = author[3] if author else ""
                    tags = fetch_tags_by_quote(quote_id)
                    
                    st.markdown(f"**Frase:** '{quote[1]}'")
                    st.markdown(f"**Autor:** {author_name} - [About]({about_author})")
                    
                    tag_list = ", ".join([tag[1] for tag in tags]) if tags else "Sin etiquetas"
                    st.markdown(f"**Etiquetas:** {tag_list}")
                    
                    st.markdown("---")                
                else:
                    st.warning("No se encontró ninguna Frase con este ID")
            except Exception as e:
                st.error(f"Error buscando Frase: {e}")
                logging.error(f"Error buscando Frase: {e}")
                
    elif main_choice == "Lista Autores":
        st.subheader("Lista de Autores")
        try:
            authors = fetch_all_authors()
            authors_per_page = 5
            total_authors = len(authors)
            total_pages = (total_authors + authors_per_page - 1) // authors_per_page
            selected_page = st.selectbox("Selecciona página", range(1, total_pages + 1))
            start = (selected_page - 1) * authors_per_page
            end = start + authors_per_page
        
            for author in authors[start:end]:
                st.markdown(f"**Autor:** {author[1]} - [About]({author[3]})")
                #st.write(f"Nombre: {author[1]}, About: {author[3]}")
        except Exception as e:
            st.error(f"Error buscando autores: {e}")
            logging.error(f"Error buscando autores: {e}")

    elif main_choice == "Autor":
        st.subheader("Consultar Autor")
        author_id = st.number_input("Introduzca ID de Autor", min_value=1)
        if st.button("Consultar Autor"):
            try:
                author = fetch_author_by_id(author_id)
                if author:
                    st.markdown(f"**Autor:** {author[1]} - [About]({author[3]})")
                else:
                    st.warning("No se ha encontrado ningún autor con este ID")
            except Exception as e:
                st.error(f"Error buscando autor: {e}")
                logging.error(f"Error buscando autor: {e}")
                
    elif main_choice == "TOP 5":
        top5_menu = ["Frases", "Autores", "Etiquetas"]
        top5_choice = st.sidebar.selectbox("Selecciona una opción de TOP 5", top5_menu)
    
        if top5_choice == "Frases":
            st.subheader("TOP 5 Frases")
            try:
                top_quotes = fetch_top_5_quotes()
                for quote in top_quotes:
                    author = fetch_author_by_id(quote[2])
                    author_name = author[1] if author else "Autor desconocido"
                    st.markdown(f"**Frase:** '{quote[1]}'")
                    st.markdown(f"**Autor:** {author_name}")
                    st.markdown("---")
            except Exception as e:
                st.error(f"Error buscando TOP 5 Frases: {e}")
                logging.error(f"Error buscando TOP 5 Frases: {e}")

        elif top5_choice == "Autores":
            st.subheader("TOP 5 Autores")
            try:
                top_authors = fetch_top_5_authors()
                for author in top_authors:
                    st.markdown(f"**Autor:** {author[1]}")
                    st.markdown(f"**Número de frases:** {author[4]}")
                    st.markdown("---")
            except Exception as e:
                st.error(f"Error buscando TOP 5 Autores: {e}")
                logging.error(f"Error buscando TOP 5 Autores: {e}")

        elif top5_choice == "Etiquetas":
            st.subheader("TOP 5 Etiquetas")
            try:
                top_tags = fetch_top_5_tags()
                for tag in top_tags:
                    st.markdown(f"**Etiqueta:** {tag[1]}")
                    st.markdown(f"**Número de usos:** {tag[2]}")
                    st.markdown("---")
            except Exception as e:
                st.error(f"Error buscando TOP 5 Etiquetas: {e}")
                logging.error(f"Error buscando TOP 5 Etiquetas: {e}")    