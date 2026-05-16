"""Type chart sub-agent: knows everything about Cobblemon type matchups."""

from langchain_core.tools import tool
from . import load_knowledge


@tool
def type_knowledge(query: str) -> str:
    """Use this tool for ANY question about Pokemon type effectiveness, type chart,
    type matchups, or which types are strong/weak against other types.
    Call this when the user asks about type advantages, weaknesses, resistances,
    immunities, STAB (Same Type Attack Bonus), or type coverage.
    The query parameter should be the user's question about types."""
    return load_knowledge("types.txt")
