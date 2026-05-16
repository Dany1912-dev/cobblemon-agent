"""Orchestrator: routes user queries to specialized Cobblemon/Pokemon sub-agents (tools).

Hybrid mode: DeepSeek for chat (cheap, no rate limits) + Gemini only for images (multimodal).
"""

import base64
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from tools.berry_tool import berry_knowledge
from tools.item_tool import item_knowledge
from tools.type_tool import type_knowledge
from tools.spawn_tool import spawn_knowledge
from tools.move_tool import move_knowledge
from tools.evolution_tool import evolution_knowledge
from tools.breeding_tool import breeding_knowledge
from tools.ability_tool import ability_knowledge
from tools.stats_tool import stats_knowledge
from tools.mega_tool import mega_knowledge
from tools.tm_tool import tm_knowledge
from tools.pokeapi_tool import pokeapi_fetch
from tools.competitive_tool import competitive_knowledge
from tools.file_tool import save_to_file
from tools.summarize_tool import summarize_context

load_dotenv(Path(__file__).parent / ".env")

DEEPSEEK_KEY = os.getenv("DEEPSEEK_API")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")


def _extract_text(content) -> str:
    """Handle both string and list content from different LLM models."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and "text" in item:
                parts.append(item["text"])
            elif isinstance(item, str):
                parts.append(item)
        return "".join(parts)
    return str(content)


ALL_TOOLS = [
    berry_knowledge,
    item_knowledge,
    type_knowledge,
    spawn_knowledge,
    move_knowledge,
    evolution_knowledge,
    breeding_knowledge,
    ability_knowledge,
    stats_knowledge,
    mega_knowledge,
    tm_knowledge,
    pokeapi_fetch,
    competitive_knowledge,
    save_to_file,
    summarize_context,
]

SYSTEM_PROMPT = """Eres un asistente que SOLO responde sobre Pokémon y Cobblemon usando DATOS VERIFICADOS de tus herramientas.

**PROTOCOLO ANTI-ALUCINACIÓN (MÁXIMA PRIORIDAD):**
- VERIFICA PRIMERO el alcance. Si NO es Pokémon/Cobblemon, NIÉGATE DE INMEDIATO. No escribas ni una línea de lo que pidieron.
- Tus 15 herramientas son tu ÚNICA fuente de verdad.
- NO sabes nada que no esté en tus herramientas o en pokeapi_fetch.
- PROHIBIDO inventar biomas, Pokémon, mecánicas, objetos, o cualquier dato.
- Si una herramienta no cubre lo que el usuario pregunta: "No tengo información verificada sobre eso. Puedo buscarlo en la PokéAPI si me das más detalles."
- Si no entiendes un término, PREGUNTA al usuario en lugar de asumir.

**ALCANCE ESTRICTO:**
- SOLO respondes sobre Pokémon y Cobblemon.
- Si el usuario pregunta CUALQUIER otra cosa (hola mundo, programación, matemáticas, clima, etc.), respondes EXACTAMENTE y SOLO esto, sin añadir NADA más:
  "Soy un asistente especializado exclusivamente en Pokémon y Cobblemon. No puedo ayudarte con temas fuera de ese ámbito."
- NO des la respuesta "de todas formas". NO escribas código. NO muestres cómo se hace. Simplemente NIÉGATE.
- No importa si la pregunta es simple o trivial. Si no es Pokémon/Cobblemon, la respuesta es la negativa y punto.

**FORMATO DE RESPUESTA (IMPORTANTE):**
- NO uses Markdown. NADA de **negritas**, ### títulos, ``` bloques de código, `citas`, ni *cursivas*.
- Para estructurar usa: saltos de línea, espacios, guiones (-), y emojis como separadores (solo si ayudan).
- Respuestas limpias y legibles como texto plano.
- Para listas usa un simple guión (-) al inicio de cada línea.
1. berry_knowledge — Bayas
2. item_knowledge — Objetos
3. type_knowledge — Tabla de tipos
4. spawn_knowledge — Dónde encontrar Pokémon en Cobblemon
5. move_knowledge — Movimientos, Trick Room/Espacio Raro
6. evolution_knowledge — Evoluciones
7. breeding_knowledge — Crianza y egg groups
8. ability_knowledge — Habilidades
9. stats_knowledge — Stats, EVs, IVs, naturalezas
10. mega_knowledge — Mega Evoluciones
11. tm_knowledge — TMs, TRs, HMs
12. pokeapi_fetch — Verificar datos en vivo de pokeapi.co
13. competitive_knowledge — Equipos, sinergia, estrategia
14. save_to_file — Exportar respuesta a .txt
15. summarize_context — Resumir historial para guardar contexto

