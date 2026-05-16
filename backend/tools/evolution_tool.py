"""Evolution sub-agent: knows all Pokemon evolution methods."""

from langchain_core.tools import tool
from . import load_knowledge


@tool
def evolution_knowledge(query: str) -> str:
    """Use this tool for ANY question about Pokemon evolution.
    Call this when the user asks how a Pokemon evolves, at what level,
    what item is needed, trade evolutions, Link Cable usage (Cobblemon-specific),
    friendship evolutions, time-based evolutions, location-based evolutions,
    special evolution conditions, or any evolution-related topic.
    You have full knowledge of all Pokemon evolution methods from training data."""
    return load_knowledge("evolutions.txt")
