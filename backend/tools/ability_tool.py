"""Ability sub-agent: knows all Pokemon abilities."""

from langchain_core.tools import tool
from . import load_knowledge


@tool
def ability_knowledge(query: str) -> str:
    """Use this tool for ANY question about Pokemon abilities/habilidades.
    Call this when the user asks what ability a Pokemon has, which ability is best,
    hidden abilities, ability effects, ability changes in battle,
    overworld ability effects, or any ability-related topic.
    You have full knowledge of all Pokemon abilities from training data."""
    return load_knowledge("abilities.txt")
