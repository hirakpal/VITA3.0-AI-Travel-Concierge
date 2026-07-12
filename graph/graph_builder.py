"""
graph_builder.py

LangGraph Workflow
VITA 3.0
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

# ---------------------------------------------------------
# Conversation
# ---------------------------------------------------------

def conversation_node(state: VitaState):

    conversation.execute(
        session_id=state.session_id,
        message=state.user_input
    )

    return state


# ---------------------------------------------------------
# Discovery
# ---------------------------------------------------------

def discovery_node(state: VitaState):

    discovery.execute(
        session_id=state.session_id
    )

    return state


# ---------------------------------------------------------
# Clarification
# ---------------------------------------------------------

def clarification_node(state: VitaState):

    """
    Ask ONE intelligent follow-up question.
    """

    traveller = state.traveller

    question = "Tell me more about your trip."

    if traveller.trip_purpose == "":

        question = "What is the purpose of your trip?"

    elif traveller.budget <= 0:

        question = "What is your approximate budget?"

    elif len(state.destinations) == 0:

        question = "Which destination would you like to visit?"

    elif traveller.travel_style == "":

        question = "How would you describe your travel style?"

    state.assistant_response = question

    return state


# ---------------------------------------------------------
# Map
# ---------------------------------------------------------

def map_node(state: VitaState):

    return state


# ---------------------------------------------------------
# Planner
# ---------------------------------------------------------

def planner_node(state: VitaState):

    planner.execute(
        session_id=state.session_id
    )

    return state


# ---------------------------------------------------------
# Recommendation
# ---------------------------------------------------------

def recommendation_node(state: VitaState):

    recommendation.execute(
        session_id=state.session_id
    )

    return state


# ---------------------------------------------------------
# Approval
# ---------------------------------------------------------

def approval_node(state: VitaState):

    return state

# -------------------------------------------------------
# Graph
# -------------------------------------------------------

# ---------------------------------------------------------
# Discovery Router
# ---------------------------------------------------------

def discovery_router(state: VitaState):

    if state.traveller.confidence < 0.80:

        return "clarification"

    return "map"


# ---------------------------------------------------------
# Map Router
# ---------------------------------------------------------

def map_router(state: VitaState):

    if len(state.destinations) == 0:

        return "clarification"

    return "planner"


# ---------------------------------------------------------
# Planner Router
# ---------------------------------------------------------

def planner_router(state: VitaState):

    if state.validation_score < 0.80:

        return "clarification"

    return "recommendation"


# ---------------------------------------------------------
# Approval Router
# ---------------------------------------------------------

def approval_router(state: VitaState):

    if state.approved:

        return END

    return "planner"
