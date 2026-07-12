"""
Audit Service
VITA 3.0

Central audit logger.
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List


class AuditService:

    def __init__(self):

        self.logs: List[Dict] = []

    # ==========================================================
    # Log
    # ==========================================================

    def log(

        self,

        agent: str,

        action: str,

        status: str = "SUCCESS",

        details: str = "",

        session_id: str = ""

    ):

        self.logs.append(

            {

                "timestamp": datetime.utcnow(),

                "session_id": session_id,

                "agent": agent,

                "action": action,

                "status": status,

                "details": details

            }

        )

    # ==========================================================
    # Success
    # ==========================================================

    def success(

        self,

        agent: str,

        action: str,

        details: str = "",

        session_id: str = ""

    ):

        self.log(

            agent,

            action,

            "SUCCESS",

            details,

            session_id

        )

    # ==========================================================
    # Failure
    # ==========================================================

    def failure(

        self,

        agent: str,

        action: str,

        details: str = "",

        session_id: str = ""

    ):

        self.log(

            agent,

            action,

            "FAILED",

            details,

            session_id

        )

    # ==========================================================
    # Search
    # ==========================================================

    def by_agent(

        self,

        agent: str

    ):

        return [

            log

            for log in self.logs

            if log["agent"] == agent

        ]

    # ==========================================================
    # Session Logs
    # ==========================================================

    def by_session(

        self,

        session_id: str

    ):

        return [

            log

            for log in self.logs

            if log["session_id"] == session_id

        ]

    # ==========================================================
    # Latest
    # ==========================================================

    def latest(

        self,

        count: int = 20

    ):

        return self.logs[-count:]

    # ==========================================================
    # Clear
    # ==========================================================

    def clear(self):

        self.logs.clear()


audit_service = AuditService()
