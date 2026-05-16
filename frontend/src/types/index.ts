export interface Message {
  id: string;
  role: 'user' | 'agent';
  content: string;
  image?: string;
  toolUsed?: string | null;
  timestamp: Date;
}

export interface ChatResponse {
  response: string;
  tool_used: string | null;
  image_analyzed: boolean;
  session_id: string | null;
}
