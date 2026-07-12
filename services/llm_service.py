"""
LLM Service
VITA 3.0

Single entry point for every LLM call.

All Agents should call this service.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv

from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)

from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


class LLMService:

    def __init__(self):

        self.model = ChatGoogleGenerativeAI(

            model="gemini-2.5-pro",

            temperature=0.2,

            google_api_key=os.getenv("GOOGLE_API_KEY")

        )

    # =====================================================
    # Generic Chat
    # =====================================================

    def chat(

        self,

        system_prompt: str,

        user_prompt: str

    ) -> str:

        messages = [

            SystemMessage(content=system_prompt),

            HumanMessage(content=user_prompt)

        ]

        response = self.model.invoke(messages)

        return response.content

    # =====================================================
    # Structured Prompt
    # =====================================================

    def ask(

        self,

        prompt: str

    ) -> str:

        response = self.model.invoke(prompt)

        return response.content

    # =====================================================
    # Discovery
    # =====================================================

    def discover(

        self,

        conversation: str

    ) -> str:

        prompt = f"""

You are VITA.

Extract:

- Intent
- Mood
- Budget
- Travel Style
- Companions
- Destination
- Missing Information

Conversation

{conversation}

"""

        return self.ask(prompt)

    # =====================================================
    # Planner
    # =====================================================

    def create_plan(

        self,

        traveller,

        destinations

    ) -> str:

        prompt = f"""

Traveller

{traveller.model_dump_json(indent=2)}

Destinations

{destinations}

Create an optimized travel plan.

"""

        return self.ask(prompt)

    # =====================================================
    # Recommendation
    # =====================================================

    def recommend(

        self,

        traveller,

        destination

    ) -> str:

        prompt = f"""

Traveller

{traveller.model_dump_json(indent=2)}

Destination

{destination}

Recommend:

Hotels

Restaurants

Activities

Transport

"""

        return self.ask(prompt)

    # =====================================================
    # Reflection
    # =====================================================

    def reflect(

        self,

        answer: str

    ) -> str:

        prompt = f"""

Review the following answer.

Find:

Mistakes

Hallucinations

Missing Information

Confidence

Answer

{answer}

"""

        return self.ask(prompt)

    # =====================================================
    # Validator
    # =====================================================

    def validate(

        self,

        itinerary

    ) -> str:

        prompt = f"""

Validate the itinerary.

Check

Budget

Flow

Travel Time

Hotel

Weather

Output score out of 100.

{itinerary}

"""

        return self.ask(prompt)


# ----------------------------------------------------------

llm = LLMService()
