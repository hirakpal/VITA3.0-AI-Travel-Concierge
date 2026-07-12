"""
Memory Agent
VITA 3.0
"""

from __future__ import annotations

from agents.base_agent import BaseAgent


class MemoryAgent(BaseAgent):

    def __init__(self):
        super().__init__("MemoryAgent")

    def run(
        self,
        state,
        operation: str = "save",
        **kwargs
    ):

        operation = operation.lower()

        if operation == "save":

            self.memory.save_state(state)

            self.audit(
                state,
                "State saved."
            )

            return self.success(
                "Memory saved."
            )

        if operation == "reset":

            state.reset()

            self.memory.save_state(state)

            self.audit(
                state,
                "Memory reset."
            )

            return self.success(
                "Memory reset."
            )

        if operation == "summary":

            return self.success(
                "Memory summary.",
                summary=state.summary()
            )

        return self.failure(
            f"Unknown operation '{operation}'."
        )
