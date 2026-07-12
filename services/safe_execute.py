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

            start = time.perf_counter()

            response = AgentResponse(
                agent=agent_name,
                action=func.__name__,
            )

            try:

                result = func(*args, **kwargs)

                elapsed = round(
                    time.perf_counter() - start,
                    3,
                )

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

                return response

        return wrapper

    return decorator
