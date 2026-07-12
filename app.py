import streamlit as st

# --------------------------------------------------
# Theme
# --------------------------------------------------

from ui.layout.theme import apply_theme
from ui.layout.header import render_header
from ui.layout.layout import render_layout

# --------------------------------------------------
# Workflow
# --------------------------------------------------

from graph.workflow import workflow

# --------------------------------------------------
# UI Panels
# --------------------------------------------------

from ui.chat.chat_panel import render_chat_panel
from ui.map.map_canvas import render_map_canvas
from ui.map.destination_panel import render_destination_panel
from ui.recommendations.recommendation_cards import render_recommendation_cards
from ui.itinerary.itinerary_timeline import render_itinerary
from ui.travel_dna.travel_dna import render_travel_dna
from ui.validator.trip_validator_panel import render_trip_validator
from ui.audit.audit_dashboard import render_audit_dashboard
from ui.mission.mission_control import render_mission_control

# ======================================================
# PAGE
# ======================================================

st.set_page_config(
    page_title="VITA 3.0",
    layout="wide",
    initial_sidebar_state="collapsed"
)

load_theme()

# ======================================================
# SESSION
# ======================================================

if "session_id" not in st.session_state:

    st.session_state.session_id = "demo"

if "state" not in st.session_state:

    st.session_state.state = workflow.run(
        session_id="demo",
        message="Hello"
    )

# ======================================================
# HEADER
# ======================================================

render_header()

# ======================================================
# LAYOUT
# ======================================================

layout = create_layout()

state = st.session_state.state

# ======================================================
# CHAT
# ======================================================

with layout["chat"]:

    prompt = render_chat_panel(state)

    if prompt:

        state = workflow.run(

            session_id=st.session_state.session_id,

            message=prompt

        )

        st.session_state.state = state

        st.rerun()

# ======================================================
# MAP
# ======================================================

with layout["map"]:

    render_map_canvas(state)

# ======================================================
# MISSION
# ======================================================

with layout["mission"]:

    render_mission_control(state)

# ======================================================
# DESTINATIONS
# ======================================================

with layout["destinations"]:

    render_destination_panel(state)

# ======================================================
# RECOMMENDATIONS
# ======================================================

with layout["recommendations"]:

    render_recommendation_cards(state)

# ======================================================
# TRAVEL DNA
# ======================================================

with layout["travel_dna"]:

    render_travel_dna(state)

# ======================================================
# TIMELINE
# ======================================================

with layout["timeline"]:

    render_itinerary(state)

# ======================================================
# VALIDATOR
# ======================================================

with layout["validator"]:

    render_trip_validator(state)

# ======================================================
# AUDIT
# ======================================================

with layout["audit"]:

    render_audit_dashboard(state)
