"""
Approval Agent
VITA 3.0

Responsible for:

✓ Approve
✓ Reject
✓ Replan
✓ Update Travel DNA
✓ Finalize Trip
"""

from __future__ import annotations

from agents.base_agent import BaseAgent


class ApprovalAgent(BaseAgent):

    def __init__(self):
        super().__init__("ApprovalAgent")

    # ==========================================================
    # Main
    # ==========================================================

    # ==========================================================
    # Execute (LangGraph Entry Point)
    # ==========================================================
    def execute(self, state):
        """
        LangGraph entry point.
        Determines the traveller's decision from the latest message
        and delegates to run().
        """
        message = (state.user_input or "").lower().strip()
        comments = state.user_input
        decision = self._extract_decision(message)

        result = self.run(
            state=state,
            decision=decision,
            comments=comments
        )

        # Update workflow state for the UI
        state.current_agent = "Approval Agent"
        state.current_stage = "Approval"
        state.progress = 1.0

        if hasattr(state, "assistant_response"):
            state.assistant_response = result.message

        return state

    # ==========================================================
    # Decision Extraction
    # ==========================================================
    def _extract_decision(self, message: str) -> str:
        if any(word in message for word in [
            "approve", "approved", "yes", "confirm",
            "looks good", "perfect", "ok", "okay"
        ]):
            return "approve"

        if any(word in message for word in [
            "reject", "no", "cancel"
        ]):
            return "reject"

        if any(word in message for word in [
            "replan", "change", "modify", "different", "another"
        ]):
            return "replan"

        if any(word in message for word in [
            "edit", "update"
        ]):
            return "edit"

        return "edit"

    def run(self, state, decision: str, comments: str = ""):
        decision = decision.lower().strip()

        # -----------------------------------------------------
        # APPROVE
        # -----------------------------------------------------
        if decision == "approve":
            state.approve()
            state.itinerary.approve()
            state.travel_dna.learn_from_accept()
            state.travel_dna.complete_trip()

            self.audit(state, "Traveller approved itinerary.")

            return self.success(
                "Trip approved successfully.",
                confidence=1.0,
                decision="APPROVED"
            )

        # -----------------------------------------------------
        # REJECT
        # -----------------------------------------------------
        elif decision == "reject":
            state.reject()
            state.travel_dna.learn_from_reject()

            self.audit(state, "Traveller rejected itinerary.")

            return self.success(
                "Trip rejected.",
                confidence=1.0,
                decision="REJECTED"
            )

        # -----------------------------------------------------
        # REPLAN
        # -----------------------------------------------------
        elif decision == "replan":
            state.awaiting_approval = False
            state.approved = False
            state.rejected = False

            self.audit(state, "Traveller requested replan.")

            return self.success(
                "Planner should generate a new itinerary.",
                confidence=1.0,
                decision="REPLAN",
                comments=comments
            )

        # -----------------------------------------------------
        # EDIT
        # -----------------------------------------------------
        elif decision == "edit":
            state.awaiting_approval = False

            self.audit(state, "Traveller requested itinerary edit.")

            return self.success(
                "Traveller wants to edit itinerary.",
                confidence=1.0,
                decision="EDIT",
                comments=comments
            )

        # -----------------------------------------------------
        # UNKNOWN
        # -----------------------------------------------------
        return self.failure(
            f"Unknown decision '{decision}'."
        )
