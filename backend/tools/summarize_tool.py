"""Summarization tool: compresses conversation context for persistence."""

from langchain_core.tools import tool
from langchain_deepseek import ChatDeepSeek
import os


@tool
def summarize_context(conversation_text: str) -> str:
    """Use this tool to SUMMARIZE or compress the conversation history.
    Call this when the conversation is getting long, when the user is leaving,
    or when you need to save context for a future session.
    The input should be the conversation text to summarize.
    Returns a condensed summary that preserves key information."""
    if not conversation_text.strip():
        return "(conversación vacía)"

    key = os.getenv("DEEPSEEK_API")
    if not key:
        # Fallback: return truncated version
        return conversation_text[-2000:]

    llm = ChatDeepSeek(model="deepseek-chat", api_key=key, temperature=0.0)

    prompt = (
        "Resume la siguiente conversación sobre Pokémon/Cobblemon en español. "
        "Máximo 300 palabras. Incluye: qué Pokémon se mencionaron, temas consultados, "
        "decisiones o recomendaciones dadas, y cualquier preferencia del usuario. "
        "Este resumen se usará para restaurar el contexto cuando el usuario vuelva.\n\n"
        f"CONVERSACIÓN:\n{conversation_text[-4000:]}"
    )

    try:
        response = llm.invoke(prompt)
        return response.content if hasattr(response, "content") else str(response)
    except Exception:
        return f"(error al resumir) {conversation_text[-1000:]}"
