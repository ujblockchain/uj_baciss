"""Routing Agent: a ReAct agent that uses tools to pick municipality and department."""

from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

from community_voice.llm.providers import Provider, get_chat_model
from community_voice.schemas.routing import RoutingResult
from community_voice.schemas.triage import TriageResult
from community_voice.tools.directory import find_municipality, lookup_department

SYSTEM_PROMPT = """\
You route citizen reports to the right municipality and department.
First call find_municipality with the area, then call lookup_department with \
the municipality and the category.
If the area is missing or not found, do not guess: use 'unknown' and set \
needs_human to true.
"""


def _build_agent(provider: Provider, tools: list):
    return create_agent(
        model=get_chat_model(provider),
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        # Groq cannot mix JSON mode with tools, so use a tool call for the result.
        response_format=ToolStrategy(RoutingResult),
    )


def _input(triage_result: TriageResult) -> dict:
    area = triage_result.area_mentioned or "not mentioned"
    content = f"Category: {triage_result.category.value}\nArea: {area}"
    return {"messages": [{"role": "user", "content": content}]}


def run_routing_agent(triage_result: TriageResult, provider: Provider = "groq") -> dict:
    """Run the agent. Returns the full state: 'messages' and 'structured_response'."""
    agent = _build_agent(provider, [find_municipality, lookup_department])
    return agent.invoke(_input(triage_result))


async def arun_routing_agent(
    triage_result: TriageResult, tools: list, provider: Provider = "groq"
) -> dict:
    """Same agent, with tools passed in (for example from an MCP server)."""
    return await _build_agent(provider, tools).ainvoke(_input(triage_result))


def route(triage_result: TriageResult, provider: Provider = "groq") -> RoutingResult:
    """Return only the routing decision."""
    return run_routing_agent(triage_result, provider)["structured_response"]
