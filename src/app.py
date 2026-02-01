import streamlit as st

from views.summary import summary_view
from views.add_stats import add_stats_view
from views.add_money import add_aportacion_view
from views.add_jornada import add_jornada_view
from views.juegos_view import juegos_view

st.set_page_config(page_title="Player Dashboard", layout="wide")

# -----------------------
# PASSWORD SETUP
# -----------------------
PASSWORD = "1234"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# -----------------------
# PASSWORD INPUT IF NOT AUTHENTICATED
# -----------------------
if not st.session_state.authenticated:
    st.sidebar.subheader("🔒 Enter password to unlock Add pages")
    pwd = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Submit"):
        if pwd == PASSWORD:
            st.session_state.authenticated = True
            st.sidebar.success("✅ Access granted")
        else:
            st.sidebar.error("❌ Incorrect password")

# -----------------------
# Sidebar navigation
# -----------------------
if st.session_state.authenticated:
    page_options = ["Alineacion", "Resumen", "Add Stats", "Add Aportaciones", "Add jornada"]
else:
    page_options = ["Alineacion", "Resumen"]  # only read-only pages

page = st.sidebar.selectbox("Navigate", page_options)

# -----------------------
# PAGE ROUTING
# -----------------------
if page == "Alineacion":
    juegos_view()
elif page == "Resumen":
    summary_view()
elif page == "Add Stats":
    add_stats_view()
elif page == "Add Aportaciones":
    add_aportacion_view()
elif page == "Add jornada":
    add_jornada_view()