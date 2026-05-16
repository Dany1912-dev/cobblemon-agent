import { useState, useCallback, useRef } from 'react';
import type { Message, ChatResponse } from '../types';

const API_URL = '/api/chat';
const SESSION_KEY = 'cobblemon_session_id';

function getSessionId(): string | null {
  return localStorage.getItem(SESSION_KEY);
}

function saveSessionId(id: string) {
  localStorage.setItem(SESSION_KEY, id);
}

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const sessionId = useRef<string | null>(getSessionId());

  const sendMessage = useCallback(async (text: string, image?: string) => {
    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content: text || 'Analiza esta imagen:',
      image,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMsg]);
    setLoading(true);

    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          image: image || null,
          session_id: sessionId.current,
        }),
      });

      if (!res.ok) throw new Error(`Error ${res.status}`);

      const data: ChatResponse = await res.json();

      // Store session ID for future messages
      if (data.session_id) {
        sessionId.current = data.session_id;
        saveSessionId(data.session_id);
      }

      const agentMsg: Message = {
        id: crypto.randomUUID(),
        role: 'agent',
        content: data.response,
        toolUsed: data.tool_used,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, agentMsg]);
    } catch (err) {
      const errorMsg: Message = {
        id: crypto.randomUUID(),
        role: 'agent',
        content: `Error: no se pudo conectar con el servidor. Asegúrate de que el backend esté corriendo.`,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  }, []);

  return { messages, loading, sendMessage, sessionId: sessionId.current };
}
