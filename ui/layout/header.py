import streamlit as st


def render_header():

    c1,c2,c3,c4,c5,c6,c7 = st.columns([3,1,1,1,1,1,1])

    with c1:
        st.title("🌍 VITA 3.0")

    with c2:
        st.button("➕ New Trip",use_container_width=True)

    with c3:
        st.button("📂 Saved",use_container_width=True)

    with c4:
        st.button("🔔",use_container_width=True)

    with c5:
        st.button("⚙️",use_container_width=True)

    with c6:
        st.button("👤",use_container_width=True)

    with c7:
        st.button("❓",use_container_width=True)

    st.divider()
