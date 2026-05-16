"""SQLite database for conversation persistence and session management."""

import sqlite3
import json
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "conversations.db"


def get_db() -> sqlite3.Connection:
    """Get database connection, creating tables if needed."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    _create_tables(conn)
    return conn


def _create_tables(conn: sqlite3.Connection):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            title TEXT DEFAULT 'Nueva conversación',
            context_summary TEXT,
            message_count INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
            role TEXT NOT NULL CHECK(role IN ('user', 'agent')),
            content TEXT NOT NULL,
            tool_used TEXT,
            image_used INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE INDEX IF NOT EXISTS idx_messages_conv ON messages(conversation_id, id);
    """)


# ---------- Conversation CRUD ----------

def create_conversation(conv_id: str, title: str = "Nueva conversación") -> dict:
    db = get_db()
    db.execute(
        "INSERT OR IGNORE INTO conversations (id, title) VALUES (?, ?)",
        (conv_id, title),
    )
    db.commit()
    return get_conversation(conv_id)


def get_conversation(conv_id: str) -> dict | None:
    db = get_db()
    row = db.execute(
        "SELECT * FROM conversations WHERE id = ?", (conv_id,)
    ).fetchone()
    if not row:
        return None
    return dict(row)


def list_conversations(limit: int = 20) -> list[dict]:
    db = get_db()
    rows = db.execute(
        "SELECT id, title, message_count, updated_at FROM conversations ORDER BY updated_at DESC LIMIT ?",
        (limit,),
    ).fetchall()
    return [dict(r) for r in rows]


def update_context_summary(conv_id: str, summary: str):
    db = get_db()
    db.execute(
        "UPDATE conversations SET context_summary = ?, updated_at = datetime('now') WHERE id = ?",
        (summary, conv_id),
    )
    db.commit()


def update_title(conv_id: str, title: str):
    db = get_db()
    db.execute(
        "UPDATE conversations SET title = ?, updated_at = datetime('now') WHERE id = ?",
        (title, conv_id),
    )
    db.commit()


def delete_conversation(conv_id: str):
    db = get_db()
    db.execute("DELETE FROM conversations WHERE id = ?", (conv_id,))
    db.commit()


# ---------- Message CRUD ----------

def add_message(conv_id: str, role: str, content: str, tool_used: str = None, image_used: bool = False):
    db = get_db()
    db.execute(
        "INSERT INTO messages (conversation_id, role, content, tool_used, image_used) VALUES (?, ?, ?, ?, ?)",
        (conv_id, role, content, tool_used, int(image_used)),
    )
    db.execute(
        "UPDATE conversations SET message_count = message_count + 1, updated_at = datetime('now') WHERE id = ?",
        (conv_id,),
    )
    db.commit()


def get_messages(conv_id: str, limit: int = 50) -> list[dict]:
    db = get_db()
    rows = db.execute(
        "SELECT role, content, tool_used, created_at FROM messages WHERE conversation_id = ? ORDER BY id ASC LIMIT ?",
        (conv_id, limit),
    ).fetchall()
    return [dict(r) for r in rows]


def get_recent_context(conv_id: str, max_messages: int = 20) -> str:
    """Get recent messages as formatted context string."""
    messages = get_messages(conv_id, max_messages)
    if not messages:
        return ""

    lines = []
    for m in messages:
        role_emoji = "🧑" if m["role"] == "user" else "🤖"
        lines.append(f"{role_emoji} [{m['role']}]: {m['content'][:500]}")

    return "\n".join(lines)


def get_or_create_session(conv_id: str | None) -> tuple[str, dict | None, str]:
    """Get existing conversation context or create new session.
    Returns (conv_id, previous_summary, recent_context).
    """
    if conv_id:
        conv = get_conversation(conv_id)
        if conv:
            recent = get_recent_context(conv_id)
            return conv_id, conv.get("context_summary"), recent

    # New session
    import uuid
    new_id = uuid.uuid4().hex[:12]
    create_conversation(new_id)
    return new_id, None, ""
