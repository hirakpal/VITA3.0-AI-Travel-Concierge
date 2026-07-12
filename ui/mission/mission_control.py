"""
ui/mission/mission_control.py
VITA 3.0
"""

import streamlit as st


def render_mission_control(state):
    """
    Mission Control Panel
    """

    st.subheader("🎯 Mission Control")

    # ------------------------------------
    # Current Agent
    # ------------------------------------

    current_agent = getattr(
        state,
        "current_agent",
        "Conversation Agent"
    )

    current_stage = getattr(
        state,
        "current_stage",
        "Conversation"
    )

    confidence = getattr(
        state,
        "confidence",
        0.0
    )

    progress = getattr(
        state,
        "progress",
        0.0
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Current Agent",
            current_agent
        )

    with col2:

        st.metric(
            "Confidence",
            f"{confidence*100:.0f}%"
        )

    st.divider()

    st.write("### Workflow Stage")

    st.info(current_stage)

    st.divider()

    st.write("### Mission Progress")

    st.progress(progress)

    st.caption(f"{progress*100:.0f}% Complete")

    st.divider()

    st.write("### Workflow")

    stages = [

        "Conversation",

        "Discovery",

        "Map",

        "Planner",

        "Recommendation",

        "Approval"

    ]

    for stage in stages:

        if stage == current_stage:

            st.success(f"🟢 {stage}")

        else:

            st.write(f"⚪ {stage}")

    st.divider()

    approved = getattr(state, "approved", False)

    if approved:

        st.success("✅ Trip Approved")

    else:

        st.warning("⏳ Awaiting Traveller Approval")
