"""
Global Workflow State
VITA 3.0

This is the SINGLE SOURCE OF TRUTH for the entire application.
Every Agent, Tool, Service and LangGraph node reads/writes this state.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from pydantic import BaseModel, ConfigDict, Field

from models.traveller import Traveller
from models.travel_dna import TravelDNA
from models.destination import Destination
from models.recommendation import RecommendationCollection
from models.itinerary import Itinerary
from models.response import AgentResponse


STAGE_PROGRESS = {
    "Conversation": 1 / 6,
    "Discovery": 2 / 6,
    "Map": 3 / 6,
    "Planner": 4 / 6,
    "Recommendation": 5 / 6,
    "Approval": 1.0,
}


class VitaState(BaseModel):

    model_config = ConfigDict(
        validate_assignment=True,
        arbitrary_types_allowed=True,
        extra="ignore"
    )

    # ======================================================
    # Session
    # ======================================================

    session_id: str = ""

    user_id: str = ""

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # ======================================================
    # Conversation
    # ======================================================

    user_input: str = ""

    assistant_response: str = ""

    conversation_history: List[Dict[str, str]] = Field(default_factory=list)

    # ======================================================
    # Traveller
    # ======================================================

    traveller: Traveller = Field(default_factory=Traveller)

    travel_dna: TravelDNA = Field(default_factory=TravelDNA)

    # ======================================================
    # Planning
    # ======================================================

    destinations: List[Destination] = Field(default_factory=list)

    recommendations: RecommendationCollection = Field(
        default_factory=RecommendationCollection
    )

    itinerary: Itinerary = Field(default_factory=Itinerary)

    # ======================================================
    # Workflow
    # ======================================================

    current_agent: str = "Conversation"

    current_step: str = "Idle"

    current_stage: str = "Conversation"

    progress: float = 0.0

    workflow_status: str = "READY"

    confidence: float = 0.0

    validation_score: float = 0.0

    # ======================================================
    # Approval
    # ======================================================

    awaiting_approval: bool = False

    approved: bool = False

    rejected: bool = False

    # ======================================================
    # Audit
    # ======================================================

    audit_log: List[str] = Field(default_factory=list)

    tool_history: List[str] = Field(default_factory=list)

    # ======================================================
    # Last Response
    # ======================================================

    last_response: AgentResponse = Field(
        default_factory=AgentResponse
    )

    # ======================================================
    # Metadata
    # ======================================================

    metadata: Dict[str, Any] = Field(default_factory=dict)

    # ======================================================
    # Helper Functions
    # ======================================================

    def update_timestamp(self):

        self.updated_at = datetime.utcnow()

    def set_user_input(self, message: str):

        self.user_input = message

        self.conversation_history.append(
            {
                "role": "user",
                "content": message
            }
        )

        self.update_timestamp()

    def set_assistant_response(self, message: str):

        self.assistant_response = message

        self.conversation_history.append(
            {
                "role": "assistant",
                "content": message
            }
        )

        self.update_timestamp()

    def add_destination(self, destination: Destination):

        self.destinations.append(destination)

        self.update_timestamp()

    def clear_destinations(self):

        self.destinations.clear()

    def add_audit(self, message: str):

        ts = datetime.utcnow().strftime("%H:%M:%S")

        self.audit_log.append(f"[{ts}] {message}")

    def add_tool_call(self, tool: str):

        self.tool_history.append(tool)

    def set_agent(self, agent: str):

        self.current_agent = agent

    def set_step(self, step: str):

        self.current_step = step

    def set_stage(self, stage: str):

        self.current_stage = stage

        self.progress = STAGE_PROGRESS.get(stage, self.progress)

    def set_response(self, response: AgentResponse):

        self.last_response = response

        self.confidence = response.confidence

        self.validation_score = response.validation_score

    def approve(self):

        self.approved = True

        self.awaiting_approval = False

        self.rejected = False

    def reject(self):

        self.rejected = True

        self.awaiting_approval = False

        self.approved = False

    def reset(self):

        fresh = VitaState(
            session_id=self.session_id,
            user_id=self.user_id,
        )

        for field in fresh.model_fields:
            setattr(self, field, getattr(fresh, field))

    @property
    def total_destinations(self):

        return len(self.destinations)

    @property
    def total_messages(self):

        return len(self.conversation_history)

    def summary(self):

        return {

            "traveller": self.traveller.name,

            "messages": self.total_messages,

            "destinations": self.total_destinations,

            "confidence": self.confidence,

            "validation": self.validation_score,

            "current_agent": self.current_agent,

            "workflow": self.workflow_status,

            "approved": self.approved

        }
