import streamlit as st

# ---------------------------------------------------
# Theme
# ---------------------------------------------------

from ui.layout.theme import apply_theme
from ui.layout.header import render_header
from ui.layout.layout import render_layout

# ---------------------------------------------------
# Components
# ---------------------------------------------------

from ui.chat.chat_panel import render_chat_panel

# (Coming next)
# from ui.map.map_panel import render_map_panel
# from ui.mission.mission_control import render_mission_control
# from ui.recommendations.recommendation_panel import render_recommendation_panel
# from ui.travel_dna.travel_dna_panel import render_travel_dna_panel
# from ui.itinerary.itinerary_timeline import render_itinerary
# from ui.validator.trip_validator_panel import render_trip_validator
# from ui.audit.audit_panel import render_audit_panel


# ===================================================
# App Configuration
# ===================================================

apply_theme()

render_header()

layout = render_layout()


# ===================================================
# CHAT
# ===================================================

with layout["chat"]:

    render_chat_panel()


# ===================================================
# MAP
# ===================================================

with layout["map"]:

    st.info("🗺️ Interactive Map (Coming Next)")


# ===================================================
# MISSION CONTROL
# ===================================================

with layout["mission"]:

    st.info("🚀 Mission Control")


# ===================================================
# DESTINATIONS
# ===================================================

with layout["destinations"]:

    st.info("📍 Selected Destinations")


# ===================================================
# RECOMMENDATIONS
# ===================================================

with layout["recommendations"]:

    st.info("🏨 Recommendation Cards")


# ===================================================
# TRAVEL DNA
# ===================================================

with layout["travel_dna"]:

    st.info("🧬 Travel DNA")


# ===================================================
# ITINERARY
# ===================================================

with layout["timeline"]:

    st.info("📅 Itinerary Timeline")


# ===================================================
# VALIDATOR
# ===================================================

with layout["validator"]:

    st.info("✅ Trip Validator")


# ===================================================
# AUDIT
# ===================================================

with layout["audit"]:

    st.info("📋 Audit Dashboard")
