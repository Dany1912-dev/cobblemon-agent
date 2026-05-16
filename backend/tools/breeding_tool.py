"""Breeding sub-agent: knows all Pokemon breeding mechanics."""

from langchain_core.tools import tool
from . import load_knowledge


@tool
def breeding_knowledge(query: str) -> str:
    """Use this tool for ANY question about Pokemon breeding/crianza.
    Call this when the user asks about breeding mechanics, egg groups,
    egg moves, how to get baby Pokemon, incubating eggs, hatching time,
    incense breeding, passing down IVs/natures, Destiny Knot, Everstone,
    or any breeding-related topic.
    You have full knowledge of Pokemon breeding from training data."""
    return load_knowledge("breeding.txt")
