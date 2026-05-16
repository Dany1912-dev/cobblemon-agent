"""Competitive Team Building sub-agent: expert in synergy, strategy, and teambuilding."""

from langchain_core.tools import tool
from . import load_knowledge


@tool
def competitive_knowledge(query: str) -> str:
    """Use this tool for ANY question about competitive Pokemon team building.
    Call this when the user asks about:
    - Building a team around a specific Pokemon
    - Team synergy (sinergia de equipo)
    - What Pokemon work well together
    - Countering specific threats
    - Team archetypes (Hyper Offense, Balance, Stall, Weather, Trick Room)
    - Roles (sweeper, wallbreaker, pivot, wall, hazard setter/remover)
    - Best items for competitive (Choice items, Life Orb, Leftovers, etc.)
    - Speed tiers and benchmarks
    - Weather/terrain/trick room teams
    - Meta threats and popular Pokemon
    - Which Pokemon counters another
    - EV spreads and nature recommendations
    - Teambuilding step-by-step guidance
    This tool contains comprehensive competitive strategy data."""
    return load_knowledge("competitive.txt")
