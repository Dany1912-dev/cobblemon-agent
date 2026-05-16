"""Move sub-agent: knows all Pokemon moves/attacks."""

from langchain_core.tools import tool
from . import load_knowledge


@tool
def move_knowledge(query: str) -> str:
    """Use this tool for ANY question about Pokemon moves/attacks/movimientos.
    Call this when the user asks about move stats (power, accuracy, PP), move effects,
    which Pokemon learn a specific move, best moves for a Pokemon, move coverage,
    priority moves, status moves, setup moves, entry hazards, or any move-related topic.
    You have full knowledge of all 900+ Pokemon moves from training data."""
    return load_knowledge("moves.txt")
