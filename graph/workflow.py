from graph.graph_builder import graph
from services.memory_service import memory_service


class Workflow:

    def run(
        self,
        session_id: str,
        message: str
    ):

        state = memory_service.start_session(
            session_id
        )

        state.user_input = message

        result = graph.invoke(state)

        memory_service.save_state(result)

        return result


workflow = Workflow()
