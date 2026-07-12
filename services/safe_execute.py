"""
Safe Execute
VITA 3.0

Standard execution wrapper for every
Agent, Tool and Engine.
"""

from __future__ import annotations

import time
import traceback
from functools import wraps

from models.response import AgentResponse


def safe_execute(agent_name: str):
    """
    Decorator for safe execution.
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            from state.vita_state import VitaState

            start = time.perf_counter()

            response = AgentResponse(
                agent=agent_name,
                action=func.__name__,
            )

            state = kwargs.get("state")

            if state is None and len(args) > 1:
                state = args[1]

            try:

                result = func(*args, **kwargs)

                elapsed = round(
                    time.perf_counter() - start,
                    3,
                )

                # -------------------------------------------------
                # Agent already returned the workflow state
                # -------------------------------------------------

                if isinstance(result, VitaState):

                    return result

                # -------------------------------------------------
                # Agent already returned AgentResponse
                # -------------------------------------------------

                if isinstance(result, AgentResponse):

                    result.execution_time = elapsed

                    return result

                # -------------------------------------------------
                # Wrap normal object
                # -------------------------------------------------

                response.success = True

                response.execution_time = elapsed

                response.data["result"] = result

                return response

            except Exception as e:

                elapsed = round(
                    time.perf_counter() - start,
                    3,
                )

                response.success = False

                response.execution_time = elapsed

                response.add_error(str(e))

                response.reasoning = traceback.format_exc()

                # ---------------------------------------------------
                # Node functions must keep returning VitaState so the
                # graph's state schema stays intact even on failure.
                # ---------------------------------------------------

                if isinstance(state, VitaState):

                    state.set_response(response)

                    state.assistant_response = (
                        "Something went wrong while processing your "
                        "request. Please try again."
                    )

                    state.add_audit(f"{agent_name}: ERROR - {e}")

                    return state

                return response

        return wrapper

    return decorator
