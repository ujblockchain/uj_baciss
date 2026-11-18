"""The contract for what the Context Check Agent must return."""

from enum import StrEnum

from pydantic import BaseModel, Field


class Finding(StrEnum):
    PLANNED_OUTAGE = "planned_outage"
    UNPLANNED_OUTAGE = "unplanned_outage"
    NOTHING_FOUND = "nothing_found"


class Confidence(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Source(BaseModel):
    title: str
    url: str


class ContextCheckResult(BaseModel):
    """What the web says about a reported problem."""

    finding: Finding = Field(description="Whether a known incident was found.")
    summary: str = Field(description="One or two short sentences on what was found.")
    confidence: Confidence = Field(description="How well the sources support it.")
    sources: list[Source] = Field(
        default_factory=list,
        description="Only pages returned by the search. Empty if nothing was found.",
    )
