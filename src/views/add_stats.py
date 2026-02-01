import streamlit as st
from sqlalchemy import text
from db import get_engine

# Mapas de formaciones → posiciones válidas
FORMATION_MAP = {
    "4-1-2-3": ["pt", "dfi", "dfc-i", "dfc-d", "dfd", "mcd", "mc-i", "mc-d", "ei", "dc", "ed"],
    "4-2-3-1": ["pt", "dfi", "dfc-i", "dfc-d", "dfd", "mcd-i", "mcd-d", "mi", "mc", "md", "dc"],
    "4-4-2":   ["pt", "dfi", "dfc-i", "dfc-d", "dfd", "mc-i", "mc-d", "mi", "md", "dc-i", "dc-d"],
}

def add_stats_view():
    st.title("✍️ Add Player Stats")

    engine = get_engine()

    # -----------------------
    # Load players & last jornada
    # -----------------------
    with engine.connect() as conn:
        players = conn.execute(text("SELECT id FROM players ORDER BY id")).mappings().all()
        last_jornada_row = conn.execute(text("SELECT MAX(jornada) AS jornada FROM juegos")).mappings().one()
        last_jornada = last_jornada_row["jornada"]

        # Cargar formación de la última jornada
        formacion_row = conn.execute(
            text("SELECT formacion FROM juegos WHERE jornada = :jornada"),
            {"jornada": last_jornada}
        ).mappings().one()
        formacion = formacion_row["formacion"]

    player_ids = [p["id"] for p in players]

    if not player_ids or last_jornada is None:
        st.error("❌ Players or jornadas not initialized")
        return

    # -----------------------
    # Posiciones válidas según la formación y no registradas aún
    # -----------------------
    valid_positions = set(FORMATION_MAP.get(formacion, []))

    with engine.connect() as conn:
        stats_taken = conn.execute(
            text("SELECT id, posicion FROM stats WHERE jornada = :jornada"),
            {"jornada": last_jornada}
        ).mappings().all()
    taken_positions = {(s["id"], s["posicion"]) for s in stats_taken}

    # -----------------------
    # Form
    # -----------------------
    with st.form("add_stats"):
        player_id = st.selectbox("Player ID", player_ids)
        jornada = st.number_input("Jornada", value=last_jornada, min_value=1, step=1)
        goles = st.number_input("Goles", min_value=0)
        asistencias = st.number_input("Asistencias", min_value=0)
        amarillas = st.number_input("Amarillas", min_value=0)
        rojas = st.number_input("Rojas", min_value=0)
        cambio = st.checkbox("Cambio")
        lesion = st.checkbox("Lesión 🩹")

        # Filtrar posiciones válidas que aún no tienen stats para este player y jornada
        remaining_positions = [p for p in valid_positions if (player_id, p) not in taken_positions]
        if not remaining_positions:
            st.info("✅ Este jugador ya tiene stats para todas las posiciones válidas de esta jornada")
            return

        posicion = st.selectbox("Posición", remaining_positions)

        submitted = st.form_submit_button("Guardar")

        if submitted:
            status = "cambio" if cambio else "inicial"

            # -----------------------
            # UPSERT: actualizar si existe, insertar si no
            # -----------------------
            query = text("""
                INSERT INTO stats
                (
                    id, jornada, gol, asistencia, amarillas, rojas, cambio, lesion, posicion, status
                )
                VALUES
                (
                    :id, :jornada, :gol, :asistencia, :amarillas, :rojas, :cambio, :lesion, :posicion, :status
                )
                ON CONFLICT(id, jornada, posicion) 
                DO UPDATE SET
                    gol = EXCLUDED.gol,
                    asistencia = EXCLUDED.asistencia,
                    amarillas = EXCLUDED.amarillas,
                    rojas = EXCLUDED.rojas,
                    cambio = EXCLUDED.cambio,
                    lesion = EXCLUDED.lesion,
                    status = EXCLUDED.status
            """)

            params = {
                "id": player_id,
                "jornada": jornada,
                "gol": goles,
                "asistencia": asistencias,
                "amarillas": amarillas,
                "rojas": rojas,
                "cambio": cambio,
                "lesion": lesion,
                "posicion": posicion,
                "status": status,
            }

            with engine.begin() as conn:
                conn.execute(query, params)

            st.success(f"Stats added/updated ✅ Player {player_id} at {posicion} as {status} for jornada {jornada}")