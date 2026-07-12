"""
Guardrails
VITA 3.0

Runs BEFORE every LLM call.
"""

from __future__ import annotations

import re

from models.response import AgentResponse


class Guardrails:

    def __init__(self):

        self.allowed_topics = [

            "travel",

            "trip",

            "holiday",

            "vacation",

            "hotel",

            "flight",

            "restaurant",

            "food",

            "visa",

            "passport",

            "itinerary",

            "destination",

            "tour",

            "tourism",

            "beach",

            "mountain",

            "adventure",

            "honeymoon",

            "family",

            "airport",

            "transport",

            "weather"

        ]

        self.blocked_patterns = [

            r"ignore previous instructions",

            r"system prompt",

            r"developer mode",

            r"reveal prompt",

            r"show hidden",

            r"jailbreak",

            r"sudo",

            r"rm -rf",

            r"<script",

            r"</script"

        ]

    # =====================================================
    # Main Validation
    # =====================================================

    def validate(

        self,

        user_input: str

    ) -> AgentResponse:

        response = AgentResponse()

        text = user_input.lower()

        # ----------------------------
        # Empty
        # ----------------------------

        if not text.strip():

            response.success = False

            response.add_error("Empty message.")

            return response

        # ----------------------------
        # Prompt Injection
        # ----------------------------

        for pattern in self.blocked_patterns:

            if re.search(pattern, text):

                response.success = False

                response.add_error(

                    "Prompt injection attempt detected."

                )

                return response

        # ----------------------------
        # Travel Scope
        # ----------------------------

        if not any(

            word in text

            for word in self.allowed_topics

        ):

            response.add_warning(

                "Conversation is outside travel domain."

            )

        # ----------------------------
        # Personal Data
        # ----------------------------

        text = self.mask_pii(text)

        response.data["clean_text"] = text

        response.success = True

        return response

    # =====================================================
    # PII Masking
    # =====================================================

    def mask_pii(

        self,

        text: str

    ) -> str:

        # Email

        text = re.sub(

            r"\S+@\S+",

            "[EMAIL]",

            text

        )

        # Phone

        text = re.sub(

            r"\+?\d[\d -]{8,}",

            "[PHONE]",

            text

        )

        # Passport (simple)

        text = re.sub(

            r"[A-Z]{1,2}\d{6,8}",

            "[PASSPORT]",

            text

        )

        return text

    # =====================================================
    # Output Validation
    # =====================================================

    def validate_output(

        self,

        answer: str

    ) -> AgentResponse:

        response = AgentResponse()

        if len(answer.strip()) == 0:

            response.success = False

            response.add_error(

                "LLM returned empty output."

            )

            return response

        if len(answer) < 20:

            response.add_warning(

                "Very short response."

            )

        response.success = True

        return response


guardrails = Guardrails()
