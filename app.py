import streamlit as st

from config.constants import APP_TITLE

st.set_page_config(
    page_title=APP_TITLE,
    layout="wide"
)

st.title(APP_TITLE)

st.info(
    "🚧 VITA 3.0 is being built step-by-step."
)
