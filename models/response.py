"""
Standard Response Model
VITA 3.0

Every Agent, Service, Tool and Graph Node
returns this object.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from pydantic import BaseModel, Field, ConfigDict


class AgentResponse(BaseModel):

    model_config = ConfigDict(
        validate_assignment=True,
        extra="ignore"
    )

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    success: bool = True

    message: str = ""

    agent: str = ""

    node: str = ""

    action: str = ""

    # --------------------------------------------------
    # AI
    # --------------------------------------------------

    confidence: float = 0.0

    reasoning: str = ""

    reflection: str = ""

    # --------------------------------------------------
    # Data
    # --------------------------------------------------

    data: Dict[str, Any] = Field(default_factory=dict)

    recommendations: List[Any] = Field(default_factory=list)

    tool_results: List[Any] = Field(default_factory=list)

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    warnings: List[str] = Field(default_factory=list)

    errors: List[str] = Field(default_factory=list)

    validation_score: float = 0.0

    requires_approval: bool = False

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    execution_time: float = 0.0

    tokens_used: int = 0

    timestamp: datetime = Field(default_factory=datetime.utcnow)

    metadata: Dict[str, Any] = Field(default_factory=dict)

    # --------------------------------------------------
    # Helper Methods
    # --------------------------------------------------

    def add_warning(self, warning: str):

        if warning not in self.warnings:

            self.warnings.append(warning)

    def add_error(self, error: str):

        self.success = False

        self.errors.append(error)

    def add_data(self, key: str, value: Any):

        self.data[key] = value

    def add_metadata(self, key: str, value: Any):

        self.metadata[key] = value

    def merge(self, other: "AgentResponse"):

        self.data.update(other.data)

        self.metadata.update(other.metadata)

        self.warnings.extend(other.warnings)

        self.errors.extend(other.errors)

        self.recommendations.extend(other.recommendations)

        self.tool_results.extend(other.tool_results)

        self.success = self.success and other.success

        self.confidence = max(

            self.confidence,

            other.confidence

        )

        self.validation_score = max(

            self.validation_score,

            other.validation_score

        )

    @property
    def has_errors(self):

        return len(self.errors) > 0

    @property
    def has_warnings(self):

        return len(self.warnings) > 0

    def summary(self):

        return {

            "success": self.success,

            "agent": self.agent,

            "action": self.action,

            "confidence": self.confidence,

            "validation": self.validation_score,

            "warnings": len(self.warnings),

            "errors": len(self.errors)

        }

    @classmethod
    def ok(

        cls,

        message: str,

        **kwargs

    ):

        return cls(

            success=True,

            message=message,

            **kwargs

        )

    @classmethod
    def fail(

        cls,

        message: str,

        **kwargs

    ):

        return cls(

            success=False,

            message=message,

            **kwargs

        )
