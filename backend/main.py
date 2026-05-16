"""FastAPI server for the Cobblemon DeepAgent with session persistence."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from orchestrator import run_orchestrator
from db import list_conversations, get_conversation, get_messages, delete_conversation


class ChatRequest(BaseModel):
    message: str
    image: str | None = None
    session_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    tool_used: str | None = None
    image_analyzed: bool = False
    session_id: str | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Cobblemon DeepAgent",
    description="AI assistant for Cobblemon with 15 specialized sub-agents. Hybrid: DeepSeek + Gemini. SQLite persistence.",
    version="0.3.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "Cobblemon DeepAgent", "sub_agents": 15}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.message.strip() and not req.image:
        raise HTTPException(status_code=400, detail="Message or image is required.")

    try:
        result = await run_orchestrator(
            message=req.message or "Describe lo que ves en esta imagen de Cobblemon.",
            image_base64=req.image,
            session_id=req.session_id,
        )
        return ChatResponse(**result)
    except Exception as e:
        error_msg = str(e)
        if "API_KEY" in error_msg or "DEEPSEEK_API" in error_msg:
            return ChatResponse(
                response="Error de configuración: API key no encontrada. Revisa backend/.env",
            )
        return ChatResponse(response=f"Error: {error_msg[:300]}")


# ---- Session management endpoints ----

@app.get("/sessions")
async def list_sessions():
    """List recent conversations."""
    return {"conversations": list_conversations()}


@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """Get a conversation with all its messages."""
    conv = get_conversation(session_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    messages = get_messages(session_id)
    return {"conversation": conv, "messages": messages}


@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a conversation."""
    delete_conversation(session_id)
    return {"status": "deleted", "session_id": session_id}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
