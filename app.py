from ui.layout.theme import apply_theme
from ui.layout.header import render_header
from ui.layout.sidebar import render_sidebar
from ui.layout.layout import render_layout

apply_theme()

render_header()

render_sidebar()

layout = render_layout()

with layout["chat"]:
    st.info("Chat")

with layout["map"]:
    st.info("Map")

with layout["mission"]:
    st.info("Mission Control")

with layout["recommendations"]:
    st.info("Recommendation Cards")

with layout["travel_dna"]:
    st.info("Travel DNA")

with layout["timeline"]:
    st.info("Timeline")

with layout["validator"]:
    st.info("Trip Validator")

with layout["audit"]:
    st.info("Audit Dashboard")
