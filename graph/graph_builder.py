"""
LangGraph Builder
"""

from langgraph.graph import StateGraph, END

from state.vita_state import VitaState

from agents.conversation_manager import ConversationManager
from agents.discovery_agent import DiscoveryAgent
from agents.map_agent import MapAgent
from agents.planner_agent import PlannerAgent
from agents.recommendation_agent import RecommendationAgent
from agents.approval_agent import ApprovalAgent


conversation = ConversationManager()
discovery = DiscoveryAgent()
map_agent = MapAgent()
planner = PlannerAgent()
recommendation = RecommendationAgent()
approval = ApprovalAgent()


# -------------------------------------------------------
# Nodes
# -------------------------------------------------------

def conversation_node(state: VitaState):

    conversation.execute(
        session_id=state.session_id,
        message=state.user_input
    )

    return state


def discovery_node(state: VitaState):

    discovery.execute(
        session_id=state.session_id
    )

    return state

def discovery_router(state: VitaState):

    if state.traveller.confidence < 0.80:

        return "conversation"

    return "map"

def map_node(state: VitaState):

    return state


def planner_node(state: VitaState):

    planner.execute(
        session_id=state.session_id
    )

    return state


def recommendation_node(state: VitaState):

    recommendation.execute(
        session_id=state.session_id
    )

    return state


def approval_node(state: VitaState):

    return state


# -------------------------------------------------------
# Graph
# -------------------------------------------------------

builder = StateGraph(VitaState)

builder.add_node("conversation", conversation_node)

builder.add_node("discovery", discovery_node)

builder.add_node("map", map_node)

builder.add_node("planner", planner_node)

builder.add_node("recommendation", recommendation_node)

builder.add_node("approval", approval_node)

builder.set_entry_point("conversation")

builder.add_edge("conversation", "discovery")

builder.add_edge("discovery", "map")

builder.add_edge("map", "planner")

builder.add_edge("planner", "recommendation")

builder.add_edge("recommendation", "approval")

builder.add_edge("approval", END)

graph = builder.compile()
