"""
Planner Agent
VITA 3.0

Responsible for:

✓ Build itinerary
✓ Reflection
✓ Governance
✓ Trip Validation
✓ Confidence
✓ Approval Gate
"""

from __future__ import annotations

import json
import re

from agents.base_agent import BaseAgent
from models.itinerary import (
    Itinerary,
    DayPlan,
    ItineraryItem,
)


class PlannerAgent(BaseAgent):

    def __init__(self):

        super().__init__("PlannerAgent")

    # ===========================================================
    # Main
    # ===========================================================

    def run(self, state, **kwargs):

        traveller = state.traveller

        if traveller.confidence < 0.80:

            return self.failure(
                "Traveller profile is incomplete."
            )

        prompt = f"""
You are an expert luxury travel planner.

Traveller

{traveller.model_dump_json(indent=2)}

Create a travel itinerary.

Return ONLY JSON.

{{
"trip_name":"",
"days":[
    {{
      "day":1,
      "city":"",
      "hotel":"",
      "activities":[
      {{
         "time":"09:00",
         "title":"",
         "category":"",
         "location":"",
         "duration":"",
         "cost":0
      }}
      ]
    }}
]
}}
"""

        answer = self.ask(
            "Create optimized itinerary.",
            prompt
        )

        itinerary = self._parse_itinerary(answer)

        # ---------------------------------------
        # Reflection
        # ---------------------------------------

        reflection = self.llm.reflect(answer)

        # ---------------------------------------
        # Governance
        # ---------------------------------------

        governance = self._governance(itinerary)

        # ---------------------------------------
        # Validation
        # ---------------------------------------

        validation = self._validate(itinerary)

        itinerary.validation_score = validation

        itinerary.ai_confidence = min(
            traveller.confidence,
            validation
        )

        state.itinerary = itinerary

        response = self.success(

            "Itinerary created successfully.",

            confidence=itinerary.ai_confidence,

            itinerary=itinerary.model_dump()

        )

        response.reasoning = reflection

        response.validation_score = validation

        response.requires_approval = True

        self.audit(
            state,
            "Planner completed."
        )

        return response

    # ===========================================================
    # JSON
    # ===========================================================

    def _parse_itinerary(self, text):

        try:

            data = json.loads(text)

        except Exception:

            match = re.search(
                r"\{.*\}",
                text,
                re.DOTALL
            )

            if not match:

                return Itinerary()

            data = json.loads(match.group())

        itinerary = Itinerary()

        itinerary.trip_name = data.get(
            "trip_name",
            "My Trip"
        )

        for day_data in data.get("days", []):

            day = DayPlan()

            day.day = day_data.get("day", 1)

            day.city = day_data.get("city", "")

            day.hotel = day_data.get("hotel", "")

            for activity in day_data.get(
                "activities",
                []
            ):

                item = ItineraryItem(

                    time=activity.get("time", ""),

                    title=activity.get("title", ""),

                    category=activity.get(
                        "category",
                        ""
                    ),

                    location=activity.get(
                        "location",
                        ""
                    ),

                    duration=activity.get(
                        "duration",
                        ""
                    ),

                    estimated_cost=float(
                        activity.get(
                            "cost",
                            0
                        )
                    )

                )

                day.add_item(item)

            itinerary.add_day(day)

        return itinerary

    # ===========================================================
    # Reflection
    # ===========================================================

    def _governance(self, itinerary):

        score = 100

        if itinerary.total_days == 0:

            score -= 40

        if itinerary.total_budget <= 0:

            score -= 20

        return score

    # ===========================================================
    # Validation
    # ===========================================================

    def _validate(self, itinerary):

        score = 1.0

        if itinerary.total_days == 0:

            score -= 0.40

        if itinerary.total_budget == 0:

            score -= 0.10

        if len(itinerary.days) == 0:

            score -= 0.20

        if itinerary.total_locations == 0:

            score -= 0.20

        return round(max(score, 0.0), 2)
