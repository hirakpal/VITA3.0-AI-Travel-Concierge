"""
Discovery Agent
VITA 3.0

Responsible for understanding the traveller.

Extracts:
- Intent
- Mood
- Budget
- Travel Style
- Interests
- Companions
- Dates
- Destination

Updates Traveller + Travel DNA
"""

from __future__ import annotations

import json
import re

from agents.base_agent import BaseAgent
from models.destination import Destination
from models.response import AgentResponse


class DiscoveryAgent(BaseAgent):

    def __init__(self):

        super().__init__("DiscoveryAgent")

    # =====================================================
    # Main
    # =====================================================

    def execute(self, state):
        response = self.run(state)

        state.set_agent("Discovery Agent")
        state.set_step("Discovery")

        return state
    
    def run(
        self,
        state,
        **kwargs
    ) -> AgentResponse:

        conversation = "\n".join(

            f'{m["role"]}: {m["content"]}'

            for m in state.conversation_history[-20:]

        )

        prompt = f"""
You are an expert travel analyst.

Extract the traveller profile.

Return ONLY JSON.

{{
"name":"",
"purpose":"",
"destination":"",
"budget":0,
"currency":"USD",
"mood":"",
"travel_style":"",
"companions":"",
"interests":[],
"missing":[]
}}

Conversation

{conversation}
"""

        answer = self.ask(
            "You extract traveller profiles.",
            prompt
        )

        data = self._parse(answer)

        traveller = state.traveller

        traveller.trip_purpose = data.get(
            "purpose",
            traveller.trip_purpose
        )

        traveller.mood = data.get(
            "mood",
            traveller.mood
        )

        traveller.travel_style = data.get(
            "travel_style",
            traveller.travel_style
        )

        if data.get("budget"):

            traveller.budget = float(
                data["budget"]
            )

        traveller.currency = data.get(
            "currency",
            traveller.currency
        )

        interests = data.get(
            "interests",
            []
        )

        for interest in interests:

            if interest not in traveller.interests:

                traveller.interests.append(interest)

            state.travel_dna.update_interest(
                interest
            )

        destination_text = data.get("destination", "").strip()

        if destination_text and not state.destinations:

            parts = [
                p.strip()
                for p in destination_text.split(",")
                if p.strip()
            ]

            city = parts[0] if parts else destination_text
            country = parts[1] if len(parts) > 1 else ""

            destination = Destination(
                city=city,
                country=country
            )

            destination.update_confidence()

            state.add_destination(destination)

            self.audit(
                state,
                f"Destination identified: {destination.display_name}"
            )

        traveller.update_confidence()

        confidence = traveller.confidence

        missing = data.get(
            "missing",
            []
        )

        response = self.success(

            "Traveller profile updated.",

            confidence=confidence,

            traveller=traveller.model_dump(),

            missing_information=missing

        )

        response.validation_score = confidence

        state.set_response(response)

        self.audit(
            state,
            "Traveller profile extracted."
        )

        return response

    # =====================================================
    # JSON Parser
    # =====================================================

    def _parse(
        self,
        text: str
    ):

        try:

            return json.loads(text)

        except Exception:

            match = re.search(

                r"\{.*\}",

                text,

                re.DOTALL

            )

            if match:

                try:

                    return json.loads(

                        match.group()

                    )

                except Exception:

                    pass

        return {}
