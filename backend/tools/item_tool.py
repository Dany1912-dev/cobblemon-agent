"""Item sub-agent: knows everything about Cobblemon items."""

from langchain_core.tools import tool
from . import load_knowledge


@tool
def item_knowledge(query: str) -> str:
    """Use this tool for ANY question about Cobblemon items (objetos).
    Call this when the user asks about held items, evolution items, medicine,
    Poké Balls, type-boosting items, battle items, food, crafting ingredients,
    or any other item-related topic.
    The query parameter should be the user's question about items."""
    return load_knowledge("items.txt")
