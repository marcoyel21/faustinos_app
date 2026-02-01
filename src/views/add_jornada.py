import streamlit as st
from db import get_engine
from sqlalchemy import text

def add_jornada_view():
    st.title("📅 Add Jornada")

    engine = get_engine()

    # Obtener última jornada
    with engine.connect() as conn:
        last_jornada = conn.execute(
            text("SELECT COALESCE(MAX(jornada), 0) FROM juegos")
        ).scalar()

    next_jornada = last_jornada + 1

    st.info(f"📌 Jornada a crear: **{next_jornada}**")

    with st.form("add_jornada"):
        fecha = st.date_input("Fecha del partido")
        contrincante = st.text_input("Contrincante")

        st.subheader("🧩 Formación")

        defensa = st.selectbox("Defensa", [3, 4, 5])

        media_opciones = {
            "1-2": (1, 2),
            "2-1": (2, 1),
            "2-3": (2, 3),
            "4": (4,)
        }
        media_label = st.selectbox("Media", list(media_opciones.keys()))

        delantera = st.selectbox("Delantera", [1, 2, 3])

        goles_favor = st.number_input("Goles a favor", min_value=0)
        goles_contra = st.number_input("Goles en contra", min_value=0)

        submitted = st.form_submit_button("Guardar Jornada")

        if submitted:
            # Construir string de formación
            media_str = "-".join(map(str, media_opciones[media_label]))
            formacion = f"{defensa}-{media_str}-{delantera}"

            with engine.begin() as conn:
                conn.execute(
                    text("""
                        INSERT INTO juegos
                        (jornada, fecha, formacion, contrincante, goles_favor, goles_contra)
                        VALUES (:jornada, :fecha, :formacion, :contrincante, :gf, :gc)
                    """),
                    {
                        "jornada": next_jornada,
                        "fecha": fecha,
                        "formacion": formacion,
                        "contrincante": contrincante,
                        "gf": goles_favor,
                        "gc": goles_contra
                    }
                )

            st.success(f"✅ Jornada {next_jornada} creada con formación {formacion}")