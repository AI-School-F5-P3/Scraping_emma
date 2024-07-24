import streamlit as st
import pandas as pd
from src.database import Database
from config.config import DB_CONFIG
from src.updater import update_database

# Inicializar la conexión a la base de datos
db = Database(**DB_CONFIG)

def main():
    st.title("Gestor de Citas")

    menu = ["Listar todas las citas", "Buscar una cita", "Actualizar base de datos"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Listar todas las citas":
        st.subheader("Todas las Citas")
        quotes = db.list_quotes(limit=1000)  # Aumentamos el límite para obtener más citas
        if quotes:
            df = pd.DataFrame([(q.text, q.author, ', '.join(q.tags)) for q in quotes], 
                            columns=['Texto', 'Autor', 'Tags'])
            st.dataframe(df)
            
            csv = df.to_csv(index=False)
            st.download_button(
                label="Descargar como CSV",
                data=csv,
                file_name="todas_las_citas.csv",
                mime="text/csv",
            )
        else:
            st.write("No se encontraron citas.")

    elif choice == "Buscar una cita":
        st.subheader("Buscar una Cita")
        quote_id = st.number_input("ID de la cita", min_value=1, step=1)
        if st.button("Buscar"):
            quote = db.read_quote(quote_id)
            if quote:
                df = pd.DataFrame([{
                    'Texto': quote.text,
                    'Autor': quote.author,
                    'Tags': ', '.join(quote.tags)
                }])
                st.dataframe(df)
                
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Descargar como CSV",
                    data=csv,
                    file_name=f"cita_{quote_id}.csv",
                    mime="text/csv",
                )
            else:
                st.warning("Cita no encontrada")
                
    elif choice == "Actualizar base de datos":
        st.subheader("Actualizar Base de Datos")
        if st.button("Iniciar actualización"):
            with st.spinner('Actualizando la base de datos...'):
                try:
                    update_database()
                    st.success("Base de datos actualizada con éxito")
                except Exception as e:
                    st.error(f"Error al actualizar la base de datos: {str(e)}")
                    
if __name__ == "__main__":
    main()