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

def planner_router(state: VitaState):

    if state.validation_score < 0.80:

        return "conversation"

    return "recommendation"


def recommendation_node(state: VitaState):

    recommendation.execute(
        session_id=state.session_id
    )

    return state


def approval_node(state: VitaState):

    return state

def approval_router(state: VitaState):

    if state.approved:

        return END

    return "planner"


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

builder.add_conditional_edges(

    "discovery",

    discovery_router,

    {

        "conversation": "conversation",

        "map": "map"

    }

)

builder.add_conditional_edges(

    "planner",

    planner_router,

    {

        "conversation": "conversation",

        "recommendation": "recommendation"

    }

)

builder.add_conditional_edges(

    "approval",

    approval_router,

    {

        "planner": "planner",

        END: END

    }

)

graph = builder.compile()
