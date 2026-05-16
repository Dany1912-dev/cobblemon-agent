"""Berry sub-agent: knows everything about Cobblemon berries."""

from langchain_core.tools import tool
from . import load_knowledge


@tool
def berry_knowledge(query: str) -> str:
    """Use this tool for ANY question about Cobblemon berries (bayas).
    Call this when the user asks about berry effects, which berry cures a status,
    type-resist berries, EV-reducing berries, berry farming, berry recipes,
    or any other berry-related topic.
    The query parameter should be the user's question about berries."""
    return load_knowledge("berries.txt")
