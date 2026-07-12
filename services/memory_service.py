"""
Memory Service
VITA 3.0

Central interface for application memory.

All Agents interact with this service instead of
directly accessing TravelMemory.
"""

from __future__ import annotations

from typing import Optional

from memory.travel_memory import TravelMemory
from state.vita_state import VitaState
from models.destination import Destination


class MemoryService:

    def __init__(self):

        self.memory = TravelMemory()

    # ====================================================
    # Session
    # ====================================================

    def start_session(
        self,
        session_id: str
    ) -> VitaState:

        if self.memory.exists(session_id):

            return self.memory.get(session_id)

        return self.memory.create_session(session_id)

    def get_state(
        self,
        session_id: str
    ) -> Optional[VitaState]:

        return self.memory.get(session_id)

    def save_state(
        self,
        state: VitaState
    ):

        self.memory._sessions[state.session_id] = state

    # ====================================================
    # Conversation
    # ====================================================

    def add_user_message(
        self,
        session_id: str,
        message: str
    ):

        self.memory.add_user_message(
            session_id,
            message
        )

    def add_assistant_message(
        self,
        session_id: str,
        message: str
    ):

        self.memory.add_ai_message(
            session_id,
            message
        )

    # ====================================================
    # Travel DNA
    # ====================================================

    def learn_interest(
        self,
        session_id: str,
        interest: str
    ):

        self.memory.update_dna(
            session_id,
            interest
        )

    # ====================================================
    # Destination
    # ====================================================

    def add_destination(
        self,
        session_id: str,
        destination: Destination
    ):

        self.memory.add_destination(
            session_id,
            destination
        )

    # ====================================================
    # Audit
    # ====================================================

    def log(
        self,
        session_id: str,
        message: str
    ):

        self.memory.add_audit(
            session_id,
            message
        )

    # ====================================================
    # Summary
    # ====================================================

    def summary(
        self,
        session_id: str
    ):

        return self.memory.summary(session_id)

    # ====================================================
    # Reset
    # ====================================================

    def reset(
        self,
        session_id: str
    ):

        self.memory.reset(session_id)

    # ====================================================
    # Delete
    # ====================================================

    def delete(
        self,
        session_id: str
    ):

        self.memory.delete(session_id)


# --------------------------------------------------------
# Singleton
# --------------------------------------------------------

memory_service = MemoryService()
