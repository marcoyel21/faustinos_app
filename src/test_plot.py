import streamlit as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

POSITION_COORDS = {"pt": (5,50), "dfi": (20,80), "dc": (75,50)}

def draw_field(ax):
    ax.set_facecolor("#2ecc71")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.plot([50,50],[0,100], color="white")
    ax.axis("off")

def juegos_view():
    st.title("⚽ Test Field")
    
    fig, ax = plt.subplots(figsize=(10,6))
    draw_field(ax)

    players = {"pt": "Portero", "dfi": "Defensa1", "dc": "Delantero"}
    
    for pos, name in players.items():
        x, y = POSITION_COORDS[pos]
        ax.scatter(x, y, s=300, color="blue", edgecolor="white", zorder=10)
        ax.text(x, y+2, name, color="white", ha="center", fontsize=12, weight="bold")
    
    st.pyplot(fig)  # dibuja el plot
    return  # <- nada se devuelve, se evita el '0'

juegos_view()