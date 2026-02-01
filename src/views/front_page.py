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

    # -----------------------
    # PNG image
    # -----------------------
    try:
        # Load a PNG from local folder or static path
        img = Image.open("static/stadium.png")  # cambia a tu ruta
        with col2:
            st.image(img, use_column_width=True)
    except FileNotFoundError:
        st.info("Imagen de cancha no disponible.")

    # -----------------------
    # Optional: add cancha layout as a small preview
    # -----------------------
    # from views.juegos_view import draw_field_plotly
    # fig = draw_field_plotly()
    # st.plotly_chart(fig, use_container_width=True)