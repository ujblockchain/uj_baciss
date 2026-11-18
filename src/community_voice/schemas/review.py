"""Contracts for human review and for saved reports."""

from typing import Literal

from pydantic import BaseModel, Field

from community_voice.schemas.triage import Category, Urgency


class ReviewDecision(BaseModel):
    """What the reviewer sends back."""

    action: Literal["approve", "reject"]
    category: Category | None = Field(default=None, description="Corrected category.")
    urgency: Urgency | None = Field(default=None, description="Corrected urgency.")
    department: str | None = Field(default=None, description="Corrected department.")
    note: str = ""


class ReportRecord(BaseModel):
    """A report as saved in the database."""

    id: str
    text: str
    status: str
    category: str
    urgency: str
    municipality: str
    department: str
    duplicate_of: str | None
    created_at: str
    updated_at: str
