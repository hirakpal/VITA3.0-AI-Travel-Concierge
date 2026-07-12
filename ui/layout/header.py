"""
VITA 3.0 Header
Modern top navigation bar
"""

import streamlit as st


def render_header():

    left, center, right = st.columns([2.2, 4.6, 2.2])

    # --------------------------------------------------
    # Logo
    # --------------------------------------------------

    with left:

        st.markdown(
            """
            <div style="
                display:flex;
                align-items:center;
                gap:12px;
                margin-top:8px;
                margin-bottom:10px;
            ">
                <span style="font-size:42px;">🌍</span>

                <div>

                    <div style="
                        font-size:40px;
                        font-weight:800;
                        color:white;
                        line-height:1;
                    ">
                        VITA
                    </div>

                    <div style="
                        color:#94A3B8;
                        font-size:13px;
                    ">
                        Intelligent AI Travel Concierge
                    </div>

                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------
    # Search
    # --------------------------------------------------

    with center:

        st.markdown("<br>", unsafe_allow_html=True)

        st.text_input(
            "",
            placeholder="🔍 Search destination, city, attraction or country...",
            key="search_destination",
            label_visibility="collapsed",
        )

    # --------------------------------------------------
    # Right Menu
    # --------------------------------------------------

    with right:

        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.button(
                "➕ Trip",
                use_container_width=True,
                key="new_trip",
            )

        with c2:
            st.button(
                "💾",
                use_container_width=True,
                key="saved_trip",
            )

        with c3:
            st.button(
                "🔔",
                use_container_width=True,
                key="notification",
            )

        with c4:
            st.button(
                "👤",
                use_container_width=True,
                key="profile",
            )

    st.markdown(
        """
        <hr style="
            border:1px solid #24324B;
            margin-top:10px;
            margin-bottom:20px;
        ">
        """,
        unsafe_allow_html=True,
    )
