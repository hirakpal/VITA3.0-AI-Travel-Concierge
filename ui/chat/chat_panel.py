"""
ui/chat/chat_panel.py
"""

import streamlit as st


def render_chat_panel(state):

    st.subheader("💬 VITA AI Travel Concierge")

    if "messages" not in st.session_state:

        st.session_state.messages = [

            {
                "role": "assistant",
                "content": "👋 Hello! I'm VITA. Where would you like to travel today?"
            }

        ]

    # -----------------------------
    # Chat History
    # -----------------------------

    history = st.container(height=500)

    with history:

        for msg in st.session_state.messages:

            if msg["role"] == "assistant":

                st.markdown(
                    f"""
<div style="
background:#1E293B;
padding:12px;
border-radius:12px;
margin-bottom:10px;
border-left:4px solid #3B82F6;
">
🤖 {msg['content']}
</div>
""",
                    unsafe_allow_html=True,
                )

            else:

                st.markdown(
                    f"""
<div style="
background:#334155;
padding:12px;
border-radius:12px;
margin-bottom:10px;
text-align:right;
border-right:4px solid #8B5CF6;
">
🧑 {msg['content']}
</div>
""",
                    unsafe_allow_html=True,
                )

    st.divider()

    # -----------------------------
    # Input
    # -----------------------------

    c1, c2 = st.columns([8, 1])

    with c1:

        prompt = st.text_input(
            "",
            placeholder="Ask VITA anything...",
            label_visibility="collapsed",
            key="vita_chat"
        )

    with c2:

        send = st.button(
            "➤",
            use_container_width=True,
            type="primary"
        )

    if send and prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        return prompt

    return None
