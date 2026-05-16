import ChatWindow from './components/ChatWindow';
import ChatInput from './components/ChatInput';
import { useChat } from './hooks/useChat';
import { Cherry } from 'lucide-react';

export default function App() {
  const { messages, loading, sendMessage } = useChat();

  return (
    <div className="h-screen flex flex-col bg-zinc-950">
      {/* Header */}
      <header className="flex items-center gap-3 px-5 py-3 border-b border-zinc-800 bg-zinc-900/80 backdrop-blur">
        <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-emerald-500 to-emerald-700 flex items-center justify-center">
          <Cherry size={20} />
        </div>
        <div>
          <h1 className="text-sm font-semibold text-zinc-100">Cobblemon DeepAgent</h1>
          <p className="text-xs text-zinc-500">
            14 subagentes · Enjaulado en Pokémon/Cobblemon
          </p>
        </div>
        <div className="ml-auto flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          <span className="text-xs text-zinc-400">Online</span>
        </div>
      </header>

      {/* Chat area */}
      <ChatWindow messages={messages} loading={loading} />

      {/* Input area */}
      <ChatInput onSend={sendMessage} loading={loading} />
    </div>
  );
}
