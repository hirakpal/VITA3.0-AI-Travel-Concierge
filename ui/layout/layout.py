import streamlit as st


def render_layout():

    chat, map_panel, mission = st.columns([3, 5, 2])

    destinations, travel_dna = st.columns([7, 3])

    recommendations, validator = st.columns([7, 3])

    timeline = st.container()

    audit = st.container()

    return {

        "chat": chat,

        "map": map_panel,

        "mission": mission,

        "destinations": destinations,

        "travel_dna": travel_dna,

        "recommendations": recommendations,

        "validator": validator,

        "timeline": timeline,

        "audit": audit

    }
