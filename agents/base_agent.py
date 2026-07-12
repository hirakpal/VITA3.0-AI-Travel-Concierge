"""
Base Agent
VITA 3.0

Every Agent inherits from this class.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from models.response import AgentResponse
from services.llm_service import llm
from services.guardrails import guardrails
from services.memory_service import memory_service
from services.safe_execute import safe_execute


class BaseAgent(ABC):

    def __init__(

        self,

        name: str

    ):

        self.name = name

        self.llm = llm

        self.memory = memory_service

        self.guardrails = guardrails

    # =====================================================
    # Main Entry
    # =====================================================

    @safe_execute("BaseAgent")
    def execute(self, state):
        response = self.run(state=state)

        if not isinstance(response, AgentResponse):
            return state

        state.set_response(response)
        state.set_agent(self.name)

        self.memory.save_state(state)
        return state

    # =====================================================
    # Abstract
    # =====================================================

    @abstractmethod
    def run(

        self,

        state,

        **kwargs

    ) -> AgentResponse:

        pass

    # =====================================================
    # Helpers
    # =====================================================

    def audit(

        self,

        state,

        message: str

    ):

        state.add_audit(

            f"{self.name}: {message}"

        )

    def tool(

        self,

        state,

        tool_name: str

    ):

        state.add_tool_call(tool_name)

    def validate(

        self,

        text: str

    ):

        return self.guardrails.validate(text)

    def ask(

        self,

        system_prompt: str,

        prompt: str

    ):

        return self.llm.chat(

            system_prompt,

            prompt

        )

    def success(

        self,

        message: str,

        confidence: float = 1.0,

        **data

    ):

        r = AgentResponse.ok(

            message,

            agent=self.name,

            confidence=confidence

        )

        r.data.update(data)

        return r

    def failure(

        self,

        message: str

    ):

        return AgentResponse.fail(

            message,

            agent=self.name

        )
