"""
Traveller Model
VITA 3.0
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


class Traveller(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        extra="ignore"
    )

    # ----------------------------
    # Basic Information
    # ----------------------------

    name: str = ""

    email: str = ""

    nationality: str = ""

    home_country: str = ""

    preferred_language: str = "English"

    # ----------------------------
    # Trip Information
    # ----------------------------

    trip_purpose: str = ""

    mood: str = ""

    travel_style: str = ""

    # ----------------------------
    # Travellers
    # ----------------------------

    adults: int = 1

    children: int = 0

    infants: int = 0

    # ----------------------------
    # Budget
    # ----------------------------

    budget: float = 0.0

    currency: str = "USD"

    # ----------------------------
    # Preferences
    # ----------------------------

    interests: List[str] = Field(default_factory=list)

    food_preferences: List[str] = Field(default_factory=list)

    hotel_preferences: List[str] = Field(default_factory=list)

    transport_preferences: List[str] = Field(default_factory=list)

    accessibility_requirements: List[str] = Field(default_factory=list)

    # ----------------------------
    # Constraints
    # ----------------------------

    visa_required: bool = False

    passport_available: bool = True

    travel_insurance: bool = False

    # ----------------------------
    # Conversation
    # ----------------------------

    notes: str = ""

    confidence: float = 0.0

    # ----------------------------
    # Helper Methods
    # ----------------------------

    @property
    def total_travellers(self) -> int:
        return self.adults + self.children + self.infants

    def update_confidence(self):

        score = 0

        if self.trip_purpose:
            score += 20

        if self.budget > 0:
            score += 20

        if self.travel_style:
            score += 20

        if self.mood:
            score += 20

        if self.interests:
            score += 20

        self.confidence = round(score / 100, 2)

    @property
    def is_complete(self):

        return self.confidence >= 0.80

    def summary(self):

        return {

            "travellers": self.total_travellers,

            "budget": self.budget,

            "currency": self.currency,

            "purpose": self.trip_purpose,

            "style": self.travel_style,

            "mood": self.mood,

            "interests": self.interests

        }

    def reset(self):

        self.__dict__.update(
            Traveller().model_dump()
        )
