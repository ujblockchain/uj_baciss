"""MCP server: exposes the directory and policy tools to any MCP client."""

from fastmcp import FastMCP

from community_voice.mcp_server import HOST, PORT
from community_voice.tools import directory

mcp = FastMCP("Community Voice")


@mcp.tool
def find_municipality(area: str) -> str:
    """Find the municipality for an area. Known names inside the text also match."""
    return directory.find_municipality.invoke({"area": area})


@mcp.tool
def lookup_department(municipality: str, category: str) -> str:
    """Find the department and phone number for a service category in a municipality.

    Categories: water, electricity, roads, sanitation, waste, other.
    """
    args = {"municipality": municipality, "category": category}
    return directory.lookup_department.invoke(args)


@mcp.tool
def search_policy(query: str) -> str:
    """Search service charters, response-time rules and reply templates."""
    # Imported here: Chroma is slow to load and only this tool needs it.
    from community_voice.tools.policy import search_policy as policy_tool

    return policy_tool.invoke({"query": query})


if __name__ == "__main__":
    # HTTP: the server runs on its own. For stdio use mcp.run() with no arguments.
    mcp.run(transport="http", host=HOST, port=PORT)
