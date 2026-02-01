import streamlit as st
import pandas as pd

from db import get_engine
from queries import SUMMARY_QUERY

def summary_view():
    st.title("📊 Player Summary")

    engine = get_engine()
    df = pd.read_sql(SUMMARY_QUERY, engine)

    st.dataframe(df, use_container_width=True)