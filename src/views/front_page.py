import streamlit as st
import pandas as pd
from sqlalchemy import text
from db import get_engine
from PIL import Image

def front_page_view():
    st.title("⚽ Próximo Partido")

    engine = get_engine()

    # -----------------------
    # Load next or last juego
    # -----------------------
    with engine.connect() as conn:
        # For example, get the next jornada with info
        juego = conn.execute(
            text("""
                SELECT jornada, contrincante, cancha, hora
                FROM juegos
                ORDER BY jornada DESC
                LIMIT 1
            """)
        ).mappings().first()

    if not juego:
        st.warning("No hay partidos registrados.")
        return

    # -----------------------
    # Contrincante arriba
    # -----------------------
    st.subheader(f"🆚 {juego['contrincante']}")

    # -----------------------
    # Cancha info + hora
    # -----------------------
    col1, col2 = st.columns([2, 3])
    with col1:
        st.markdown(f"**Cancha:** {juego['cancha']}")
        st.markdown(f"**Hora:** {juego['hora']}")

    # Image via URL
    image_url = "https://github.com/marcoyel21/faustinos_app/blob/069822f6a35afa863cddd72e0050e20de2c19e6a/canchas.jpg?raw=true"
    with col2:
        st.image(image_url, caption="Vista de la cancha", width=400)
