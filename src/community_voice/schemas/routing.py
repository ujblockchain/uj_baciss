"""The contract for what the Routing Agent must return."""

from pydantic import BaseModel, Field


class RoutingResult(BaseModel):
    """Where a report should be sent."""

    municipality: str = Field(description="Municipality name, or 'unknown'.")
    department: str = Field(description="Responsible department, or 'unknown'.")
    needs_human: bool = Field(
        description="True if the municipality or department could not be found."
    )
    reason: str = Field(description="One short sentence explaining the routing.")
