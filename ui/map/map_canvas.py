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

    # Read HTML
    html = HTML_FILE.read_text(encoding="utf-8")

    # Inject API Key from Streamlit Secrets
    api_key = st.secrets.get("GOOGLE_MAPS_API_KEY", "")

    if not api_key:
        st.error("GOOGLE_MAPS_API_KEY not found in Streamlit Secrets.")
        return

    html = html.replace(
        "YOUR_GOOGLE_MAPS_API_KEY",
        api_key
    )

    components.html(
        html,
        height=550,
        scrolling=False,
    )

    st.divider()

    st.subheader("📍 Selected Destinations")

    destinations = getattr(state, "destinations", [])

    if not destinations:
        st.info("No destinations selected yet.")
        return

    for d in destinations:

        if isinstance(d, dict):

            st.container(border=True)

            st.write(f"**{d.get('city','Unknown')}**")

            st.caption(d.get("country",""))

            st.write(
                f"{d.get('lat','')} , {d.get('lng','')}"
            )

        else:

            st.container(border=True)

            st.write(f"**{d.city}**")

            st.caption(d.country)

            st.write(
                f"{d.coordinates.latitude} , {d.coordinates.longitude}"
            )
