"""
Travel Memory
VITA 3.0

Stores conversation, Travel DNA and previous trips.
"""

from __future__ import annotations

from typing import Dict, List

from state.vita_state import VitaState


class TravelMemory:

    def __init__(self):

        self._sessions: Dict[str, VitaState] = {}

    # -----------------------------------------------------
    # Session
    # -----------------------------------------------------

    def create_session(self, session_id: str) -> VitaState:

        state = VitaState(session_id=session_id)

        self._sessions[session_id] = state

        return state

    def get(self, session_id: str) -> VitaState | None:

        return self._sessions.get(session_id)

    def exists(self, session_id: str) -> bool:

        return session_id in self._sessions

    def delete(self, session_id: str):

        if session_id in self._sessions:

            del self._sessions[session_id]

    # -----------------------------------------------------
    # Conversation
    # -----------------------------------------------------

    def add_user_message(

        self,

        session_id: str,

        message: str

    ):

        state = self.get(session_id)

        if not state:

            return

        state.set_user_input(message)

    def add_ai_message(

        self,

        session_id: str,

        message: str

    ):

        state = self.get(session_id)

        if not state:

            return

        state.set_assistant_response(message)

    def conversation(

        self,

        session_id: str

    ) -> List[dict]:

        state = self.get(session_id)

        if not state:

            return []

        return state.conversation_history

    # -----------------------------------------------------
    # Travel DNA
    # -----------------------------------------------------

    def update_dna(

        self,

        session_id: str,

        interest: str

    ):

        state = self.get(session_id)

        if not state:

            return

        state.travel_dna.update_interest(interest)

    # -----------------------------------------------------
    # Audit
    # -----------------------------------------------------

    def add_audit(

        self,

        session_id: str,

        message: str

    ):

        state = self.get(session_id)

        if not state:

            return

        state.add_audit(message)

    # -----------------------------------------------------
    # Destinations
    # -----------------------------------------------------

    def add_destination(

        self,

        session_id: str,

        destination

    ):

        state = self.get(session_id)

        if not state:

            return

        state.add_destination(destination)

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    def summary(self, session_id: str):

        state = self.get(session_id)

        if not state:

            return {}

        return state.summary()

    # -----------------------------------------------------
    # Reset
    # -----------------------------------------------------

    def reset(self, session_id: str):

        state = self.get(session_id)

        if state:

            state.reset()

    # -----------------------------------------------------
    # All Sessions
    # -----------------------------------------------------

    def sessions(self):

        return list(self._sessions.keys())

    def count(self):

        return len(self._sessions)
