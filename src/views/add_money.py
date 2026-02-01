import streamlit as st
from db import get_engine
import pandas as pd
from sqlalchemy import text

def add_aportacion_view():
    st.title("💰 Add Aportación")

    engine = get_engine()

    # 🔹 Cargar jugadores (solo id)
    with engine.connect() as conn:
        players = pd.read_sql(
            "SELECT id FROM players ORDER BY id",
            conn
        )

    if players.empty:
        st.warning("No players found")
        return

    player_ids = players["id"].tolist()

    # 🔹 Última jornada
    with engine.connect() as conn:
        last_jornada = conn.execute(
            text("SELECT MAX(jornada) FROM juegos")
        ).scalar()

    with st.form("add_aportacion"):
        player_id = st.selectbox(
            "Player",
            player_ids
        )

        jornada = st.number_input(
            "Jornada",
            min_value=1,
            value=last_jornada or 1,
            step=1
        )

        cantidad = st.number_input(
            "Cantidad",
            min_value=0,
            step=10
        )

        submitted = st.form_submit_button("Guardar")

        if submitted:
            with engine.begin() as conn:
                conn.execute(
                    text("""
                        INSERT INTO money (id, jornada, cantidad)
                        VALUES (:id, :jornada, :cantidad)
                    """),
                    {
                        "id": player_id,
                        "jornada": jornada,
                        "cantidad": cantidad
                    }
                )

            st.success("Aportación registrada ✅")