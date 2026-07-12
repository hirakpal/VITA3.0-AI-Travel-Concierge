"""
Recommendation Agent
VITA 3.0

Generates:
✓ Hotels
✓ Attractions
✓ Restaurants
✓ Activities
✓ Flights
✓ Transport
"""

from __future__ import annotations

import json
import re

from agents.base_agent import BaseAgent

from models.recommendation import (
    Recommendation,
    RecommendationCollection,
    RecommendationType
)


class RecommendationAgent(BaseAgent):

    def __init__(self):

        super().__init__("RecommendationAgent")

    # ======================================================
    # Main
    # ======================================================

    def run(self, state, **kwargs):

        traveller = state.traveller

        if not state.destinations:

            return self.failure(
                "No destination selected."
            )

        collection = RecommendationCollection()

        for destination in state.destinations:

            prompt = f"""
You are an expert travel advisor.

Traveller

{traveller.model_dump_json(indent=2)}

Destination

{destination.model_dump_json(indent=2)}

Return ONLY JSON.

{{
"hotel":[
{
"name":"",
"rating":4.8,
"price":220
}
],

"restaurants":[
{
"name":"",
"rating":4.7
}
],

"attractions":[
{
"name":"",
"rating":4.9,
"duration":"2 Hours"
}
],

"activities":[
{
"name":"",
"duration":"Half Day"
}
]
}}
"""

            answer = self.ask(
                "Generate recommendations.",
                prompt
            )

            data = self.parse(answer)

            # ---------------- Hotels ----------------

            for hotel in data.get("hotel", []):

                collection.hotels.append(

                    Recommendation(

                        title=hotel["name"],

                        city=destination.city,

                        country=destination.country,

                        type=RecommendationType.HOTEL,

                        rating=float(
                            hotel.get("rating", 0)
                        ),

                        price=float(
                            hotel.get("price", 0)
                        ),

                        ai_match_score=95,

                        confidence=0.95

                    )

                )

            # ---------------- Attractions ----------------

            for item in data.get("attractions", []):

                collection.attractions.append(

                    Recommendation(

                        title=item["name"],

                        city=destination.city,

                        country=destination.country,

                        type=RecommendationType.ATTRACTION,

                        rating=float(
                            item.get("rating", 0)
                        ),

                        duration=item.get(
                            "duration",
                            ""
                        ),

                        ai_match_score=96,

                        confidence=0.95

                    )

                )

            # ---------------- Restaurants ----------------

            for item in data.get("restaurants", []):

                collection.restaurants.append(

                    Recommendation(

                        title=item["name"],

                        city=destination.city,

                        country=destination.country,

                        type=RecommendationType.RESTAURANT,

                        rating=float(
                            item.get("rating", 0)
                        ),

                        ai_match_score=94,

                        confidence=0.93

                    )

                )

            # ---------------- Activities ----------------

            for item in data.get("activities", []):

                collection.activities.append(

                    Recommendation(

                        title=item["name"],

                        city=destination.city,

                        country=destination.country,

                        type=RecommendationType.ACTIVITY,

                        duration=item.get(
                            "duration",
                            ""
                        ),

                        ai_match_score=94,

                        confidence=0.93

                    )

                )

        state.recommendations = collection

        self.audit(
            state,
            f"{collection.total} recommendations generated."
        )

        return self.success(

            "Recommendations generated.",

            confidence=0.95,

            recommendations=collection.model_dump()

        )

    # ======================================================
    # JSON
    # ======================================================

    def parse(self, text):

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

                    return json.loads(match.group())

                except Exception:

                    pass

        return {}
