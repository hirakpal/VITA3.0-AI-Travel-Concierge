"""
Google Map Panel
VITA 3.0
"""

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


HTML_FILE = Path("assets/google_map.html")


def render_map_canvas(state):

    st.subheader("🗺️ Destination Explorer")

    if not HTML_FILE.exists():

        st.error("google_map.html not found.")

        return

    html = HTML_FILE.read_text(encoding="utf-8")

    components.html(
        html,
        height=520,
        scrolling=False,
    )

    st.divider()

    st.markdown("### Selected Destinations")

    if not state.destinations:

        st.info("No destinations selected yet.")

        return

    for destination in state.destinations:

        with st.container(border=True):

            if isinstance(destination, dict):

                st.markdown(
                    f"""
**📍 {destination.get('city','Unknown')}**

Country: {destination.get('country','')}

Latitude: {destination.get('lat','')}

Longitude: {destination.get('lng','')}
"""
                )

            else:

                st.markdown(
                    f"""
**📍 {destination.city}**

Country: {destination.country}

Latitude: {destination.coordinates.latitude}

Longitude: {destination.coordinates.longitude}
"""
                )
