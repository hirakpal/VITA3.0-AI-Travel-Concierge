"""
Recommendation Models
VITA 3.0
"""

from __future__ import annotations

from enum import Enum
from typing import List

from pydantic import BaseModel, Field, ConfigDict


class RecommendationType(str, Enum):
    HOTEL = "HOTEL"
    ATTRACTION = "ATTRACTION"
    RESTAURANT = "RESTAURANT"
    FLIGHT = "FLIGHT"
    ACTIVITY = "ACTIVITY"
    TRANSPORT = "TRANSPORT"


class RecommendationStatus(str, Enum):
    SUGGESTED = "SUGGESTED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    REPLACED = "REPLACED"


class Recommendation(BaseModel):

    model_config = ConfigDict(
        validate_assignment=True,
        extra="ignore"
    )

    # ----------------------------------
    # Identity
    # ----------------------------------

    id: str = ""

    destination_id: str = ""

    type: RecommendationType = RecommendationType.ATTRACTION

    # ----------------------------------
    # Basic Info
    # ----------------------------------

    title: str = ""

    subtitle: str = ""

    description: str = ""

    image_url: str = ""

    # ----------------------------------
    # Location
    # ----------------------------------

    city: str = ""

    country: str = ""

    address: str = ""

    latitude: float = 0.0

    longitude: float = 0.0

    # ----------------------------------
    # Commercial
    # ----------------------------------

    price: float = 0.0

    currency: str = "USD"

    rating: float = 0.0

    review_count: int = 0

    duration: str = ""

    # ----------------------------------
    # AI
    # ----------------------------------

    ai_match_score: float = 0.0

    confidence: float = 0.0

    reasoning: str = ""

    tags: List[str] = Field(default_factory=list)

    alternatives: List[str] = Field(default_factory=list)

    # ----------------------------------
    # User
    # ----------------------------------

    status: RecommendationStatus = RecommendationStatus.SUGGESTED

    bookmarked: bool = False

    selected: bool = False

    # ----------------------------------
    # Helper Methods
    # ----------------------------------

    def accept(self):

        self.selected = True

        self.status = RecommendationStatus.ACCEPTED

    def reject(self):

        self.selected = False

        self.status = RecommendationStatus.REJECTED

    def replace(self, new_title: str):

        self.title = new_title

        self.status = RecommendationStatus.REPLACED

    def summary(self):

        return {

            "title": self.title,

            "type": self.type.value,

            "price": self.price,

            "rating": self.rating,

            "score": self.ai_match_score,

            "status": self.status.value

        }


class RecommendationCollection(BaseModel):

    model_config = ConfigDict(extra="ignore")

    hotels: List[Recommendation] = Field(default_factory=list)

    attractions: List[Recommendation] = Field(default_factory=list)

    restaurants: List[Recommendation] = Field(default_factory=list)

    activities: List[Recommendation] = Field(default_factory=list)

    flights: List[Recommendation] = Field(default_factory=list)

    transport: List[Recommendation] = Field(default_factory=list)

    def all(self):

        return (
            self.hotels
            + self.attractions
            + self.restaurants
            + self.activities
            + self.flights
            + self.transport
        )

    @property
    def total(self):

        return len(self.all())

    def selected(self):

        return [

            r

            for r in self.all()

            if r.selected

        ]
