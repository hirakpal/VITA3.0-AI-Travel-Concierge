"""
Travel DNA Model
VITA 3.0

Learns user travel behaviour over time.
"""

from __future__ import annotations

from typing import Dict, List

from pydantic import BaseModel, Field, ConfigDict


class TravelDNA(BaseModel):

    model_config = ConfigDict(
        validate_assignment=True,
        extra="ignore"
    )

    # -------------------------------------------------
    # Budget
    # -------------------------------------------------

    budget_level: str = "Medium"

    average_trip_budget: float = 0.0

    preferred_currency: str = "USD"

    # -------------------------------------------------
    # Travel Style
    # -------------------------------------------------

    travel_style: str = ""

    travel_pace: str = "Balanced"

    # -------------------------------------------------
    # Interests
    # -------------------------------------------------

    interests: List[str] = Field(default_factory=list)

    favourite_foods: List[str] = Field(default_factory=list)

    favourite_activities: List[str] = Field(default_factory=list)

    # -------------------------------------------------
    # Preferences
    # -------------------------------------------------

    preferred_hotel_rating: int = 4

    preferred_airline: str = ""

    preferred_transport: str = ""

    walking_tolerance_km: float = 3.0

    # -------------------------------------------------
    # Behaviour Scores (0-100)
    # -------------------------------------------------

    adventure: int = 50

    luxury: int = 50

    food: int = 50

    shopping: int = 50

    nightlife: int = 50

    culture: int = 50

    nature: int = 50

    photography: int = 50

    family: int = 50

    relaxation: int = 50

    # -------------------------------------------------
    # Learning
    # -------------------------------------------------

    accepted_recommendations: int = 0

    rejected_recommendations: int = 0

    trips_completed: int = 0

    trust_score: float = 0.50

    # -------------------------------------------------
    # Helper Methods
    # -------------------------------------------------

    def learn_from_accept(self):

        self.accepted_recommendations += 1

        self.update_trust()

    def learn_from_reject(self):

        self.rejected_recommendations += 1

        self.update_trust()

    def complete_trip(self):

        self.trips_completed += 1

    def update_trust(self):

        total = (

            self.accepted_recommendations +

            self.rejected_recommendations

        )

        if total == 0:

            self.trust_score = 0.50

            return

        self.trust_score = round(

            self.accepted_recommendations / total,

            2

        )

    def update_interest(

        self,

        interest: str,

        score: int = 5

    ):

        mapping = {

            "Adventure": "adventure",

            "Luxury": "luxury",

            "Food": "food",

            "Shopping": "shopping",

            "Nightlife": "nightlife",

            "Culture": "culture",

            "Nature": "nature",

            "Photography": "photography",

            "Family": "family",

            "Relaxation": "relaxation"

        }

        attr = mapping.get(interest.strip().title())

        if attr is None:

            return

        value = getattr(self, attr)

        value = min(100, value + score)

        setattr(self, attr, value)

    @property
    def profile_completion(self):

        score = 0

        if self.travel_style:

            score += 20

        if self.interests:

            score += 20

        if self.favourite_foods:

            score += 20

        if self.preferred_transport:

            score += 20

        if self.preferred_airline:

            score += 20

        return score

    def dashboard(self):

        return {

            "Adventure": self.adventure,

            "Luxury": self.luxury,

            "Food": self.food,

            "Shopping": self.shopping,

            "Nature": self.nature,

            "Photography": self.photography,

            "Relaxation": self.relaxation,

            "Trust": self.trust_score

        }

    def summary(self):

        return {

            "budget": self.budget_level,

            "style": self.travel_style,

            "pace": self.travel_pace,

            "trust": self.trust_score,

            "completed_trips": self.trips_completed

        }

    def reset(self):

        self.__dict__.update(

            TravelDNA().model_dump()

        )
