"""
Destination Model
VITA 3.0
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


class Coordinates(BaseModel):
    model_config = ConfigDict(extra="ignore")

    latitude: float = 0.0
    longitude: float = 0.0


class Stay(BaseModel):
    model_config = ConfigDict(extra="ignore")

    arrival_date: str = ""
    departure_date: str = ""
    nights: int = 0


class Destination(BaseModel):
    """
    Represents one city/country in a trip.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="ignore"
    )

    # ----------------------------------------
    # Identity
    # ----------------------------------------

    id: str = ""

    city: str = ""

    state: str = ""

    country: str = ""

    country_code: str = ""

    coordinates: Coordinates = Field(default_factory=Coordinates)

    # ----------------------------------------
    # Trip
    # ----------------------------------------

    stay: Stay = Field(default_factory=Stay)

    sequence: int = 1

    selected: bool = True

    # ----------------------------------------
    # Planner
    # ----------------------------------------

    hotel: Optional[str] = None

    attractions: List[str] = Field(default_factory=list)

    restaurants: List[str] = Field(default_factory=list)

    activities: List[str] = Field(default_factory=list)

    transport: List[str] = Field(default_factory=list)

    hidden_gems: List[str] = Field(default_factory=list)

    # ----------------------------------------
    # Context
    # ----------------------------------------

    weather: str = ""

    temperature: float = 0.0

    budget: float = 0.0

    notes: str = ""

    confidence: float = 0.0

    # ----------------------------------------
    # Helpers
    # ----------------------------------------

    @property
    def display_name(self):

        if self.country:
            return f"{self.city}, {self.country}"

        return self.city

    @property
    def total_places(self):

        return (
            len(self.attractions)
            + len(self.activities)
            + len(self.restaurants)
        )

    def update_confidence(self):

        score = 0

        if self.city:
            score += 20

        if self.country:
            score += 20

        if self.hotel:
            score += 20

        if self.attractions:
            score += 20

        if self.stay.nights > 0:
            score += 20

        self.confidence = round(score / 100, 2)

    def add_attraction(self, name: str):

        if name not in self.attractions:
            self.attractions.append(name)

    def add_restaurant(self, name: str):

        if name not in self.restaurants:
            self.restaurants.append(name)

    def add_activity(self, name: str):

        if name not in self.activities:
            self.activities.append(name)

    def summary(self):

        return {

            "destination": self.display_name,

            "hotel": self.hotel,

            "nights": self.stay.nights,

            "attractions": len(self.attractions),

            "restaurants": len(self.restaurants),

            "activities": len(self.activities),

            "confidence": self.confidence

        }
