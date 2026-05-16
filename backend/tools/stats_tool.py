"""Stats sub-agent: knows Pokemon stats, EVs, IVs, natures."""

from langchain_core.tools import tool
from . import load_knowledge


@tool
def stats_knowledge(query: str) -> str:
    """Use this tool for ANY question about Pokemon stats/estadísticas.
    Call this when the user asks about base stats, stat calculations,
    EVs (Effort Values), IVs (Individual Values), natures (naturalezas),
    competitive stat spreads, which nature is best for a Pokemon,
    EV training, Hyper Training, or any stats-related topic.
    You have full knowledge of all Pokemon base stats from training data."""
    return load_knowledge("stats.txt")
