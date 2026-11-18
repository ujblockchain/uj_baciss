"""Drafter Agent: writes a suggested reply from the policy documents."""

from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

from community_voice.llm.providers import Provider, get_chat_model
from community_voice.schemas.context_check import ContextCheckResult, Finding
from community_voice.schemas.draft import DraftResponse
from community_voice.schemas.routing import RoutingResult
from community_voice.schemas.triage import TriageResult
from community_voice.tools.policy import search_policy

SYSTEM_PROMPT = """\
You draft a short, polite reply from a municipality to a citizen who reported a \
service problem.
Use search_policy to find the reply template, the response times for the urgency \
level, and the department charter for this exact problem. Quote only times you \
found there.
If the charter gives a time for this exact problem, use that time for the crew or \
repair. Use the urgency rules only for the acknowledgement time, or when the \
charter has no time for this problem.
Fill in the template with the details given. Do not invent facts, dates, times \
or phone numbers. If no phone number is given, leave that sentence out.
If a web check is given, you may say the issue is publicly known.
Write in English, at most 120 words, and list the policy files you used.
"""


def write_draft(
    report_id: str,
    triaged: TriageResult,
    routed: RoutingResult,
    context: ContextCheckResult | None = None,
    provider: Provider = "gemini",
) -> DraftResponse:
    """Draft a reply. A person approves it before it counts as ready to send."""
    agent = create_agent(
        model=get_chat_model(provider),
        tools=[search_policy],
        system_prompt=SYSTEM_PROMPT,
        response_format=ToolStrategy(DraftResponse),
    )
    lines = [
        f"Reference: {report_id}",
        f"Issue: {triaged.summary}",
        f"Area: {triaged.area_mentioned or 'not given'}",
        f"Urgency: {triaged.urgency.value}",
        f"Department: {routed.department}",
    ]
    if context and context.finding is not Finding.NOTHING_FOUND:
        lines.append(f"Web check: {context.finding.value}. {context.summary}")
    content = "\n".join(lines)
    state = agent.invoke({"messages": [{"role": "user", "content": content}]})
    return state["structured_response"]
