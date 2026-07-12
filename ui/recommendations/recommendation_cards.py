"""
Recommendation Cards
VITA 3.0
"""

import streamlit as st


def render_recommendation_cards(state):

    st.subheader("✨ AI Recommendations")

    recommendations = state.recommendations

    if recommendations is None:

        st.info("No recommendations yet.")

        return

    tabs = st.tabs(

        [

            "🏨 Hotels",

            "🍽 Restaurants",

            "🎯 Attractions",

            "🎉 Activities"

        ]

    )

    # -----------------------------------------------------

    with tabs[0]:

        hotels = recommendations.hotels

        if not hotels:

            st.info("No hotel recommendations.")

        for hotel in hotels:

            with st.container(border=True):

                st.markdown(f"### 🏨 {hotel.title}")

                st.caption(f"{hotel.city}, {hotel.country}")

                col1, col2 = st.columns(2)

                col1.metric("⭐ Rating", hotel.rating)

                col2.metric("💰 Price", hotel.price)

                st.progress(hotel.ai_match_score / 100)

    # -----------------------------------------------------

    with tabs[1]:

        restaurants = recommendations.restaurants

        if not restaurants:

            st.info("No restaurant recommendations.")

        for item in restaurants:

            with st.container(border=True):

                st.markdown(f"### 🍽 {item.title}")

                st.caption(f"{item.city}, {item.country}")

                st.metric(

                    "⭐ Rating",

                    item.rating

                )

    # -----------------------------------------------------

    with tabs[2]:

        attractions = recommendations.attractions

        if not attractions:

            st.info("No attractions.")

        for item in attractions:

            with st.container(border=True):

                st.markdown(f"### 📍 {item.title}")

                st.caption(item.duration)

                st.progress(item.ai_match_score / 100)

    # -----------------------------------------------------

    with tabs[3]:

        activities = recommendations.activities

        if not activities:

            st.info("No activities.")

        for item in activities:

            with st.container(border=True):

                st.markdown(f"### 🎉 {item.title}")

                st.caption(item.duration)
