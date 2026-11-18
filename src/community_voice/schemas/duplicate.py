"""Contracts for the duplicate check."""

from pydantic import BaseModel, Field


class SameIncident(BaseModel):
    """The model's verdict on two reports."""

    same_incident: bool = Field(description="True if both describe the same incident.")
    reason: str = Field(description="One short sentence explaining the verdict.")


class DuplicateResult(BaseModel):
    """Whether a new report repeats an earlier one."""

    duplicate_of: str | None = Field(
        default=None, description="Id of the earlier report."
    )
    related_ids: list[str] = Field(
        default_factory=list,
        description="Similar reports that are a different incident.",
    )
    reason: str = ""
