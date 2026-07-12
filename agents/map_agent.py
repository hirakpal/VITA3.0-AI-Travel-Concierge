"""
Map Agent
VITA 3.0
"""

from __future__ import annotations

from agents.base_agent import BaseAgent


class MapAgent(BaseAgent):

    def __init__(self):
        super().__init__("MapAgent")

    def run(
        self,
        state,
        **kwargs
    ):

        if not state.destinations:

            return self.failure(
                "No destination available to map."
            )

        destination = state.destinations[-1]

        destination.update_confidence()

        self.audit(
            state,
            f"Destination mapped: {destination.display_name}"
        )

        return self.success(
            "Destination mapped.",
            confidence=1.0,
            destination=destination.model_dump()
        )
