"""Contracts for the drafted reply and the reviewer's decision on it."""

from typing import Literal

from pydantic import BaseModel, Field


class DraftResponse(BaseModel):
    """A suggested reply to the citizen."""

    body: str = Field(description="The reply to the citizen, in English.")
    policy_sources: list[str] = Field(
        default_factory=list,
        description="Names of the policy files the reply relies on.",
    )


class DraftDecision(BaseModel):
    """What the reviewer decides about the draft."""

    action: Literal["approve", "reject"]
    text: str | None = Field(default=None, description="Edited reply, if changed.")
