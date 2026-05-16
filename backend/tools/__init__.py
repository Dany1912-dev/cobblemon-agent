"""Base tool class that loads knowledge from .txt files."""

from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


def load_knowledge(filename: str) -> str:
    """Load knowledge from a .txt file in the data directory."""
    filepath = DATA_DIR / filename
    if not filepath.exists():
        return f"Error: knowledge file '{filename}' not found."
    return filepath.read_text(encoding="utf-8")
