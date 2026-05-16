"""File export tool: saves responses to .txt files on request."""

from pathlib import Path
from datetime import datetime
from langchain_core.tools import tool

EXPORTS_DIR = Path(__file__).parent.parent / "exports"


@tool
def save_to_file(content: str, filename: str = "") -> str:
    """Use this tool when the user asks you to save, export, or download something to a .txt file.
    Examples: 'guárdame eso en un archivo', 'exporta la respuesta a txt', 'dame un archivo con esto'.

    Parameters:
    - content: The text content to save (the answer, data, or information)
    - filename: Optional filename (without .txt extension). If empty, a name with date/time is generated.

    Returns the path where the file was saved."""
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    if not filename:
        filename = datetime.now().strftime("export_%Y-%m-%d_%H-%M-%S")

    safe_name = "".join(c for c in filename if c.isalnum() or c in "_-.").rstrip()
    filepath = EXPORTS_DIR / f"{safe_name}.txt"

    filepath.write_text(content, encoding="utf-8")
    return f"Archivo guardado exitosamente en: {filepath}"
