"""The workflow: how the steps connect and where the paths split."""

from typing import Literal

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import END, START, StateGraph
from langgraph.store.base import BaseStore

from community_voice.graph import nodes
from community_voice.graph.state import ReportState
from community_voice.schemas.context_check import Finding
from community_voice.schemas.triage import Urgency


def after_routing(state: ReportState) -> Literal["context_check", "duplicate_check"]:
    """Critical reports, and reports with no known municipality, skip the web search."""
    if state["triage_result"].urgency is Urgency.CRITICAL:
        return "duplicate_check"
    if state["routing_result"].needs_human:
        return "duplicate_check"
    return "context_check"


def after_context_check(
    state: ReportState,
) -> Literal["known_outage", "duplicate_check"]:
    """A planned outage ends the workflow early, without human review."""
    if state["context_result"].finding is Finding.PLANNED_OUTAGE:
        return "known_outage"
    return "duplicate_check"


def after_review(state: ReportState) -> Literal["drafter", "__end__"]:
    """Only approved reports get a drafted reply."""
    return "drafter" if state["status"] == "approved" else END


def build_graph(
    checkpointer: BaseCheckpointSaver | None = None, store: BaseStore | None = None
):
    """Build the workflow.

    The checkpointer is needed for the pauses; the store is long-term memory.
    """
    builder = StateGraph(ReportState)
    builder.add_node("triage", nodes.triage_node)
    builder.add_node("routing", nodes.routing_node)
    builder.add_node("context_check", nodes.context_check_node)
    builder.add_node("known_outage", nodes.known_outage_node)
    builder.add_node("duplicate_check", nodes.duplicate_check_node)
    builder.add_node("save_report", nodes.save_report_node)
    builder.add_node("human_review", nodes.human_review_node)
    builder.add_node("finish_review", nodes.finish_review_node)
    builder.add_node("drafter", nodes.drafter_node)
    builder.add_node("draft_review", nodes.draft_review_node)
    builder.add_node("finish_draft", nodes.finish_draft_node)

    builder.add_edge(START, "triage")
    builder.add_edge("triage", "routing")
    builder.add_conditional_edges("routing", after_routing)
    builder.add_conditional_edges("context_check", after_context_check)
    builder.add_edge("known_outage", END)
    builder.add_edge("duplicate_check", "save_report")
    builder.add_edge("save_report", "human_review")
    builder.add_edge("human_review", "finish_review")
    builder.add_conditional_edges("finish_review", after_review)
    builder.add_edge("drafter", "draft_review")
    builder.add_edge("draft_review", "finish_draft")
    builder.add_edge("finish_draft", END)
    return builder.compile(checkpointer=checkpointer, store=store)
