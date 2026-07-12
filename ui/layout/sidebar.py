import streamlit as st


def render_sidebar():

    with st.expander("⚡ Quick Actions",expanded=True):

        st.button("New Trip",use_container_width=True)

        st.button("Load Trip",use_container_width=True)

        st.button("Travel DNA",use_container_width=True)

        st.button("Audit",use_container_width=True)

        st.button("Settings",use_container_width=True)
