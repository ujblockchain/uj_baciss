"""The state shared by every step of the workflow."""

from typing_extensions import TypedDict

from community_voice.schemas.context_check import ContextCheckResult
from community_voice.schemas.draft import DraftDecision, DraftResponse
from community_voice.schemas.duplicate import DuplicateResult
from community_voice.schemas.report import ReportIn
from community_voice.schemas.review import ReviewDecision
from community_voice.schemas.routing import RoutingResult
from community_voice.schemas.triage import TriageResult


class ReportState(TypedDict, total=False):
    """Input is report_id and report. Each step adds its own result."""

    report_id: str
    report: ReportIn
    triage_result: TriageResult
    routing_result: RoutingResult
    context_result: ContextCheckResult
    duplicate_result: DuplicateResult
    review: ReviewDecision
    draft: DraftResponse
    draft_decision: DraftDecision
    status: str
