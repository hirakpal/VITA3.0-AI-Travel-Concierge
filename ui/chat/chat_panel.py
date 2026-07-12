import streamlit as st


def render_chat_panel():

    with st.container(border=True):

        st.markdown("## 💬 VITA")
        st.caption("Your Intelligent AI Travel Concierge")

        st.divider()

        # Welcome
        st.markdown("### 👋 Welcome")
        st.write(
            "Tell me where you'd like to travel, or click a place on the map."
        )

        st.divider()

        # Chat History
        if "messages" not in st.session_state:

            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content":
                    "Hi! I'm VITA. Where shall we travel today? 🌍"
                }
            ]

        for msg in st.session_state.messages:

            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # Suggested prompts
        st.markdown("### ✨ Suggested")

        c1, c2 = st.columns(2)

        with c1:

            st.button("🇯🇵 Japan")

            st.button("🏔 Switzerland")

            st.button("🌍 Europe")

        with c2:

            st.button("🏖 Beach Holiday")

            st.button("👨‍👩‍👧 Family Trip")

            st.button("💍 Honeymoon")

        st.divider()

        # Chat Input
        prompt = st.chat_input(
            "Ask VITA anything about your next trip..."
        )

        if prompt:

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": prompt
                }
            )

            with st.chat_message("user"):
                st.write(prompt)

            # Temporary Mock Response
            response = (
                "Thanks! 😊\n\n"
                "I'm analysing your travel request.\n\n"
                "Next we'll identify:\n"
                "- Destination\n"
                "- Budget\n"
                "- Travel style\n"
                "- Companions\n"
                "- Dates"
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response
                }
            )

            with st.chat_message("assistant"):

                with st.spinner("Thinking..."):

                    st.write(response)

            st.rerun()
