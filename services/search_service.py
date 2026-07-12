"""
Search Service
VITA 3.0

Central search abstraction.

Later this will call:

Google Places
Google Maps
Weather
Flights
Hotels

For MVP it returns mock data.
"""

from __future__ import annotations


class SearchService:

    # ==========================================================
    # Hotels
    # ==========================================================

    def hotels(

        self,

        city: str

    ):

        return [

            {

                "name": f"{city} Grand Hotel",

                "rating": 4.8,

                "price": 220

            },

            {

                "name": f"{city} Marriott",

                "rating": 4.7,

                "price": 180

            }

        ]

    # ==========================================================
    # Restaurants
    # ==========================================================

    def restaurants(

        self,

        city: str

    ):

        return [

            {

                "name": f"{city} Fine Dining",

                "rating": 4.9

            },

            {

                "name": f"{city} Local Kitchen",

                "rating": 4.7

            }

        ]

    # ==========================================================
    # Attractions
    # ==========================================================

    def attractions(

        self,

        city: str

    ):

        return [

            {

                "name": f"{city} City Museum",

                "rating": 4.8

            },

            {

                "name": f"{city} Historic Centre",

                "rating": 4.9

            }

        ]

    # ==========================================================
    # Activities
    # ==========================================================

    def activities(

        self,

        city: str

    ):

        return [

            {

                "name": "Walking Tour"

            },

            {

                "name": "Food Tour"

            }

        ]

    # ==========================================================
    # Nearby
    # ==========================================================

    def nearby(

        self,

        city: str

    ):

        return {

            "hotels": self.hotels(city),

            "restaurants": self.restaurants(city),

            "attractions": self.attractions(city),

            "activities": self.activities(city)

        }


search_service = SearchService()
