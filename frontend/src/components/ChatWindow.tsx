import { useEffect, useRef } from 'react';
import type { Message } from '../types';
import MessageBubble from './MessageBubble';
import { Cherry } from 'lucide-react';

interface Props {
  messages: Message[];
  loading: boolean;
}

export default function ChatWindow({ messages, loading }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  if (messages.length === 0) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-center p-8">
        <div className="w-20 h-20 rounded-full bg-zinc-800 flex items-center justify-center mb-6">
          <Cherry size={36} className="text-emerald-400" />
        </div>
        <h2 className="text-xl font-semibold text-zinc-200 mb-2">
          Asistente Cobblemon
        </h2>
        <p className="text-zinc-500 max-w-lg text-sm leading-relaxed">
          Pregúntame sobre{' '}
          <span className="text-emerald-400">bayas</span>,{' '}
          <span className="text-amber-400">objetos</span>,{' '}
          <span className="text-indigo-400">tipos</span>,{' '}
          <span className="text-cyan-400">spawns</span>,{' '}
          <span className="text-red-400">movimientos</span>,{' '}
          <span className="text-purple-400">evoluciones</span>,{' '}
          <span className="text-pink-400">crianza</span>,{' '}
          <span className="text-yellow-400">habilidades</span>,{' '}
          <span className="text-orange-400">stats</span>,{' '}
          <span className="text-rose-400">mega evoluciones</span>,{' '}
          <span className="text-teal-400">TMs</span>,{' '}
          y <span className="text-lime-400">equipos competitivos</span>.
          También verifico datos en vivo desde la{' '}
          <span className="text-sky-400">PokéAPI</span> y analizo screenshots.
        </p>
        <div className="mt-8 grid grid-cols-3 gap-3 text-xs text-zinc-500">
          <div className="bg-zinc-800/50 rounded-lg p-3 hover:bg-zinc-800 transition-colors cursor-default">
            <span className="text-emerald-400 font-medium block mb-1">Bayas</span>
            ¿Qué baya cura el veneno?
          </div>
          <div className="bg-zinc-800/50 rounded-lg p-3 hover:bg-zinc-800 transition-colors cursor-default">
            <span className="text-amber-400 font-medium block mb-1">Objetos</span>
            ¿Para qué sirve el Choice Band?
          </div>
          <div className="bg-zinc-800/50 rounded-lg p-3 hover:bg-zinc-800 transition-colors cursor-default">
            <span className="text-cyan-400 font-medium block mb-1">Spawns</span>
            ¿Dónde encuentro a Dratini?
          </div>
          <div className="bg-zinc-800/50 rounded-lg p-3 hover:bg-zinc-800 transition-colors cursor-default">
            <span className="text-purple-400 font-medium block mb-1">Evoluciones</span>
            ¿Cómo evoluciono a Gengar?
          </div>
          <div className="bg-zinc-800/50 rounded-lg p-3 hover:bg-zinc-800 transition-colors cursor-default">
            <span className="text-red-400 font-medium block mb-1">Movimientos</span>
            ¿Qué hace Dragon Dance?
          </div>
          <div className="bg-zinc-800/50 rounded-lg p-3 hover:bg-zinc-800 transition-colors cursor-default">
            <span className="text-pink-400 font-medium block mb-1">Crianza</span>
            ¿Qué son los Egg Groups?
          </div>
          <div className="bg-zinc-800/50 rounded-lg p-3 hover:bg-zinc-800 transition-colors cursor-default">
            <span className="text-rose-400 font-medium block mb-1">Mega</span>
            ¿Cómo mega evoluciono a Charizard?
          </div>
          <div className="bg-zinc-800/50 rounded-lg p-3 hover:bg-zinc-800 transition-colors cursor-default">
            <span className="text-teal-400 font-medium block mb-1">TMs</span>
            ¿Qué TM es Earthquake?
          </div>
          <div className="bg-zinc-800/50 rounded-lg p-3 hover:bg-zinc-800 transition-colors cursor-default">
            <span className="text-sky-400 font-medium block mb-1">PokéAPI</span>
            Verifica stats de Garchomp
          </div>
          <div className="bg-zinc-800/50 rounded-lg p-3 hover:bg-zinc-800 transition-colors cursor-default">
            <span className="text-lime-400 font-medium block mb-1">Competitivo</span>
            ¿Cómo armo equipo con Garchomp?
          </div>
          <div className="bg-zinc-800/50 rounded-lg p-3 hover:bg-zinc-800 transition-colors cursor-default">
            <span className="text-rose-400 font-medium block mb-1">Sinergia</span>
            ¿Quiénes cubren las debilidades de Tyranitar?
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto p-4 scroll-smooth">
      {messages.map(msg => (
        <MessageBubble key={msg.id} message={msg} />
      ))}

      {/* Loading indicator */}
      {loading && (
        <div className="flex gap-3 mb-4">
          <div className="w-8 h-8 rounded-full bg-emerald-600 flex items-center justify-center shrink-0">
            <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          </div>
          <div className="bg-zinc-800 rounded-2xl rounded-tl-md px-4 py-3">
            <div className="flex gap-1.5">
              <span className="w-2 h-2 bg-zinc-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
              <span className="w-2 h-2 bg-zinc-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
              <span className="w-2 h-2 bg-zinc-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
            </div>
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  );
}
