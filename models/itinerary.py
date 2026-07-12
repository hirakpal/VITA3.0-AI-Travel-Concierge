"""
Itinerary Model
VITA 3.0
"""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field, ConfigDict


class ItineraryItem(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        extra="ignore"
    )

    id: str = ""

    time: str = ""

    title: str = ""

    category: str = ""

    location: str = ""

    duration: str = ""

    notes: str = ""

    estimated_cost: float = 0.0

    completed: bool = False


class DayPlan(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        extra="ignore"
    )

    day: int = 1

    city: str = ""

    country: str = ""

    title: str = ""

    date: str = ""

    hotel: str = ""

    weather: str = ""

    items: List[ItineraryItem] = Field(default_factory=list)

    estimated_cost: float = 0.0

    def add_item(self, item: ItineraryItem):

        self.items.append(item)

        self.calculate_cost()

    def calculate_cost(self):

        self.estimated_cost = round(

            sum(i.estimated_cost for i in self.items),

            2

        )


class Itinerary(BaseModel):
    """
    Complete Trip Itinerary
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="ignore"
    )

    trip_name: str = ""

    start_date: str = ""

    end_date: str = ""

    total_days: int = 0

    total_budget: float = 0.0

    currency: str = "USD"

    destinations: List[str] = Field(default_factory=list)

    days: List[DayPlan] = Field(default_factory=list)

    validation_score: float = 0.0

    ai_confidence: float = 0.0

    approved: bool = False

    version: int = 1

    notes: str = ""

    def add_day(self, day: DayPlan):

        self.days.append(day)

        self.total_days = len(self.days)

        self.calculate_budget()

    def calculate_budget(self):

        self.total_budget = round(

            sum(day.estimated_cost for day in self.days),

            2

        )

    @property
    def total_locations(self):

        return sum(len(day.items) for day in self.days)

    def summary(self):

        return {

            "trip": self.trip_name,

            "days": self.total_days,

            "budget": self.total_budget,

            "currency": self.currency,

            "destinations": self.destinations,

            "validation": self.validation_score,

            "confidence": self.ai_confidence

        }

    def approve(self):

        self.approved = True

    def reset(self):

        self.__dict__.update(

            Itinerary().model_dump()

        )
