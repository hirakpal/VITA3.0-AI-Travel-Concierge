import streamlit as st


def apply_theme():

    st.set_page_config(
        page_title="VITA 3.0",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    st.markdown(
        """
        <style>

        .block-container{
            padding-top:1rem;
            padding-bottom:1rem;
            padding-left:1rem;
            padding-right:1rem;
        }

        div[data-testid="stToolbar"]{
            visibility:hidden;
        }

        header{
            visibility:hidden;
        }

        footer{
            visibility:hidden;
        }

        .panel{

            border:1px solid #E5E7EB;

            border-radius:14px;

            padding:15px;

            background:white;

            box-shadow:0 2px 8px rgba(0,0,0,.05);

        }

        .section-title{

            font-size:20px;

            font-weight:700;

            margin-bottom:15px;

        }

        </style>

        """,
        unsafe_allow_html=True
    )
