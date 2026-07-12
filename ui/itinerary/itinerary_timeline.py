"""
Itinerary Timeline
VITA 3.0
"""

import streamlit as st


def render_itinerary(state):

    st.subheader("🗓️ Travel Timeline")

    itinerary = state.itinerary

    if itinerary is None:

        st.info("No itinerary generated.")

        return

    if len(itinerary.days) == 0:

        st.info("No itinerary available.")

        return

    for day in itinerary.days:

        with st.expander(

            f"Day {day.day} • {day.city}",

            expanded=(day.day == 1)

        ):

            if day.hotel:

                st.success(f"🏨 Hotel: {day.hotel}")

            if day.weather:

                st.caption(f"🌤️ {day.weather}")

            if len(day.items) == 0:

                st.info("No activities planned.")

                continue

            for item in day.items:

                col1, col2 = st.columns([1, 5])

                with col1:

                    st.markdown(f"**{item.time}**")

                with col2:

                    st.markdown(f"**{item.title}**")

                    if item.location:

                        st.caption(item.location)

                    if item.duration:

                        st.caption(f"⏱ {item.duration}")

                    if item.estimated_cost:

                        st.caption(
                            f"💰 {item.estimated_cost}"
                        )

            st.divider()

            st.metric(

                "Estimated Cost",

                day.estimated_cost

            )
