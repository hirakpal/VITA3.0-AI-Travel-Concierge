"""
Conversation Manager
VITA 3.0

Main orchestrator.

Every user message first comes here.
"""

from __future__ import annotations

from models.response import AgentResponse

from agents.base_agent import BaseAgent


class ConversationManager(BaseAgent):

    def __init__(self):

        super().__init__("ConversationManager")

    # =====================================================
    # Main Router
    # =====================================================

    def run(

        self,

        state,

        message: str

    ) -> AgentResponse:

        # --------------------------------------------
        # Store user message
        # --------------------------------------------

        state.set_user_input(message)

        self.audit(

            state,

            "Received user message."

        )

        # --------------------------------------------
        # Guardrails
        # --------------------------------------------

        guard = self.validate(message)

        if not guard.success:

            return guard

        clean_text = guard.data.get(

            "clean_text",

            message

        )

        # --------------------------------------------
        # Determine Intent
        # --------------------------------------------

        route = self.detect_route(clean_text)

        state.metadata["route"] = route

        self.audit(

            state,

            f"Conversation routed to {route}"

        )

        # --------------------------------------------
        # Build response
        # --------------------------------------------

        if route == "DISCOVERY":

            reply = self.discovery_prompt(clean_text)

        elif route == "PLANNER":

            reply = self.planner_prompt(clean_text)

        elif route == "APPROVAL":

            reply = self.approval_prompt(clean_text)

        elif route == "MAP":

            reply = self.map_prompt(clean_text)

        else:

            reply = self.general_prompt(clean_text)

        # --------------------------------------------
        # Ask Gemini
        # --------------------------------------------

        answer = self.ask(

            self.system_prompt(),

            reply

        )

        state.set_assistant_response(answer)

        return self.success(

            answer,

            confidence=0.90,

            route=route

        )

    # =====================================================
    # Router
    # =====================================================

    def detect_route(

        self,

        text: str

    ) -> str:

        text = text.lower()

        # ---------------- Planner ----------------

        planner_keywords = [

            "plan",

            "itinerary",

            "schedule",

            "trip",

            "vacation",

            "holiday"

        ]

        if any(

            k in text

            for k in planner_keywords

        ):

            return "PLANNER"

        # ---------------- Approval ----------------

        if any(

            k in text

            for k in [

                "approve",

                "confirm",

                "book",

                "go ahead"

            ]

        ):

            return "APPROVAL"

        # ---------------- Map ----------------

        if any(

            k in text

            for k in [

                "map",

                "nearby",

                "around",

                "location",

                "city"

            ]

        ):

            return "MAP"

        # ---------------- Discovery ----------------

        if any(

            k in text

            for k in [

                "recommend",

                "suggest",

                "looking",

                "want",

                "love"

            ]

        ):

            return "DISCOVERY"

        return "CHAT"

    # =====================================================
    # System Prompt
    # =====================================================

    def system_prompt(self):

        return """

You are VITA.

A world-class AI Travel Concierge.

You freely converse with the traveller.

DO NOT immediately recommend.

Understand:

Mood

Purpose

Travel Style

Budget

Companions

Dream destinations

Conversation should feel natural.

Only ask ONE useful question at a time.

Never hallucinate.

"""

    # =====================================================
    # Prompt Builders
    # =====================================================

    def general_prompt(

        self,

        message

    ):

        return f"""

Traveller says

{message}

Continue the conversation naturally.

"""

    def discovery_prompt(

        self,

        message

    ):

        return f"""

Discover traveller preferences.

Conversation

{message}

Ask ONE useful follow-up question.

"""

    def planner_prompt(

        self,

        message

    ):

        return f"""

Traveller wants a trip.

Conversation

{message}

Understand remaining information before planning.

"""

    def approval_prompt(

        self,

        message

    ):

        return f"""

Traveller is responding to a proposed itinerary.

Conversation

{message}

Respond appropriately.

"""

    def map_prompt(

        self,

        message

    ):

        return f"""

Traveller is interacting with a map.

Conversation

{message}

Explain nearby places naturally.

"""
