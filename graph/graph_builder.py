"""
Graph Builder
VITA 3.0

Builds the execution pipeline.

Conversation
      ↓
Discovery
      ↓
Map
      ↓
Planner
      ↓
Recommendation
      ↓
Approval
"""

from __future__ import annotations

from agents.conversation_manager import ConversationManager
from agents.discovery_agent import DiscoveryAgent
from agents.map_agent import MapAgent
from agents.planner_agent import PlannerAgent
from agents.recommendation_agent import RecommendationAgent
from agents.approval_agent import ApprovalAgent


class GraphBuilder:

    def __init__(self):

        self.conversation = ConversationManager()

        self.discovery = DiscoveryAgent()

        self.map = MapAgent()

        self.planner = PlannerAgent()

        self.recommendation = RecommendationAgent()

        self.approval = ApprovalAgent()

    # =====================================================
    # Conversation
    # =====================================================

    def conversation_node(

        self,

        session_id,

        message

    ):

        return self.conversation.execute(

            session_id=session_id,

            message=message

        )

    # =====================================================
    # Discovery
    # =====================================================

    def discovery_node(

        self,

        session_id

    ):

        return self.discovery.execute(

            session_id=session_id

        )

    # =====================================================
    # Map
    # =====================================================

    def map_node(

        self,

        session_id,

        city="",

        country="",

        latitude=0.0,

        longitude=0.0

    ):

        return self.map.execute(

            session_id=session_id,

            city=city,

            country=country,

            latitude=latitude,

            longitude=longitude

        )

    # =====================================================
    # Planner
    # =====================================================

    def planner_node(

        self,

        session_id

    ):

        return self.planner.execute(

            session_id=session_id

        )

    # =====================================================
    # Recommendation
    # =====================================================

    def recommendation_node(

        self,

        session_id

    ):

        return self.recommendation.execute(

            session_id=session_id

        )

    # =====================================================
    # Approval
    # =====================================================

    def approval_node(

        self,

        session_id,

        decision,

        comments=""

    ):

        return self.approval.execute(

            session_id=session_id,

            decision=decision,

            comments=comments

        )


graph = GraphBuilder()
