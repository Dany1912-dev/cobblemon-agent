import type { Message } from '../types';
import { User, Bot, Wrench } from 'lucide-react';

interface Props {
  message: Message;
}

export default function MessageBubble({ message }: Props) {
  const isUser = message.role === 'user';

  return (
    <div className={`flex gap-3 ${isUser ? 'flex-row-reverse' : ''} mb-4`}>
      {/* Avatar */}
      <div
        className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
          isUser
            ? 'bg-indigo-600'
            : 'bg-emerald-600'
        }`}
      >
        {isUser ? <User size={16} /> : <Bot size={16} />}
      </div>

      {/* Content */}
      <div className={`max-w-[75%] ${isUser ? 'items-end' : 'items-start'}`}>
        {/* Image preview */}
        {message.image && (
          <img
            src={message.image}
            alt="Uploaded"
            className="max-w-[240px] max-h-[240px] rounded-lg mb-2 border border-zinc-700 object-contain"
          />
        )}

        {/* Text bubble */}
        <div
          className={`rounded-2xl px-4 py-3 text-sm leading-relaxed whitespace-pre-wrap ${
            isUser
              ? 'bg-indigo-600 text-white rounded-tr-md'
              : 'bg-zinc-800 text-zinc-100 rounded-tl-md'
          }`}
        >
          {message.content}
        </div>

        {/* Tool used badge */}
        {message.toolUsed && (
          <div className="flex items-center gap-1 mt-1 text-xs text-zinc-500">
            <Wrench size={10} />
            <span>Subagente: {message.toolUsed}</span>
          </div>
        )}

        {/* Timestamp */}
        <div className={`text-xs text-zinc-600 mt-1 ${isUser ? 'text-right' : 'text-left'}`}>
          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>
    </div>
  );
}
