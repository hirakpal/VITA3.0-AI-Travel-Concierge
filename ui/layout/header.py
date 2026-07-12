import streamlit as st


def render_header():

    col1, col2 = st.columns([2, 8])

    with col1:

        st.markdown(
            """
            <div style="padding-top:10px;">
                <div style="font-size:42px;font-weight:800;color:white;">
                    🌍 VITA 3.0
                </div>

                <div style="color:#94A3B8;font-size:15px;">
                    Intelligent AI Travel Concierge
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        c1, c2, c3, c4 = st.columns([8, 1, 1, 1])

        with c1:
            st.text_input(
                "",
                placeholder="🔍 Search destination, city, attraction or country...",
                label_visibility="collapsed",
            )

        with c2:
            st.button("➕ Trip", use_container_width=True)

        with c3:
            st.button("🔔", use_container_width=True)

        with c4:
            st.button("👤", use_container_width=True)

    st.divider()
