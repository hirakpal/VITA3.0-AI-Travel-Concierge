import streamlit as st


def render_layout():

    top_left,top_center,top_right = st.columns(
        [3,5,2]
    )

    bottom_left,bottom_right = st.columns(
        [7,3]
    )

    timeline,validator = st.columns(
        [7,3]
    )

    audit = st.container()

    return {

        "chat":top_left,

        "map":top_center,

        "mission":top_right,

        "recommendations":bottom_left,

        "travel_dna":bottom_right,

        "timeline":timeline,

        "validator":validator,

        "audit":audit

    }
