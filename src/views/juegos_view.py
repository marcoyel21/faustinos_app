import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import text
from db import get_engine

# =========================
# POSICIONES → COORDENADAS
# =========================
POSITION_COORDS = {
    "pt": (5, 50),
    "dfi": (20, 80), "df-i": (20, 60), "df-d": (20, 40), "dfd": (20, 20),
    "dfc-i": (20, 65), "dfc": (20, 50), "dfc-d": (20, 35),
    "mcd": (40, 50), "mcd-i": (40, 60), "mcd-d": (40, 40),
    "mc": (55, 50), "mc-i": (55, 60), "mc-d": (55, 40), "mi": (55, 70), "md": (55, 30),
    "dc": (75, 50), "dc-i": (75, 60), "dc-d": (75, 40), "ei": (75, 70), "ed": (75, 30),
}

# =========================
# DIBUJAR CANCHA CON PLOTLY
# =========================
def draw_field_plotly():
    fig = go.Figure()
    fig.update_layout(
        xaxis=dict(range=[0, 100], showgrid=False, showticklabels=False),
        yaxis=dict(range=[0, 100], showgrid=False, showticklabels=False, scaleanchor="x"),
        plot_bgcolor="#2ecc71",
        height=600,
        margin=dict(l=10, r=10, t=10, b=10)
    )

    # Línea media
    fig.add_shape(type="line", x0=50, y0=0, x1=50, y1=100, line=dict(color="white"))
    # Círculo central
    fig.add_shape(type="circle", x0=50-9.15, y0=50-9.15, x1=50+9.15, y1=50+9.15, line=dict(color="white"))
    # Áreas
    fig.add_shape(type="rect", x0=0, y0=20, x1=16, y1=80, line=dict(color="white"))
    fig.add_shape(type="rect", x0=84, y0=20, x1=100, y1=80, line=dict(color="white"))
    # Porterías
    fig.add_shape(type="line", x0=0, y0=45, x1=2, y1=45, line=dict(color="white"))
    fig.add_shape(type="line", x0=0, y0=55, x1=2, y1=55, line=dict(color="white"))
    fig.add_shape(type="line", x0=98, y0=45, x1=100, y1=45, line=dict(color="white"))
    fig.add_shape(type="line", x0=98, y0=55, x1=100, y1=55, line=dict(color="white"))
    return fig

# =========================
# VIEW COMPLETA
# =========================
def juegos_view():
    st.title("⚽ Jornada & Alineación")
    engine = get_engine()

    # 🔹 Cargar jornadas
    with engine.connect() as conn:
        juegos = pd.read_sql(
            "SELECT jornada, fecha, formacion, contrincante, goles_favor, goles_contra "
            "FROM juegos ORDER BY jornada DESC",
            conn,
        )

    if juegos.empty:
        st.warning("No hay juegos")
        return

    # 🔹 Selección de jornada
    jornada = st.selectbox("Jornada", juegos["jornada"])
    juego = juegos[juegos["jornada"] == jornada].iloc[0]

    st.subheader(
        f"🆚 {juego.contrincante} | {juego.goles_favor}-{juego.goles_contra} | Formación {juego.formacion}"
    )

    # 🔹 Stats de la jornada con número de player
    with engine.connect() as conn:
        stats = pd.read_sql(
            text("""
                SELECT s.id, s.posicion, s.gol, s.asistencia, s.amarillas, s.rojas, s.cambio, s.lesion,
                       s.status, p.number
                FROM stats s
                LEFT JOIN players p ON s.id = p.id
                WHERE s.jornada = :jornada
            """),
            conn,
            params={"jornada": jornada},
        )

    if stats.empty:
        st.info("No hay jugadores registrados para esta jornada")
        return

    # 🔹 Asegurarse que number sea int
    stats["number"] = stats["number"].fillna(0).astype(int)

    # 🔹 Crear figura limpia
    fig = draw_field_plotly()

    # 🔹 Filtrar solo jugadores iniciales
    iniciales = stats[stats["status"] == "inicial"].copy()

    for _, row in iniciales.iterrows():
        pos = row["posicion"]
        if not pos or pos.strip().lower() not in POSITION_COORDS:
            continue
        x, y = POSITION_COORDS[pos.strip().lower()]

        # Emojis
        emojis = "⚽"*row["gol"] + "🅰️"*row["asistencia"] + "🟨"*row["amarillas"] + "🟥"*row["rojas"] + "🤕"*row["lesion"]

        # 🔹 Texto con número centrado en círculo, saltos de línea y nombre/emoji grande
        text_label = f"{row['number']}\n\n{row['id']} {emojis}"

        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode="markers+text",
            marker=dict(size=40, color="blue", line=dict(color="white", width=2)),
            text=text_label,
            textposition="top center",
            textfont=dict(size=18, color="white", family="Arial Black"),
            showlegend=False,
            hoverinfo="skip"
        ))

    # 🔹 Renderizar pitch con key dinámica
    st.plotly_chart(fig, use_container_width=True, key=f"pitch_{jornada}")

    # 🔹 Cambios como bullets con número, emojis y posición
    st.divider()
    st.subheader("🔄 Cambios")
    cambios = stats[stats["status"] == "cambio"]
    for _, row in cambios.iterrows():
        emojis = ""
        if row["gol"]:
            emojis += "⚽"*row["gol"]
        if row["asistencia"]:
            emojis += "🅰️"*row["asistencia"]
        if row["amarillas"]:
            emojis += "🟨"*row["amarillas"]
        if row["rojas"]:
            emojis += "🟥"*row["rojas"]
        if row["lesion"]:
            emojis += "🤕"

        st.markdown(f"- **{row['number']} - {row['id']}** 🔄 ({row['posicion']}) {emojis}")