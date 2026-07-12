"""
graph_builder.py

LangGraph Workflow
VITA 3.0
"""

from langgraph.graph import StateGraph, END

from state.vita_state import VitaState

from agents.conversation_agent import ConversationManager
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

    state.set_stage("Conversation")

    return conversation.execute(state)


# ---------------------------------------------------------
# Discovery
# ---------------------------------------------------------

def discovery_node(state: VitaState):

    state.set_stage("Discovery")

    return discovery.execute(state)


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

    state.set_stage("Map")

    return map_agent.execute(state)


# ---------------------------------------------------------
# Planner
# ---------------------------------------------------------

def planner_node(state: VitaState):

    state.set_stage("Planner")

    return planner.execute(state)


# ---------------------------------------------------------
# Recommendation
# ---------------------------------------------------------

def recommendation_node(state: VitaState):

    state.set_stage("Recommendation")

    return recommendation.execute(state)

# ---------------------------------------------------------
# Approval
# ---------------------------------------------------------

def approval_node(state: VitaState):

    state.set_stage("Approval")

    return approval.execute(state)


# ==========================================================
# Build Router
# ==========================================================

# ---------------------------------------------------------
# Discovery Router
# ---------------------------------------------------------

def discovery_router(state: VitaState):

    if state.traveller.confidence < 0.80:
        return "clarification"

    if len(state.destinations) == 0:
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
# Post-Conversation Router
# ---------------------------------------------------------

def post_conversation_router(state: VitaState):

    """
    A trip is only awaiting approval once recommendations have
    already been generated on a *previous* turn. In that case the
    traveller's new message is their approve/reject/edit decision,
    so route straight to approval instead of re-running the whole
    discovery -> map -> planner -> recommendation pipeline.
    """

    if state.awaiting_approval:
        return "approval"

    return "discovery"


# ==========================================================
# Build Graph
# ==========================================================

builder = StateGraph(VitaState)

# ----------------------------------------------------------
# Nodes
# ----------------------------------------------------------

builder.add_node("conversation", conversation_node)

builder.add_node("discovery", discovery_node)

builder.add_node("clarification", clarification_node)

builder.add_node("map", map_node)

builder.add_node("planner", planner_node)

builder.add_node("recommendation", recommendation_node)

builder.add_node("approval", approval_node)

# ----------------------------------------------------------
# Entry Point
# ----------------------------------------------------------

builder.set_entry_point("conversation")

# ----------------------------------------------------------
# Post-Conversation Routing
# ----------------------------------------------------------

builder.add_conditional_edges(

    "conversation",

    post_conversation_router,

    {

        "discovery": "discovery",

        "approval": "approval"

    }

)

# ----------------------------------------------------------
# Discovery Routing
# ----------------------------------------------------------

builder.add_conditional_edges(

    "discovery",

    discovery_router,

    {

        "clarification": "clarification",

        "map": "map"

    }

)

# ----------------------------------------------------------
# Clarification
# ----------------------------------------------------------

builder.add_edge(

    "clarification",

    END

)

# ----------------------------------------------------------
# Map Routing
# ----------------------------------------------------------

builder.add_conditional_edges(

    "map",

    map_router,

    {

        "clarification": "clarification",

        "planner": "planner"

    }

)

# ----------------------------------------------------------
# Planner Routing
# ----------------------------------------------------------

builder.add_conditional_edges(

    "planner",

    planner_router,

    {

        "clarification": "clarification",

        "recommendation": "recommendation"

    }

)

# ----------------------------------------------------------
# Recommendation
# ----------------------------------------------------------

# Recommendations are generated, awaiting_approval is set, and the
# turn ends here. The traveller's next message is their decision,
# which post_conversation_router routes straight to "approval".

builder.add_edge(

    "recommendation",

    END

)

# ----------------------------------------------------------
# Approval
# ----------------------------------------------------------

# approve / reject / edit / replan are all resolved within a single
# turn; any follow-up work (a new itinerary, a fresh conversation)
# happens on the traveller's next message, re-entering at the top.

builder.add_edge(

    "approval",

    END

)

# ----------------------------------------------------------
# Compile
# ----------------------------------------------------------

graph = builder.compile()
