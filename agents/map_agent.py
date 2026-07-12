"""
Map Agent
VITA 3.0
"""

from __future__ import annotations

from agents.base_agent import BaseAgent
from models.destination import Destination


class MapAgent(BaseAgent):

    def __init__(self):
        super().__init__("MapAgent")

    def run(
        self,
        state,
        city: str = "",
        country: str = "",
        latitude: float = 0.0,
        longitude: float = 0.0,
        **kwargs
    ):

        destination = Destination(
            city=city,
            country=country
        )

        destination.coordinates.latitude = latitude
        destination.coordinates.longitude = longitude

        state.add_destination(destination)

        self.audit(
            state,
            f"Destination added: {destination.display_name}"
        )

        return self.success(
            "Destination added.",
            confidence=1.0,
            destination=destination.model_dump()
        )
