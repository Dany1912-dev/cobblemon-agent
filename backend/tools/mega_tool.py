"""Mega Evolution sub-agent: knows all Mega Evolutions, stones, stats, and abilities."""

from langchain_core.tools import tool
from . import load_knowledge


@tool
def mega_knowledge(query: str) -> str:
    """Use this tool for ANY question about Mega Evolutions.
    Call this when the user asks about Mega Stones, which Pokemon can Mega Evolve,
    Mega stat changes, Mega abilities, type changes during Mega Evolution,
    Primal Reversion, or any Mega Evolution-related topic.
    Covers all 48+ Mega forms and their mechanics."""
    return load_knowledge("mega_evolutions.txt")
