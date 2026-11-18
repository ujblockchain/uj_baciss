"""Turns a graph run into a stream of events."""

import logging
from collections.abc import Iterator
from typing import Any

from fastapi.sse import ServerSentEvent

from community_voice.api.schemas import (
    DoneEvent,
    ErrorEvent,
    PausedEvent,
    StepEvent,
)

logger = logging.getLogger(__name__)

# The graph step a paused report is waiting in, and what the caller should do.
WAITING = {"human_review": "review", "draft_review": "draft"}


def thread_config(report_id: str) -> dict:
    return {"configurable": {"thread_id": report_id}}


def describe(node: str, update: dict) -> str:
    """A short plain-language line for a finished step."""
    if node == "triage":
        triaged = update["triage_result"]
        return f"{triaged.category.value}, {triaged.urgency.value} urgency"
    if node == "routing":
        return update["routing_result"].department
    if node == "context_check":
        return update["context_result"].finding.value
    if node == "duplicate_check":
        duplicate = update["duplicate_result"].duplicate_of
        return f"duplicate of {duplicate}" if duplicate else "no duplicate"
    if node == "human_review":
        return f"reviewer chose to {update['review'].action}"
    if node == "draft_review":
        return f"reviewer chose to {update['draft_decision'].action}"
    if node in ("known_outage", "finish_review", "finish_draft"):
        return update["status"]
    if node == "save_report":
        return "saved"
    if node == "drafter":
        return "draft written"
    return "done"


def stream_run(
    graph: Any, graph_input: Any, report_id: str, show_payload: bool = True
) -> Iterator[ServerSentEvent]:
    """Run the graph and yield one event per finished step, then pause or done.

    show_payload=False leaves out what the reviewer sees (for citizens).
    """
    config = thread_config(report_id)
    try:
        for chunk in graph.stream(
            graph_input, config, stream_mode="updates", version="v2"
        ):
            if chunk["type"] != "updates":
                continue
            for node, update in chunk["data"].items():
                if node == "__interrupt__":
                    continue
                step = StepEvent(node=node, message=describe(node, update or {}))
                yield ServerSentEvent(data=step, event="step")
        snapshot = graph.get_state(config)
        if snapshot.next:
            paused = PausedEvent(
                waiting_for=WAITING[snapshot.next[0]],
                payload=snapshot.interrupts[0].value if show_payload else None,
            )
            yield ServerSentEvent(data=paused, event="paused")
        else:
            done = DoneEvent(status=snapshot.values["status"])
            yield ServerSentEvent(data=done, event="done")
    except Exception as error:
        # Details stay in the server log; the caller only learns that it failed.
        logger.exception("Workflow failed for %s", report_id)
        message = f"The workflow failed ({type(error).__name__})."
        yield ServerSentEvent(data=ErrorEvent(message=message), event="error")
