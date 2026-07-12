"""
Travel DNA Panel
VITA 3.0
"""

import streamlit as st


def render_travel_dna(state):

    st.subheader("🧬 Travel DNA")

    dna = state.travel_dna

    if dna is None:

        st.info("Travel DNA not available.")

        return

    st.metric("Trust Score", f"{dna.trust_score*100:.0f}%")

    st.progress(dna.trust_score)

    st.divider()

    scores = {

        "Adventure": dna.adventure,

        "Luxury": dna.luxury,

        "Food": dna.food,

        "Shopping": dna.shopping,

        "Nature": dna.nature,

        "Culture": dna.culture,

        "Photography": dna.photography,

        "Relaxation": dna.relaxation,

    }

    for name, value in scores.items():

        st.write(name)

        st.progress(value / 100)

    st.divider()

    st.caption("Travel Style")

    st.info(dna.travel_style or "Unknown")

    st.caption("Travel Pace")

    st.info(dna.travel_pace)

    st.caption("Budget")

    st.info(dna.budget_level)

    st.caption("Trips Completed")

    st.success(dna.trips_completed)
