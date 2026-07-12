"""
VITA 3.0 Theme

Global styling for the application.
"""

import streamlit as st


PRIMARY = "#3B82F6"
SUCCESS = "#22C55E"
WARNING = "#F59E0B"
ERROR = "#EF4444"

BACKGROUND = "#0B1220"
CARD = "#141D2E"
CARD_HOVER = "#1C2942"
BORDER = "#24324B"

TEXT = "#F8FAFC"
TEXT_SECONDARY = "#94A3B8"


def apply_theme():

    st.markdown(
        f"""
<style>

/* ---------------------------------------------------
General
----------------------------------------------------*/

html, body, [class*="css"] {{

    font-family:
        Inter,
        Segoe UI,
        sans-serif;

}}

body {{

    background:{BACKGROUND};

    color:{TEXT};

}}

.main .block-container {{

    padding-top:1rem;

    padding-left:1.2rem;

    padding-right:1.2rem;

    padding-bottom:1rem;

    max-width:100%;

}}

/* Hide Streamlit UI */

header{{visibility:hidden;}}

footer{{visibility:hidden;}}

#MainMenu{{visibility:hidden;}}

div[data-testid="stToolbar"]{{display:none;}}

/* ---------------------------------------------------
Buttons
----------------------------------------------------*/

.stButton>button{{

    width:100%;

    border-radius:12px;

    border:1px solid {BORDER};

    background:{CARD};

    color:{TEXT};

    height:46px;

    transition:.25s;

}}

.stButton>button:hover{{

    border-color:{PRIMARY};

    background:{CARD_HOVER};

    color:white;

}}

/* ---------------------------------------------------
Text Input
----------------------------------------------------*/

.stTextInput input{{

    border-radius:12px;

    border:1px solid {BORDER};

    background:{CARD};

    color:white;

}}

textarea{{

    border-radius:12px;

}}

/* ---------------------------------------------------
Cards
----------------------------------------------------*/

.vita-card{{

    background:{CARD};

    border:1px solid {BORDER};

    border-radius:18px;

    padding:18px;

    box-shadow:
        0 4px 12px rgba(0,0,0,.18);

    margin-bottom:15px;

}}

.vita-card:hover{{

    border-color:{PRIMARY};

    transition:.25s;

}}

.vita-title{{

    font-size:22px;

    font-weight:700;

    color:{TEXT};

    margin-bottom:15px;

}}

.vita-subtitle{{

    color:{TEXT_SECONDARY};

    font-size:14px;

}}

.metric{{

    font-size:28px;

    font-weight:700;

}}

.badge-success{{

    background:{SUCCESS};

    color:white;

    padding:5px 12px;

    border-radius:50px;

    font-size:12px;

}}

.badge-warning{{

    background:{WARNING};

    color:white;

    padding:5px 12px;

    border-radius:50px;

    font-size:12px;

}}

.badge-error{{

    background:{ERROR};

    color:white;

    padding:5px 12px;

    border-radius:50px;

    font-size:12px;

}}

/* ---------------------------------------------------
Tabs
----------------------------------------------------*/

.stTabs [role="tab"]{{

    background:{CARD};

    border-radius:10px;

    margin-right:6px;

}}

.stTabs [aria-selected="true"]{{

    background:{PRIMARY};

    color:white;

}}

/* ---------------------------------------------------
Progress
----------------------------------------------------*/

.stProgress > div > div > div {{

    background:{PRIMARY};

}}

/* ---------------------------------------------------
Scrollbar
----------------------------------------------------*/

::-webkit-scrollbar{{

    width:8px;

}}

::-webkit-scrollbar-thumb{{

    background:#374151;

    border-radius:20px;

}}

::-webkit-scrollbar-track{{

    background:{BACKGROUND};

}}

</style>
""",
        unsafe_allow_html=True,
    )


def card(title: str):

    st.markdown(
        f"""
<div class="vita-card">

<div class="vita-title">{title}</div>

""",
        unsafe_allow_html=True,
    )


def end_card():

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


def section(title: str, icon: str = ""):

    st.markdown(
        f"""
<div class="vita-title">
{icon} {title}
</div>
""",
        unsafe_allow_html=True,
    )
# Alias so old code continues working
def load_theme():
    apply_theme()
