"""PokéAPI tool: fetches live Pokemon data from PokéAPI for verification."""

import json
import urllib.request
import urllib.error
from langchain_core.tools import tool

POKEAPI_BASE = "https://pokeapi.co/api/v2"


def _fetch(endpoint: str) -> dict | None:
    """Fetch data from PokéAPI."""
    url = f"{POKEAPI_BASE}/{endpoint}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "CobblemonDeepAgent/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"error": "Not found"}
        return {"error": f"HTTP {e.code}"}
    except Exception as e:
        return {"error": str(e)}


@tool
def pokeapi_fetch(query: str) -> str:
    """Use this tool to VERIFY or LOOK UP Pokemon data from the official PokéAPI.
    This fetches live data from pokeapi.co (free, no API key needed).

    HOW TO USE:
    - To get Pokemon data: "pokemon/<name>" (e.g., "pokemon/charizard")
    - To get a move: "move/<name>" (e.g., "move/thunderbolt")
    - To get an ability: "ability/<name>" (e.g., "ability/intimidate")
    - To get evolution chain: "evolution-chain/<id>" (e.g., "evolution-chain/2")
    - To get egg group: "egg-group/<name>" (e.g., "egg-group/monster")
    - To get Pokemon species: "pokemon-species/<name>" (e.g., "pokemon-species/eevee")
    - To get a list of all Pokemon: "pokemon?limit=1302"
    - To search: just pass the resource name/endpoint

    Always format the query as the API endpoint path.
    This tool returns RAW JSON data - you must interpret it for the user."""
    data = _fetch(query)
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching '{query}': {data['error']}"
    return json.dumps(data, indent=2, ensure_ascii=False)[:8000]
