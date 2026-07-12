from graph.graph_builder import graph
from services.memory_service import memory_service


class Workflow:

    def run(
        self,
        session_id: str,
        message: str,
    ):

        # Restore previous state
        state = memory_service.start_session(session_id)

        # Update latest user message
        state.user_input = message

        print("===== BEFORE GRAPH =====")
        print(type(state))
        print(type(state.recommendations))
        print(state.recommendations)

        # Execute LangGraph
        state = graph.invoke(state)

        # Persist latest state
        memory_service.save_state(state)

        return state


workflow = Workflow()
workflow = Workflow()
