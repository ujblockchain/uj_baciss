"""Graph nodes: each reads the shared state and returns only what it changes."""

from langgraph.runtime import Runtime
from langgraph.types import interrupt

from community_voice.agents.context_check import context_check
from community_voice.agents.drafter import write_draft
from community_voice.agents.routing import route
from community_voice.agents.triage import triage
from community_voice.db.repository import (
    finish_draft,
    save_draft,
    save_report,
    save_review,
)
from community_voice.graph.memory import find_hints, remember_correction
from community_voice.graph.state import ReportState
from community_voice.rag.reports import add_report
from community_voice.schemas.draft import DraftDecision
from community_voice.schemas.review import ReviewDecision
from community_voice.schemas.triage import TriageResult, Urgency
from community_voice.tools.duplicates import check_duplicate


def _index_text(triaged: TriageResult) -> str:
    return f"{triaged.area_mentioned or ''}: {triaged.english_text}"


def _persist(state: ReportState, status: str) -> None:
    """Save the report in the database and in the similarity index."""
    triaged, routed = state["triage_result"], state["routing_result"]
    duplicate = state.get("duplicate_result")
    save_report(
        report_id=state["report_id"],
        text=state["report"].text,
        status=status,
        category=triaged.category.value,
        urgency=triaged.urgency.value,
        municipality=routed.municipality,
        department=routed.department,
        duplicate_of=duplicate.duplicate_of if duplicate else None,
    )
    add_report(state["report_id"], _index_text(triaged), triaged.category.value)


def triage_node(state: ReportState, runtime: Runtime) -> dict:
    """Triage, with hints from past reviewer corrections (long-term memory)."""
    hints = find_hints(runtime.store, state["report"].text)
    return {"triage_result": triage(state["report"], hints=hints)}


def routing_node(state: ReportState) -> dict:
    return {"routing_result": route(state["triage_result"])}


def context_check_node(state: ReportState) -> dict:
    triaged = state["triage_result"]
    result = context_check(
        triaged.category.value,
        triaged.area_mentioned or "",
        state["routing_result"].municipality,
    )
    return {"context_result": result}


def known_outage_node(state: ReportState) -> dict:
    status = "known_planned_outage"
    _persist(state, status)
    return {"status": status}


def duplicate_check_node(state: ReportState) -> dict:
    triaged = state["triage_result"]
    duplicate = check_duplicate(
        state["report_id"], _index_text(triaged), triaged.category.value
    )
    if duplicate.duplicate_of:
        status = "duplicate"
    elif triaged.urgency is Urgency.CRITICAL:
        status = "fast_track"
    elif state["routing_result"].needs_human:
        status = "needs_human"
    else:
        status = "ready_for_review"
    return {"duplicate_result": duplicate, "status": status}


def save_report_node(state: ReportState) -> dict:
    _persist(state, state["status"])
    return {"status": state["status"]}


def human_review_node(state: ReportState) -> dict:
    """Pause for a reviewer. No side effects before interrupt(): this node re-runs."""
    context = state.get("context_result")
    duplicate = state["duplicate_result"]
    answer = interrupt(
        {
            "report_id": state["report_id"],
            "text": state["report"].text,
            "status": state["status"],
            "triage": state["triage_result"].model_dump(mode="json"),
            "routing": state["routing_result"].model_dump(mode="json"),
            "context": context.model_dump(mode="json") if context else None,
            "duplicate": duplicate.model_dump(mode="json"),
        }
    )
    return {"review": ReviewDecision.model_validate(answer)}


def finish_review_node(state: ReportState, runtime: Runtime) -> dict:
    decision = state["review"]
    status = "approved" if decision.action == "approve" else "rejected"
    save_review(state["report_id"], decision, status)
    remember_correction(
        runtime.store,
        state["report_id"],
        state["report"].text,
        state["triage_result"],
        state["routing_result"].department,
        decision,
    )

    update: dict = {"status": status}
    triage_changes = decision.model_dump(
        include={"category", "urgency"}, exclude_none=True
    )
    if triage_changes:
        update["triage_result"] = state["triage_result"].model_copy(
            update=triage_changes
        )
    if decision.department:
        routing = state["routing_result"]
        update["routing_result"] = routing.model_copy(
            update={"department": decision.department}
        )
    return update


def drafter_node(state: ReportState) -> dict:
    draft = write_draft(
        state["report_id"],
        state["triage_result"],
        state["routing_result"],
        state.get("context_result"),
    )
    save_draft(state["report_id"], draft.body)
    return {"draft": draft}


def draft_review_node(state: ReportState) -> dict:
    """Second approval. No side effects before interrupt(): this node re-runs."""
    answer = interrupt(
        {
            "report_id": state["report_id"],
            "department": state["routing_result"].department,
            "draft": state["draft"].model_dump(mode="json"),
        }
    )
    return {"draft_decision": DraftDecision.model_validate(answer)}


def finish_draft_node(state: ReportState) -> dict:
    decision, draft = state["draft_decision"], state["draft"]
    if decision.action == "approve":
        status, body = "ready_to_send", decision.text or draft.body
    else:
        status, body = "draft_rejected", draft.body
    finish_draft(state["report_id"], body, status)
    return {"status": status, "draft": draft.model_copy(update={"body": body})}
