"""TM/TR/HM sub-agent: knows all Technical Machines and their moves."""

from langchain_core.tools import tool
from . import load_knowledge


@tool
def tm_knowledge(query: str) -> str:
    """Use this tool for ANY question about TMs, TRs, HMs (Technical Machines).
    Call this when the user asks about which TM to teach a move, TM numbers,
    TM locations, which Pokemon can learn a specific TM, TM compatibility,
    or any TM/TR/HM-related topic.
    Contains the full Gen IX TM catalog (229 TMs) and historic HMs."""
    return load_knowledge("tms.txt")