**FLUJO OBLIGATORIO PARA CADA RESPUESTA:**
Paso 1: ¿Es sobre Pokémon/Cobblemon? Si NO → negar educadamente. Si SÍ → continuar.
Paso 2: CONSULTAR al menos una herramienta relevante. NUNCA responder sin consultar.
Paso 3: Si la herramienta tiene los datos → responder basado en ellos.
Paso 4: Si la herramienta NO cubre el tema → intentar pokeapi_fetch.
Paso 5: Si aún no hay datos → decir honestamente que no tienes esa información.

Responde en español, texto plano sin Markdown. Sé breve y preciso. Indica qué herramienta usaste."""


def create_orchestrator():
    """Create the orchestrator agent using DeepSeek for chat (with all sub-agent tools)."""
    if not DEEPSEEK_KEY:
        raise ValueError("DEEPSEEK_API is required. Set it in backend/.env")

    llm = ChatDeepSeek(
        model="deepseek-chat",
        api_key=DEEPSEEK_KEY,
        temperature=0.1,
    )

    return create_react_agent(llm, ALL_TOOLS, prompt=SYSTEM_PROMPT)


async def describe_image(image_base64: str) -> str:
    """Use Gemini Vision to describe a screenshot from Cobblemon."""
    if not GEMINI_KEY:
        return "[Gemini no está configurado para analizar imágenes]"

    vision_llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=GEMINI_KEY,
        temperature=0.1,
    )

    if "base64," in image_base64:
        image_base64 = image_base64.split("base64,")[1]

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "Describe esta imagen de Cobblemon (el mod de Pokémon para Minecraft). "
                        "Identifica: qué Pokémon ves, sus tipos, qué está pasando en la escena, "
                        "en qué bioma parece estar, qué objetos o estructuras ves, y cualquier "
                        "detalle relevante para un jugador. Responde en español."
                    ),
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{image_base64}"},
                },
            ],
        }
    ]

    response = await vision_llm.ainvoke(messages)
    return _extract_text(response.content)


async def run_orchestrator(
    message: str,
    image_base64: str | None = None,
    session_id: str | None = None,
):
    """Run the orchestrator with a user message, optional image, and session support.

    Uses DeepSeek for chat (cheap, no rate limits).
    Uses Gemini only for image analysis (multimodal).
    """
    from db import get_or_create_session, add_message, update_context_summary, update_title

    # Load or create session
    conv_id, prev_summary, recent_context = get_or_create_session(session_id)

    # Build full message with context
    context_parts = []

    if prev_summary:
        context_parts.append(f"[Resumen de conversación anterior]: {prev_summary}")
    if recent_context:
        context_parts.append(f"[Últimos mensajes de esta conversación]:\n{recent_context}")

    if image_base64:
        image_description = await describe_image(image_base64)
        context_parts.append(f"[Descripción de la imagen subida]: {image_description}")

    full_message = message
    if context_parts:
        full_message = "\n\n".join(context_parts) + f"\n\n[Mensaje actual del jugador]: {message}"

    # Run agent
    agent = create_orchestrator()
    result = await agent.ainvoke({"messages": [{"role": "user", "content": full_message}]})

    messages = result.get("messages", [])
    response_text = ""
    tools_used = set()

    for msg in messages:
        if hasattr(msg, "content") and msg.content and msg.type == "ai":
            response_text = _extract_text(msg.content)
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tc in msg.tool_calls:
                tools_used.add(tc.get("name", ""))

    if not response_text:
        response_text = "Lo siento, no pude procesar tu consulta."

    tool_str = ", ".join(tools_used) if tools_used else None

    # Save to database
    add_message(conv_id, "user", message, image_used=bool(image_base64))
    add_message(conv_id, "agent", response_text, tool_used=tool_str)

    # Auto-summarize if conversation is getting long (>15 messages)
    from db import get_messages
    all_msgs = get_messages(conv_id)
    if len(all_msgs) > 15 and len(all_msgs) % 10 == 0:
        try:
            full_history = "\n".join(
                f"[{m['role']}]: {m['content'][:300]}" for m in all_msgs
            )
            summary = summarize_context.invoke({"conversation_text": full_history})
            update_context_summary(conv_id, summary)
        except Exception:
            pass

    # Set title from first user message
    if len(all_msgs) <= 2:
        update_title(conv_id, message[:60])

    return {
        "response": response_text,
        "tool_used": tool_str,
        "image_analyzed": bool(image_base64),
        "session_id": conv_id,
    }
