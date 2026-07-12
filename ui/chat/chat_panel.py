"""
ui/chat/chat_panel.py
"""

import streamlit as st


def render_chat_panel(state):
    """
    Render the conversation panel.
    Returns the latest user prompt.
    """

    st.subheader("💬 VITA AI Travel Concierge")

    # -----------------------------------------
    # Initialise messages
    # -----------------------------------------

    if "messages" not in st.session_state:

        st.session_state.messages = [

            {

                "role": "assistant",

                "content": "👋 Hello! I'm VITA. Where would you like to travel?"

            }

        ]

    # -----------------------------------------
    # Render chat history
    # -----------------------------------------

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # -----------------------------------------
    # User Input
    # -----------------------------------------

    prompt = st.chat_input(
        "Ask VITA anything..."
    )

    if prompt:

        st.session_state.messages.append(

            {

                "role": "user",

                "content": prompt

            }

        )

        return prompt

    return None
