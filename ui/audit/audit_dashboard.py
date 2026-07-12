"""
Audit Dashboard
VITA 3.0
"""

import streamlit as st


def render_audit_dashboard(state):

    st.subheader("📋 Audit Dashboard")

    logs = getattr(state, "audit_log", [])

    if not logs:

        st.info("No audit logs available.")

        return

    st.metric("Total Events", len(logs))

    st.divider()

    for log in reversed(logs[-20:]):

        st.code(log, language="text")
