"""
Destination Panel
VITA 3.0
"""

import streamlit as st


def render_destination_panel(state):

    st.subheader("📍 Selected Destinations")

    if not state.destinations:

        st.info("No destinations selected.")

        return

    for index, destination in enumerate(state.destinations):

        with st.container(border=True):

            # Destination model
            if hasattr(destination, "city"):

                city = destination.city
                country = destination.country

                lat = getattr(
                    destination.coordinates,
                    "latitude",
                    0
                )

                lng = getattr(
                    destination.coordinates,
                    "longitude",
                    0
                )

            # Dictionary
            else:

                city = destination.get("city", "")

                country = destination.get("country", "")

                lat = destination.get("lat", 0)

                lng = destination.get("lng", 0)

            st.markdown(f"### 📍 {city}")

            st.caption(country)

            col1, col2 = st.columns(2)

            col1.metric("Latitude", f"{lat:.4f}")

            col2.metric("Longitude", f"{lng:.4f}")

            if st.button(
                "Remove",
                key=f"remove_{index}"
            ):

                state.destinations.pop(index)

                st.rerun()
