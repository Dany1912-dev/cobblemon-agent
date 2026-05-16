"""Spawn sub-agent: knows where to find every Pokemon in Cobblemon."""

from langchain_core.tools import tool
from . import load_knowledge


@tool
def spawn_knowledge(query: str) -> str:
    """Use this tool for ANY question about WHERE to find Pokemon in Cobblemon.
    Call this when the user asks about spawn locations, biomes, where a Pokemon appears,
    spawn conditions (day/night, weather, Y-level), legendary spawns,
    or any question about finding/locating Pokemon in the Minecraft world.
    This covers Cobblemon-specific spawn mechanics and biome data."""
    return load_knowledge("spawns.txt")
