"""Duplicate check: find similar stored reports, then ask a model to confirm."""

from community_voice.llm.providers import get_chat_model
from community_voice.rag.reports import find_similar
from community_voice.schemas.duplicate import DuplicateResult, SameIncident

# Smaller distance = closer. Loose on purpose: the model makes the final call.
MAX_DISTANCE = 1.0

SYSTEM_PROMPT = """\
Do these two citizen reports describe the same incident: the same problem in \
the same place? A different place or a different problem is not the same incident.
"""


def _confirm(new_text: str, old_text: str) -> SameIncident:
    model = get_chat_model("groq").with_structured_output(SameIncident)
    result = model.invoke(
        [
            ("system", SYSTEM_PROMPT),
            ("human", f"Report A: {new_text}\nReport B: {old_text}"),
        ]
    )
    return SameIncident.model_validate(result)


def check_duplicate(report_id: str, text: str, category: str) -> DuplicateResult:
    """Compare a report with stored ones. Storing happens later, in save_report."""
    result = DuplicateResult()
    for candidate in find_similar(text, category):
        if candidate["id"] == report_id or candidate["distance"] > MAX_DISTANCE:
            continue
        verdict = _confirm(text, candidate["text"])
        if verdict.same_incident and result.duplicate_of is None:
            result.duplicate_of = candidate["id"]
            result.reason = verdict.reason
        else:
            result.related_ids.append(candidate["id"])
    return result
