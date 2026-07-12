"""
Trip Validator Panel
VITA 3.0
"""

import streamlit as st


def render_trip_validator(state):

    st.subheader("✅ Trip Validator")

    score = state.validation_score

    confidence = state.confidence

    st.metric(
        "Validation Score",
        f"{score*100:.0f}%"
    )

    st.metric(
        "AI Confidence",
        f"{confidence*100:.0f}%"
    )

    st.progress(score)

    st.divider()

    checks = [

        ("Traveller Profile", state.traveller.confidence >= 0.80),

        ("Destination Selected", len(state.destinations) > 0),

        ("Itinerary Created", len(state.itinerary.days) > 0),

        ("Recommendations", state.recommendations.total > 0),

    ]

    for title, status in checks:

        if status:

            st.success(f"✔ {title}")

        else:

            st.warning(f"⚠ {title}")

    st.divider()

    if score >= 0.80:

        st.success("Ready for Approval")

    else:

        st.error("Needs More Information")
